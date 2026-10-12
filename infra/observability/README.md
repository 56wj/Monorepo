# Observability

M2 exposes one trace ID across HTTP submission, durable jobs, worker callbacks
and structured logs. Prometheus collects control-plane job lifecycle metrics,
solver-worker execution metrics and Planning Agent latency/evaluation metrics.

Key indicators:

- queue depth by state and queue-delay histogram;
- solver duration, concurrency, retry, lease expiry and job dead-letter rate;
- Agent request latency, executable/draft outcomes and retrieval-hit count;
- service `up` and health probes.

Grafana provisioning loads `grafana/dashboards/packing-platform.json`. Alerts
cover control-plane/worker availability, queue backlog, lease expiry and job
failure rate. Notification publishing queues and broker consumers no longer exist.
Best-effort notification failures are logged; the browser recovers state through
HTTP polling even when a WebSocket is disconnected or connected to another replica.
