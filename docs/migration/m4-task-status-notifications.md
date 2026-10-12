# M4: state-based task notifications

## Current contract

The MySQL job queue, leasing, heartbeats, idempotent completion, computation
retries and terminal job failures are unchanged. Kafka and the notification
Outbox implementation, cursor API (`/task/events`), event schema, publishing
retry/dead-letter mechanisms, dependencies and monitoring have been removed.

`JobResultHandler` registers a transaction synchronization. Only after commit
does a bounded executor attempt a WebSocket hint (`code=20000`, `data.taskId`).
The hint is not a computation result. Rollback produces no hint. Disconnection,
executor saturation or process failure may lose the hint; they never roll back
or fail an already committed computation. There is no delivery acknowledgement,
notification persistence, or promise of per-event replay.

The authenticated `GET /task/job?taskId=42&includeResult=true` endpoint returns:

- Existing job metadata: ID, type, status, attempts, errors and timestamps.
- `output`: the persisted worker completion object, only for `SUCCEEDED`.
  `output.result` may be a JSON string or a JSON value.
- `config`: the job input configuration used to restore a reloaded page.

Without `includeResult`, output/config are omitted as null. Missing tasks and
non-owned tasks return 404. Payloads and results are read after ownership checks.
The latest job for the task is authoritative, including the second pallet stage.

Both calculation pages query immediately after submission, upon a matching
WebSocket hint, upon connection/reconnection, and every five seconds while
running. Terminal states stop polling; transient errors back off to 30 seconds.
401/403/404 stop retries. The task ID and stage in the URL restore tracking after
reload. Generation checks ignore responses from an old task/stage or a destroyed
page. Cached inactive pages pause polling and resume active jobs on return. No open WebSocket is required to submit or complete a task.

A multi-replica control plane may send a hint on the wrong replica because
sessions are local. HTTP polling still converges on durable state. This is an
explicit latency tradeoff, not a broadcast guarantee. Shared artifact storage
is still a separate requirement for horizontally scaling file-backed results.

## Deployment and database migration

1. Back up the database (including notification history if it must be retained).
2. Drain/stop all old control-plane replicas before migration. Do not mix old
   notification writers and this version during the schema change.
3. Deploy the new frontend and backend together. Old frontends expect result
   payloads in WebSocket messages and are not compatible with hint-only delivery.
4. Run the application's normal Flyway startup migrations:
   - V4 is intentionally byte-for-byte unchanged so existing installations pass
     checksum validation. Fresh databases also apply V4 before V5.
   - V5 drops `packing_outbox_event`; this permanently removes notification
     history, not jobs or computation results. Export that table first if needed.
5. The M2 Compose file no longer declares a broker, its environment variables,
   dependency or volume. Remove a previously running orphan Kafka container
   explicitly after verifying the new stack; do not use `down -v` on the stack.
   Existing broker volumes may be retained for rollback rather than wiped.
6. Remove obsolete `KAFKA_*` and `OUTBOX_*` deployment variables.

The code change itself does not execute a migration against an existing database.

## Verification

From `apps/control-plane`: `mvn clean package`.

Opt-in MySQL integration (use a disposable instance; each test creates/drops a
random `notify_test_*` database and needs database creation privileges):

```sh
NOTIFICATION_TEST_MYSQL_URL=jdbc:mysql://127.0.0.1:13317/ \
NOTIFICATION_TEST_MYSQL_USER=root \
NOTIFICATION_TEST_MYSQL_PASSWORD='' mvn clean package
```

Without the URL, the two database integration cases are explicitly skipped.
From `apps/web-console`: `npm run test:unit -- --runInBand` and `npm run build:prod`.

Regression tests cover post-commit-only hints, rollback, send failure, executor
rejection, owner-scoped result recovery, first/second-stage configuration,
missed hints, reconnect wakeups, duplicate wakeups, terminal states, transient
failures, stale in-flight responses, page reload and teardown.

Release smoke checks:

1. Complete a task with the browser WebSocket closed. Polling must show results.
2. Reload during calculation; the URL restores the same task and stage.
3. Submit the second pallet stage; a stale first-stage response must not reopen
   its result editor. Confirm suspension and pallet-final result navigation.
4. Verify terminal compute failures clear the loading state.
5. Query another user's task; expect 404 and no output.
6. Verify fresh migration V1–V5 and upgrade from V4 in a disposable database.

## Rollback

Keep the previous source/release and a pre-upgrade database backup. Restoring
only old code after V5 is insufficient: restore the compatible pre-V5 schema,
notification data and Flyway history together, then start old services and the
matching frontend. Coordinate this with any jobs created after the backup; do
not overwrite live task data blindly. For code comparison, the local pre-edit
snapshot is stored outside the repository under `tmp/remove-messaging-backup`.

The historical notification benchmark JSON in `evals/benchmarks/results` is
retained as evidence of its original revision and is not a current release gate.

## Verified on 2026-10-12

- Backend: 36 tests passed, including two real MySQL 8.0.41 integration tests.
- Both fresh V1–V5 migration and V4-to-V5 upgrade passed Flyway validation.
- Existing job result survives migration; separate connections see committed
  state before notification; rollback produces neither a state change nor a hint.
- Packaged application starts without a broker; `/actuator/health` returns `UP`
  against a disposable database. Temporary services were shut down afterward.
- Frontend: 22 focused notification/reconnect tests passed; production build and
  lint of the new modules/tests passed. Full suite: 59 passed, 1 pre-existing
  failure (`validUsername('xxxx')` returns true). That implementation and test
  are unchanged. Existing bundle-size warnings remain.
- Compose configuration and `git diff --check` passed. Packaged JAR contains no
  retired messaging classes or broker libraries. Original V4 bytes are intact.
- Browser UI smoke was not executed: the browser tool's approval quota was
  exhausted. No claim of visual or end-to-end solver acceptance is made.
- No existing application database was migrated. All database checks used a
  separate temporary MySQL instance and randomly named test databases.

Machine-readable evidence: `evals/benchmarks/results/task-notification-simplification-20261012.json`.
