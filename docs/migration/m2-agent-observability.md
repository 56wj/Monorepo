# M2 Planning Agent and observability

## Delivered topology

```text
user request
  -> Planning Agent 8200
       -> BM25 sparse-RAG rule_search
       -> constraint_extractor
       -> constraint_validator
       -> solver_router
  -> control plane 8101 -> MySQL durable queue -> solver worker
          |                                        |
          +---------- X-Trace-Id / trace_id -------+

Prometheus 9090 <- control plane management port 9100 / worker 9108 / Agent metrics
Grafana 3000    <- provisioned dashboard and alert rules
```

## Agent contract

`POST /v1/plans` accepts `query`, optional `orderContext`, and `topK`. The response contains typed constraints, missing fields, violations, solver route, citations and a five-state audit trail. An executable decision requires `max_weight_kg`, `max_height_mm`, and zero validation violations.

The corpus in `services/planning-agent/knowledge/rules.v1.json` contains synthetic rules only. Rule version and content hash appear in every result.

## Run

```bash
docker compose --env-file .env -f infra/compose/docker-compose.m2.yml up --build

curl -s http://localhost:8200/v1/plans \
  -H 'Content-Type: application/json' \
  -H 'X-Trace-Id: demo-trace-1234' \
  -d '{"query":"托盘装箱，最大承重1200kg，最大高度1600mm，禁止混装"}'
```

## Verification gates

```bash
(cd apps/control-plane && mvn test)
(cd services/solver-worker && python -m unittest -v tests/test_overlap_rules.py tests/test_worker_contract.py)
(cd services/planning-agent && PYTHONPATH=. python -m unittest discover -s tests -v)
python evals/agent/evaluate.py
python evals/benchmarks/load_test.py --mode inprocess --requests 1000 --concurrency 32
docker compose -f infra/compose/docker-compose.m2.yml config
```

For deployed acceptance, rerun the load generator with `--mode http`; use the committed SLO thresholds instead of presenting the in-process result as network throughput.

## Primary metrics

- `packing_job_queue_depth{status}`
- `packing_job_queue_delay_seconds`
- `packing_job_execution_seconds`
- `packing_jobs_retried_total{reason,job_type}`
- `packing_job_lease_expired_total{job_type}`
- `packing_worker_active_jobs{job_type}`
- `packing_worker_job_duration_seconds{job_type,outcome}`
- `packing_agent_plan_duration_seconds`
- `packing_agent_plan_requests_total{outcome,job_type}`

## Rollback

Stop M2 Compose and start `docker-compose.m1.yml`. Application code from M1 ignores the added `trace_id` column. The V2 migration is additive; retain it during rollback so previously written job rows remain readable.
