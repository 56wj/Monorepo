# M4+ production backend roadmap

Status: In progress - state-based task recovery delivered

## 1. Current baseline and the next real bottleneck

The repository already has the backend capabilities that are usually added
first: a durable MySQL job queue, Lease/heartbeat recovery, idempotent
completion, concurrent `SKIP LOCKED` claiming, trace propagation, metrics,
alerts, deterministic Agent evaluation and fault-injection benchmarks.

The next milestone should not add middleware for its own sake. It should close
four concrete gaps in the current execution path:

1. `solver-worker/api_test.py` fetches pallet, truck, tube and pallet-roll
   specifications while a job is running. A retry can therefore use different
   master data from the original attempt and produce a different answer.
2. `JobQueueService.complete` trusts the Worker result before committing it to
   the legacy task. `services/solution-validator` is still only a reserved
   directory, so a syntactically valid but infeasible packing plan can become a
   business result.
3. Task notifications are best effort after commit. HTTP state/result polling
   now handles offline clients, page reloads and missed hints. Per-event delivery
   and replay are deliberately not product requirements.
4. Source, intermediate and result artifacts are represented as local paths.
   This prevents stateless control-plane replicas and makes retention,
   integrity and access control difficult.

## 2. Recommended priority

| Priority | Milestone | Backend knowledge | Why it is worth doing now |
| --- | --- | --- | --- |
| P0 | Deterministic input snapshot + independent solution validation | immutable snapshots, canonical JSON, content hashing, validation state machine, trust boundaries | Most domain-specific improvement; fixes retry reproducibility and prevents invalid plans from becoming business results |
| Delivered | State-based task recovery | transaction commit hooks, bounded executor, authenticated status queries, frontend polling | Keeps computation durable without a separate notification delivery subsystem |
| P0 | Object storage abstraction | S3/MinIO, presigned URL, SHA-256, metadata transaction, lifecycle/retention | Removes node-local state and enables horizontal control-plane/Worker scaling |
| P1 | Security and tenant boundary | Spring Security, password migration, RBAC, refresh-token rotation, tenant row isolation, audit log | Current MD5 password and interceptor-based authorization are not a production boundary |
| P1 | Contract and error governance | typed DTO, runtime JSON Schema, OpenAPI, RFC 7807-style errors, compatibility tests | Replaces `Map<String,Object>` and opaque result strings with evolvable APIs |
| P1 | Real integration and chaos gates | Testcontainers MySQL, property-based geometry tests, fault injection, load/SLO regression | Converts the existing one-machine benchmark into a repeatable CI quality gate |
| P2 | Admission control and elastic compute | per-tenant quota, priority aging, backpressure, graceful drain, HPA/KEDA | Useful after correctness and data boundaries are stable; prevents one large order from monopolizing compute |

## 3. M4: deterministic, independently verified solutions

### 3.1 Submission-time snapshot

At submission, resolve every mutable dependency and persist one immutable
`SolverInputEnvelopeV2`:

```json
{
  "schemaVersion": "2.0",
  "taskId": 10001,
  "jobType": "PALLET_SECOND",
  "algorithm": {"name": "roll-pack", "version": "git-sha-or-image-digest"},
  "order": {},
  "specSnapshot": {
    "pallet": {},
    "trucks": [],
    "tubes": [],
    "palletRollRules": []
  },
  "submittedAt": "2026-09-08T10:00:00+08:00",
  "inputHash": "sha256-of-canonical-envelope-without-this-field"
}
```

Implementation rules:

- Canonicalize JSON before hashing: stable key ordering, explicit decimal
  normalization and UTF-8 encoding.
- Store `input_hash`, `algorithm_version` and `spec_snapshot_version` as queryable
  columns on `packing_job`; keep the full snapshot in `payload_json` initially.
- Remove runtime specification HTTP calls from the solver path. Retries consume
  the exact same envelope.
- Include the three versions/hashes in result metadata and logs.
- Reject a completion whose `taskId`, `inputHash` or algorithm identity does not
  match the active Lease.

### 3.2 Independent validator

Build `services/solution-validator` as a separately deployable service/library.
It must not import or call the optimization algorithm. It checks the solution
from first principles:

- item conservation: input quantity = placed quantity + explicit residue;
- bounds: every roll/tray is inside its pallet/container;
- collision: no pair overlaps beyond the configured epsilon;
- weight: pallet, container and configured side/axle limits;
- stacking: height, foam, overhang, overlap and lying-layer limits;
- business constraints: mixing, priority, arrival/order constraints;
- numeric safety: finite numbers, units, precision and tolerance;
- artifact integrity: declared checksum and referenced artifact existence.

Recommended completion state machine:

```text
RUNNING -> VALIDATING -> SUCCEEDED
                    \-> VALIDATION_FAILED -> RETRY_WAIT or QUARANTINED
```

The validation response should contain `validatorVersion`, `inputHash`,
`solutionHash`, `feasible`, typed violations, computed totals and duration. The
control plane persists the report before exposing a final result.

### 3.3 Acceptance criteria

- The same envelope run 20 times, including injected Worker crashes, retains the
  same `inputHash` and validation decision.
- Mutation tests cover one violation per invariant: missing item, out-of-bounds,
  overlap, overweight, excess height, illegal mixing and checksum mismatch.
- 100% of successful jobs have a persisted validation report and matching
  `inputHash`/`solutionHash`.
- Validator p95 stays below an agreed fraction of solver p95; start with 10% and
  report the measured number rather than hard-coding a resume claim.

### 3.4 Resume evidence after measurement

> Designed an immutable, versioned solver-input snapshot with canonical JSON and
> SHA-256 identity, eliminating retry-time master-data drift and making packing
> jobs reproducible across Worker restarts and algorithm releases.

> Built an independent packing-solution validation gate covering quantity
> conservation, boundary/collision, load and business constraints; persisted
> typed violation reports and prevented infeasible Worker output from entering
> the business result path.

## 4. Delivered: state-based task recovery

The completion transaction persists task and job results. After commit, a
bounded executor attempts a WebSocket hint containing only the task ID. The
browser queries the authenticated job endpoint immediately on submission,
notification and reconnect, and otherwise every five seconds while active.
Terminal states stop polling. Transient failures back off; authentication and
not-found responses stop polling. URL task/stage parameters restore tracking.

Acceptance criteria:

- Rollback never notifies; notifications start only after successful commit.
- Notification failure/executor saturation does not fail a committed callback.
- No WebSocket delivery is required to recover a result or terminal failure.
- Repeated hints and old in-flight responses do not duplicate UI transitions.
- Task ownership is checked before returning job output and configuration.

See `m4-task-status-notifications.md` for migration and verification.

## 5. M6: object storage and artifact lifecycle

Introduce an `ArtifactStore` interface with local and S3-compatible
implementations. Persist metadata instead of filesystem paths:

```text
artifact_id, tenant_id, task_id, kind, object_key, content_type, size_bytes,
sha256, status, created_at, expires_at
```

Upload through a temporary object key, verify size/checksum, then promote the
metadata to `READY`. Return short-lived presigned URLs only after task ownership
checks. Add lifecycle rules for temporary, failed and deleted-task artifacts.

Acceptance should include interrupted upload cleanup, checksum mismatch,
cross-tenant access rejection, concurrent download and expiry behavior.

Resume evidence:

> Abstracted packing inputs, JSON plans, images and Excel exports onto
> S3-compatible object storage with checksum verification, presigned access,
> metadata transactions and lifecycle cleanup, enabling stateless API replicas.

## 6. M7: security, contracts and delivery gates

### Security

- Upgrade to a supported Java/Spring baseline, then replace the custom login
  interceptor with Spring Security method/route authorization.
- Migrate MD5 password hashes on successful login to BCrypt/Argon2 without a
  forced all-user reset.
- Use short-lived access tokens, rotating refresh tokens, revocation and key
  rotation; separate Worker identity from user identity and prefer mTLS or
  workload identity in deployment.
- Add tenant/department ownership to every task, job, artifact and event query;
  test insecure direct object reference cases.
- Record append-only audit events for specification changes, replay, cancel,
  delete and result export.

### Contracts

- Replace controller `Map<String,Object>` parameters with versioned DTOs and
  bean validation.
- Validate JSON Schema at both contract boundaries in CI and at runtime.
- Return a stable error envelope containing `code`, `traceId`, field violations
  and retryability; never let the legacy interceptor rewrite internal errors.
- Generate OpenAPI and run backward-compatibility checks for published schemas.

### Verification

- Run MySQL job-queue integration tests with Testcontainers in CI.
- Add property-based tests for geometry invariants and metamorphic tests such as
  permutation invariance and monotonicity under larger capacity.
- Extend fault injection to database restart, Worker SIGKILL, validator timeout,
  object-store timeout and missed WebSocket notifications.
- Promote only when p95/p99, error ratio, validation failure ratio, backlog age
  and recovery-time SLOs pass against the same synthetic workload.

## 7. What not to add yet

- Task state is authoritative. Add a broker only for measured downstream event delivery requirements, not for UI refresh.
- Do not add Redis in front of the durable queue. It creates two sources of truth
  without solving the current reproducibility or correctness gaps.
- Do not split more microservices before object storage, contracts and tracing
  make services independently deployable.
- Do not claim “high concurrency” from a single throughput number. Keep the
  existing before/after workload, concurrency, p95/p99, duplicate count and
  failure-recovery evidence together.

## 8. Recommended implementation order

1. State-based task recovery and post-commit notifications - delivered in M4.
2. Add `SolverInputEnvelopeV2`, snapshot mutable specifications at submission
   and prove deterministic retry.
3. Implement the standalone validator and gate `SUCCEEDED` on its report.
4. Replace local result paths with `ArtifactStore` + MinIO in local Compose.
5. Upgrade the security boundary and enforce tenant ownership end to end.
6. Put Testcontainers, mutation/property tests and chaos/SLO regression in CI.
7. Only then add quota-aware scheduling and Kubernetes Worker autoscaling.
