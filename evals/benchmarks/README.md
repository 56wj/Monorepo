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
