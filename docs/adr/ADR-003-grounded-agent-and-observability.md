# ADR-003: Deterministic grounded planning and unified job telemetry

- Status: Accepted
- Date: 2026-09-02

## Context

Natural-language packing requests introduce ambiguity, while a remote model can add cost, latency, nondeterminism, and ungrounded constraints. M1 also lacked a common trace identity and measurable service objectives across submission, queueing and solving.

## Decision

1. Implement Planning Agent as a typed, replayable state machine: `INTAKE`, `RETRIEVE`, `EXTRACT`, `VALIDATE`, `ROUTE`.
2. Use a versioned local rule corpus and BM25 retrieval for M2. Every decision returns citations, `ruleVersion`, `corpusHash`, `requestHash`, and an audit trail.
3. Keep model use behind a future adapter. The deterministic path remains the fallback oracle and evaluation baseline.
4. Persist `trace_id` with every durable job and propagate it through worker claim, heartbeat, completion and failure calls.
5. Export bounded-cardinality metrics through Prometheus and provision Grafana dashboards and alert rules from source control.
6. Gate Agent changes with exact-match and citation-coverage evals; measure concurrency separately in-process and over HTTP.

## Consequences

- Agent output is explainable, reproducible and safe to feed into the solver only after validation.
- Rule changes have a stable version/hash and can be correlated with production outcomes.
- Sparse retrieval is intentionally simpler than an embedding/vector stack. Hybrid retrieval and a model tool-calling adapter can be added without changing response contracts.
- In-process benchmark numbers describe code-path capacity, not deployed end-to-end capacity; HTTP mode is the deployment acceptance test.
