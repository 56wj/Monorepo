# Agent evaluation

Deterministic regression set for constraint exact match, solver routing, grounded citations, missing-field handling, and invalid-plan rejection.

```bash
python evaluate.py --output report.json
```

The command exits non-zero when exact-match accuracy drops below `0.95` or citation coverage drops below `1.0`, so it is suitable for CI gating.
