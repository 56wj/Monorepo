# Roll Load AI Platform

Enterprise-oriented monorepo for roll packing optimization, long-running compute orchestration, deterministic solution validation, and a planning agent.

## Current baseline

- `apps/control-plane`: Spring Boot business API and durable job control plane.
- `apps/web-console`: legacy Vue operations console and 3D viewer.
- `services/solver-worker`: Python packing solver with leased, process-isolated worker slots.
- `services/planning-agent`: reserved for natural-language-to-constraint orchestration.
- `services/solution-validator`: reserved for independent feasibility validation.
- `evals`: replay, agent, and compute benchmarks.
- `contracts`: versioned cross-service schemas.
- `infra`: local and production infrastructure definitions.

M1 replaces the Java thread/process-per-request dispatch path with a MySQL-backed leased job control plane and a configurable concurrent Python worker.

## M1 highlights

- Durable jobs and Flyway migrations.
- Atomic submission and idempotency keys.
- `FOR UPDATE SKIP LOCKED` concurrent claiming.
- Worker leases, heartbeat, crash recovery, exponential retry, and dead-letter handling.
- Versioned Java/Python JSON contracts.
- Solver subprocess isolation and configurable parallel slots.

See `docs/migration/m1-job-control-plane.md` for verification and local topology.

## Repository policy

Real orders, database dumps, internal addresses, credentials, generated artifacts, and customer files must not be committed. Use `.env.example` and `testdata/synthetic` for reproducible local development.
