# Planning Agent

Rule-grounded sparse-RAG planning service that turns natural-language packing requirements into a typed constraint draft.

The M2 implementation is deliberately deterministic: retrieval, extraction, validation, routing, citations, and the audit trail can be replayed without an external model. A model adapter can later be inserted behind the same typed contract without changing the control plane.

```bash
python -m pip install -r requirements.txt
uvicorn planning_agent.api:app --host 0.0.0.0 --port 8200
python -m unittest discover -s tests -v
```

Endpoints:

- `POST /v1/plans`: retrieve rules, extract constraints, validate and select a solver job type.
- `POST /v1/knowledge/search`: inspect grounded retrieval results.
- `GET /healthz`: liveness plus corpus version.
- `GET /metrics`: Prometheus metrics.

Every response carries `X-Trace-Id`, `ruleVersion`, source citations, and an `auditTrail` suitable for replay.
