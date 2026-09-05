# M3 job reliability quantification

## Scope

This benchmark measures the backend long-running-job control path, not Planning
Agent or packing-algorithm throughput. Both revisions ran on the same machine
against MySQL 8.0.46, a local Spring Boot JVM, 32 HTTP clients and synthetic job
payloads.

- Baseline: commit `44bf5b591b0cb5458418ee24d71d121a145a758b`.
- Optimized: `feature/m2-agent-observability` working tree with M3 claim locking fix.
- Workload: 1,000 claims, 100 pairs of duplicate completion requests, 20 Worker
  crash injections with a 10-second lease, and 40 process-isolation jobs.
- Raw reports:
  - `evals/benchmarks/results/job-reliability-baseline-44bf5-20260905.json`
  - `evals/benchmarks/results/job-reliability-20260905.json`

## Result

| Metric | Baseline | Optimized | Change |
| --- | ---: | ---: | ---: |
| Claim success, 1,000 jobs | 99.1% | 100% | all jobs claimed |
| Claim throughput | 332.3 jobs/s | 673.6 jobs/s | +102.7% |
| Claim latency p95 | 261.8 ms | 85.9 ms | -67.2% |
| Terminal claim errors in claim phase | 9 | 0 | -100% |
| Duplicate claims | 0 | 0 | unchanged |
| Duplicate-completion business side effects | 0 | 0 | unchanged |
| Crash recovery success, 20 jobs | 100% | 100% | unchanged |
| Failure-to-reclaim p95, 10 s lease | 10.09 s | 10.13 s | no regression |
| Stale Lease response observed by Worker | 401 | 409 | correct conflict semantics |
| Hung child processes terminated | 8/8 | 8/8 | unchanged |
| Orphaned child processes | 0 | 0 | unchanged |

The baseline server recorded 17 `DeadlockLoserDataAccessException` responses
across all claim phases (9 in the 1,000-job claim phase and 8 while preparing
the idempotency phase). The legacy login interceptor then replaced the original
error dispatch with an empty HTTP 401, hiding both claim deadlocks and stale
Lease conflicts from the Worker.

## Root cause and fix

1. Claim mixed expired-Lease reaping and normal task acquisition in one
   transaction. Concurrent callers acquired the Lease and claim indexes in
   conflicting orders.
2. The claim query order did not match its composite index. MySQL used a
   filesort and locked a large candidate set before updating one row.
3. `/error` was not excluded from the legacy JWT interceptor, so internal API
   exceptions were rewritten as HTTP 401 during error dispatch.

M3 separates Lease Reaper from claim transactions, adds an index-aligned order
(`status`, `available_at`, descending `priority`, `created_at`, `id`), and lets
`/error` preserve the original internal API status. `EXPLAIN FORMAT=TREE` after
V3 shows the `idx_packing_job_claim` range scan without a Sort node.

## Resume-ready evidence

- Built a MySQL durable task queue with `FOR UPDATE SKIP LOCKED`, Lease/heartbeat
  and scheduled recovery; in a 32-concurrency, 1,000-job test, removed claim
  deadlocks, improved throughput from 332.3 to 673.6 jobs/s, and reduced p95
  latency from 261.8 to 85.9 ms with zero duplicate claims.
- Added Idempotency Key, Lease Token and optimistic version checks; 100 duplicate
  completion pairs produced zero duplicate business writes, while 20 injected
  Worker crashes recovered successfully and all 20 stale writes were rejected.
- Isolated solver jobs in bounded child processes; 8 injected hung processes
  were terminated within 1.23 s p95, with 32/32 healthy sibling jobs succeeding
  and zero orphan processes.

The 10.13-second recovery number is tied to the benchmark's 10-second Lease.
For another deployment, report the configured Lease together with its measured
recovery latency.
