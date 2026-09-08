# M4 Transactional Outbox

## Delivered vertical slice

M4 removes the database/WebSocket dual write from the durable packing-job
completion path. The legacy task update, `packing_job` terminal transition and
Outbox event insert now participate in the same MySQL transaction. A separate
leased dispatcher publishes committed events after the transaction finishes.

```text
Solver Worker
  -> POST /internal/v1/jobs/{id}/complete
       MySQL transaction
         - update legacy packing result
         - insert packing_outbox_event (PENDING)
         - transition packing_job to SUCCEEDED
       commit

Outbox Dispatcher replica(s)
  -> SELECT ... FOR UPDATE SKIP LOCKED
  -> PENDING -> PUBLISHING with a short Lease
  -> WebSocket publish
  -> PUBLISHED
       or exponential retry -> DEAD_LETTER
```

Terminal task failures use the same path. Other legacy WebSocket messages are
outside this slice and remain unchanged.

## Delivery semantics

- Database state and event creation are atomic.
- Publication is at least once. A dispatcher crash after send but before the
  acknowledgement can cause the same event to be sent again.
- Every event has a stable `eventId`, also embedded in the notification data,
  so clients can deduplicate retries.
- `deduplication_key = packingJobPublicId:eventType` prevents duplicate logical
  events if the completion transaction is retried.
- Dispatcher ownership is protected by `lease_token`, `lease_expires_at` and
  optimistic `version` checks.
- Expired dispatcher leases are reaped independently from normal claims to
  avoid mixing lock orders.
- A publication failure uses bounded exponential backoff and enters
  `DEAD_LETTER` after the configured attempt budget.
- Lifecycle counters are registered after transaction commit, so a rolled-back
  database transition does not create a false successful metric.

The WebSocket endpoint itself has no application-level acknowledgement. A
successful publish therefore means that the durable event was offered to the
live channel. The Outbox row remains queryable for offline catch-up.

## Reconnect/catch-up API

Authenticated users can read only their own durable task events:

```http
GET /task/events?after=0&limit=100
```

The response returns an ordered event list and `nextCursor`. A client stores the
cursor after processing and supplies it on reconnect. Page size is bounded to
200 server-side. The numeric cursor is opaque to the client and the query is
always scoped by authenticated `user_id`.

## Schema and indexes

Flyway migration `V4__create_packing_outbox.sql` creates
`packing_outbox_event` with:

- stable event and deduplication identities;
- aggregate, event type, user and trace correlation;
- JSON payload and durable state;
- attempt budget, availability time and publisher Lease;
- timestamps for creation and publication;
- claim, Lease reaping, user cursor and aggregate indexes.

The claim query uses the index-aligned order
`status, available_at, created_at, id` and locks a single row with
`FOR UPDATE SKIP LOCKED`.

## Configuration

| Environment variable | Default | Purpose |
| --- | ---: | --- |
| `OUTBOX_LEASE_SECONDS` | 30 | Dispatcher ownership window |
| `OUTBOX_MAX_ATTEMPTS` | 8 | Maximum publication attempts |
| `OUTBOX_RETRY_BASE_SECONDS` | 2 | Exponential-backoff base |
| `OUTBOX_DISPATCH_BATCH_SIZE` | 50 | Maximum events per scheduled batch |
| `OUTBOX_DISPATCH_INTERVAL_MS` | 500 | Dispatcher polling interval |
| `OUTBOX_REAPER_BATCH_SIZE` | 100 | Expired Leases recovered per pass |
| `OUTBOX_REAPER_INTERVAL_MS` | 30000 | Expired-Lease scan interval |

## Observability

M4 exports bounded-cardinality metrics:

- `packing_outbox_depth{status}`
- `packing_outbox_events_enqueued_total{event_type}`
- `packing_outbox_events_published_total{event_type}`
- `packing_outbox_events_retried_total{event_type,reason}`
- `packing_outbox_events_dead_letter_total{event_type,reason}`
- `packing_outbox_publish_delay_seconds`

Prometheus alerts cover a sustained pending/publishing backlog and any Outbox
dead-letter event.

## Verification

```bash
cd apps/control-plane
mvn test
```

The test suite covers event identity/payload construction, cursor bounds,
leased claim, exponential retry, DLQ transition, dispatcher success/failure,
metrics and the real `JobResultHandler` business wiring.

A synthetic local MySQL 8 acceptance run is recorded at
`evals/benchmarks/results/outbox-reliability-20260908.json`. It verifies Flyway
V4, the claim index plan, atomic completion, duplicate-completion idempotency,
restart recovery, publish retry/DLQ, expired-Lease recovery, cursor catch-up and
exported metrics without containing production data.

For a deployed MySQL acceptance test, additionally verify:

1. stop the dispatcher after a completion commit and confirm the PENDING event
   is published after restart;
2. stop it after WebSocket send but before acknowledgement and confirm the same
   `eventId` is safely replayed;
3. run multiple control-plane replicas and confirm one active Lease per event;
4. force publication failures and confirm backoff plus terminal DLQ state;
5. reconnect with the previous cursor and confirm ordered, user-scoped catch-up.

## Known boundary and next step

Result JSON is still embedded in the notification and stored as a local file by
the control plane. The next storage milestone should replace large event payloads
with artifact metadata and an S3/MinIO object reference. Until then, monitor
Outbox table growth and keep retention cleanup explicit.

## Resume-ready statement

> Replaced database/WebSocket dual writes with a MySQL Transactional Outbox;
> implemented idempotent event creation, `SKIP LOCKED` multi-replica claiming,
> Lease recovery, bounded exponential retry, DLQ handling, trace propagation and
> cursor-based offline replay, with fault-path unit tests and Prometheus alerts.
