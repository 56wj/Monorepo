# Roll Load AI Platform

Enterprise-oriented monorepo for roll packing optimization, long-running compute orchestration, deterministic solution validation, and a planning agent.

## Current baseline

- `apps/control-plane`: legacy Spring Boot business and task API.
- `apps/web-console`: legacy Vue operations console and 3D viewer.
- `services/solver-worker`: legacy Python packing solver and HTTP worker.
- `services/planning-agent`: reserved for natural-language-to-constraint orchestration.
- `services/solution-validator`: reserved for independent feasibility validation.
- `evals`: replay, agent, and compute benchmarks.
- `contracts`: versioned cross-service schemas.
- `infra`: local and production infrastructure definitions.

The first milestone preserves a runnable legacy baseline before replacing its thread/process-per-request execution path with a durable asynchronous job control plane.

## Repository policy

Real orders, database dumps, internal addresses, credentials, generated artifacts, and customer files must not be committed. Use `.env.example` and `testdata/synthetic` for reproducible local development.
