# Concurrency benchmarks

`load_test.py` runs the planning path either in-process for deterministic CI regression or over HTTP for deployment-level load testing. Reports contain throughput, error rate, p50/p95/p99 and SLO verdicts.

```bash
# deterministic code-path benchmark
python load_test.py --mode inprocess --requests 1000 --concurrency 32 --output report.json

# deployed service benchmark
python load_test.py --mode http --url http://localhost:8200/v1/plans \
  --requests 2000 --concurrency 64 --output report.json
```

The benchmark payloads are synthetic and rotate through pallet, suspended and invalid-constraint scenarios.

## Durable job reliability benchmark

`job_reliability_benchmark.py` measures the backend mainline rather than the
Planning Agent. It drives the real MySQL 8 + Spring HTTP worker contract and
injects duplicate completion, expired leases, stale worker writes and hung
solver child processes.

```bash
python job_reliability_benchmark.py \
  --control-plane-url http://127.0.0.1:18101 \
  --mysql-port 33306 \
  --mysql-user root \
  --mysql-password "$MYSQL_ROOT_PASSWORD" \
  --claim-jobs 1000 \
  --idempotency-jobs 100 \
  --recovery-jobs 20 \
  --isolation-jobs 40 \
  --concurrency 32 \
  --lease-seconds 10 \
  --output results/job-reliability.json
```

The report separates four claims that may be used in project evidence:

- concurrent claim throughput, success rate and duplicate-claim count;
- idempotent convergence and duplicate business side-effect count;
- injected Worker-crash recovery latency/rate and stale-lease rejection rate;
- hung child-process termination, healthy sibling success and orphan count.

The crash benchmark uses a 10-second test lease. Production recovery time is
bounded by the configured lease plus reaper/poll interval, so keep the lease
value next to every reported recovery number. Synthetic payload results measure
control-plane reliability, not packing-algorithm throughput.

The benchmark database account needs permission to create the temporary audit
trigger used to prove exactly-once business side effects. The application itself
continues to run with the restricted `packing` account.
