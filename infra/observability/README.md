# Observability

M2 exposes one trace ID across HTTP submission, durable jobs, worker callbacks and structured logs. M4 extends that identity through durable task-event publication. Prometheus collects control-plane lifecycle metrics, Outbox delivery metrics, solver-worker execution metrics, and Planning Agent latency/evaluation metrics.

Key indicators:

- queue depth by state and queue-delay histogram;
- solver duration, concurrency, retry, lease expiry and dead-letter rate;
- Outbox depth, publish delay, retry, expired publisher Lease and event DLQ;
- Agent request latency, executable/draft outcomes and retrieval-hit count;
- service `up` and health probes.

Grafana provisioning loads `grafana/dashboards/packing-platform.json`. Alert rules cover control-plane/worker availability, queue backlog, Lease expiry, job dead-letter rate, Outbox backlog and Outbox dead letters.
