# Legacy baseline

Migration date: 2026-09-01

| Component | Source repository | Source branch | Baseline commit |
| --- | --- | --- | --- |
| Control plane | `wj56/packing_service` | `feature/overlap-validation-20260821` | `9fe4241` |
| Solver worker | `wj56/py3dbp` | `feature/overlap-validation-20260821` | `995734f` |
| Web console | `wj56/packing_service_frontend` | `feature/overlap-validation-20260821` | `d987b0d` plus reviewed local WebSocket/asset fixes |

The monorepo imports working-tree source code without nested `.git` directories, dependency folders, build output, runtime logs, production SQL dumps, or private environment configuration.

## Initial technical debt retained intentionally

- Java uses `@Async` plus manually created threads for solver calls and timeout handling.
- Python spawns processes per request and reports completion through HTTP callbacks.
- Intermediate and result artifacts are represented as filesystem paths.
- Task state transitions are string-based and are not protected by a durable job lease.

These behaviors define the measurable V1 baseline for the job-control-plane migration.
