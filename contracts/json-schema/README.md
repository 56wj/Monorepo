# JSON Schema contracts

- `solver-job-v1.schema.json`: control plane → solver worker claim response.
- `solver-completion-v1.schema.json`: solver worker → control plane completion request.
- `planning-request-v1.schema.json`: natural-language request plus optional typed context.
- `planning-response-v1.schema.json`: grounded constraints, citations, route and replay audit.

Contracts are versioned independently from implementations so Java, Python, and later Agent services can run compatibility tests before deployment.
