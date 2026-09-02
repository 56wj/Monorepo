# Observability

M2 exposes one trace ID across HTTP submission, durable jobs, worker callbacks and structured logs. Prometheus collects control-plane lifecycle metrics, solver-worker execution metrics, and Planning Agent latency/evaluation metrics.

Key indicators:

- queue depth by state and queue-delay histogram;
- solver duration, concurrency, retry, lease expiry and dead-letter rate;
- Agent request latency, executable/draft outcomes and retrieval-hit count;
- service `up` and health probes.

Grafana provisioning loads `grafana/dashboards/packing-platform.json`. Alert rules cover control-plane/worker availability, queue backlog, lease expiry and dead-letter rate.
