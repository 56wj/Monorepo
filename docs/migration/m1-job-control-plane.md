# M1 durable job control plane

## Delivered vertical slice

- Durable `packing_job` schema managed by Flyway.
- Atomic legacy-task plus job submission.
- Capability-aware claim using `FOR UPDATE SKIP LOCKED`.
- Lease token, heartbeat, lease expiry recovery, bounded exponential retry, and dead-letter state.
- Idempotent completion and atomic result-file replacement.
- Configurable multi-slot Python worker with one isolated solver child process per slot.
- Dedicated read-only asset server for generated images and Excel exports.
- Authenticated internal worker API and versioned JSON contracts.
- User-facing `GET /task/job?taskId=...` status query.
- GitHub Actions gates for Java tests, Python tests, contracts, and Compose syntax.

## Local verification

```bash
cd apps/control-plane
mvn test

cd ../../services/solver-worker
python3 -m unittest -v tests/test_overlap_rules.py tests/test_worker_contract.py

cd ../../infra/compose
docker compose -f docker-compose.m1.yml config
```

For a full calculation, point MySQL at a schema containing the existing specification tables. Production dumps and real order data stay outside version control.

## Worker API

| Action | Endpoint | Key invariant |
| --- | --- | --- |
| Claim | `POST /internal/v1/jobs/claim` | Capability match and row lock |
| Heartbeat | `POST /internal/v1/jobs/{id}/heartbeat` | Current unexpired lease |
| Complete | `POST /internal/v1/jobs/{id}/complete` | Idempotent after success |
| Fail | `POST /internal/v1/jobs/{id}/fail` | Retry budget and backoff |

All calls carry `X-Worker-Token`.
