# Roll Load AI Platform

Enterprise-oriented monorepo for roll packing optimization, long-running compute orchestration, deterministic solution validation, and a planning agent.

## Current baseline

- `apps/control-plane`: Spring Boot business API and durable job control plane.
- `apps/web-console`: legacy Vue operations console and 3D viewer.
- `services/solver-worker`: Python packing solver with leased, process-isolated worker slots.
- `services/planning-agent`: rule-grounded natural-language-to-constraint Agent.
- `services/solution-validator`: reserved for independent feasibility validation.
- `evals`: replay, agent, and compute benchmarks.
- `contracts`: versioned cross-service schemas.
- `infra`: local and production infrastructure definitions.

M1 replaces the Java thread/process-per-request dispatch path with a MySQL-backed leased job control plane and a configurable concurrent Python worker.
M2 adds a replayable Planning Agent, BM25 rule retrieval, cross-service trace IDs, Prometheus/Grafana observability, agent eval gates, and concurrent load testing.
M3 adds repeatable long-task fault injection, fixes concurrent claim deadlocks, and records same-machine before/after evidence.
M4 uses committed task state as the source of truth, with post-commit WebSocket hints and authenticated HTTP polling.

The remaining production roadmap prioritizes immutable solver-input snapshots,
independent feasibility validation, object storage, security boundaries and
repeatable integration/chaos gates.

## M1 highlights

- Durable jobs and Flyway migrations.
- Atomic submission and idempotency keys.
- `FOR UPDATE SKIP LOCKED` concurrent claiming.
- Worker leases, heartbeat, crash recovery, exponential retry, and dead-letter handling.
- Versioned Java/Python JSON contracts.
- Solver subprocess isolation and configurable parallel slots.

See `docs/migration/m1-job-control-plane.md` for verification and local topology.

## M2 highlights

- Typed Agent state machine: `INTAKE -> RETRIEVE -> EXTRACT -> VALIDATE -> ROUTE`.
- Versioned rule corpus, BM25 sparse RAG, source citations, corpus hash, and deterministic request hash.
- Constraint normalization, invalid-plan rejection, solver routing, and idempotency key generation.
- Trace propagation from HTTP to durable job and worker callbacks.
- Micrometer/Prometheus lifecycle metrics plus solver and Agent metrics.
- Provisioned Grafana dashboard, alert rules, SLO thresholds, eval gate, and HTTP/in-process load generator.

See `docs/migration/m2-agent-observability.md` for architecture, commands, metrics, and verification.

## M3 highlights

- Real MySQL 8 + Spring HTTP benchmark for claim, duplicate completion, expired
  Lease recovery, stale Worker writes and child-process timeout isolation.
- Claim/Reaper transaction separation and index-aligned `SKIP LOCKED` ordering.
- 32-concurrency/1,000-job result: 673.6 jobs/s, p95 85.9 ms, 100% claim
  success and zero duplicate claims.
- 20/20 injected Worker crashes recovered with a 10.13-second p95 under a
  10-second test Lease; 20/20 stale writes were rejected.

See `docs/migration/m3-job-reliability-quantification.md` for the baseline,
optimized report, limitations and resume-ready evidence.

## M4 highlights

- MySQL job state and computation results remain durable; leases, retries and worker recovery are unchanged.
- Small best-effort WebSocket hints run on a bounded executor only after commit.
- The browser polls `/task/job?taskId=...&includeResult=true`, refreshes on reconnect and stops on terminal states.
- The task identifier/stage in the URL restores tracking on page reload; results are read only after ownership checks.
- Notification failures never turn a committed computation into a failed worker callback.

See `docs/migration/m4-task-status-notifications.md` for API semantics, migration,
verification and rollback. Historical benchmark results describe their recorded
revision, not the current notification architecture.

## Next production milestone

See `docs/migration/m4-production-backend-roadmap.md` for the repository-specific
gap analysis, implementation order, acceptance criteria and measurable resume
evidence. It deliberately avoids adding Kafka, Redis or extra microservices
before the current correctness and data-boundary gaps are closed.

## Repository policy

Real orders, database dumps, internal addresses, credentials, generated runtime artifacts, and customer files must not be committed. Use `.env.example` and `testdata/synthetic` for reproducible local development. Versioned reports under `evals/**/results` are limited to synthetic benchmark evidence and contain no production data.
