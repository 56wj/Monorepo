# JSON Schema contracts

- `solver-job-v1.schema.json`: control plane → solver worker claim response.
- `solver-completion-v1.schema.json`: solver worker → control plane completion request.

Contracts are versioned independently from implementations so Java, Python, and later Agent services can run compatibility tests before deployment.
