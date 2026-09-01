# ADR-001: Monorepo and control/compute separation

Status: Accepted

## Context

The legacy system is split across independent Java, Python, and frontend repositories. A packing request currently crosses all three components and produces long-running CPU-bound work, files, callbacks, and UI progress events.

## Decision

Maintain the platform in one monorepo while preserving independently deployable services. Spring Boot remains the durable control plane, and Python remains the compute plane. Cross-service requests and results will be defined by versioned contracts.

## Consequences

- Cross-component changes and integration tests can be committed atomically.
- Solver workers can scale and fail independently from the business API.
- Legacy behavior can be replayed before each migration step.
- Deployment boundaries remain explicit even though source control is unified.
