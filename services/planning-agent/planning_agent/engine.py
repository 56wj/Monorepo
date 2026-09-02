import hashlib
import json
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from .constraints import extract_constraints, job_type_for, validate_constraints
from .models import PlanningRequest
from .retrieval import RuleRetriever


DEFAULT_CORPUS = Path(__file__).resolve().parents[1] / "knowledge" / "rules.v1.json"


class PlanningAgent:
    def __init__(self, retriever: RuleRetriever):
        self.retriever = retriever

    @classmethod
    def from_corpus(cls, path: Optional[Path] = None) -> "PlanningAgent":
        return cls(RuleRetriever.from_json(path or DEFAULT_CORPUS))

    def plan(self, request: PlanningRequest) -> Dict[str, Any]:
        query = request.query.strip()
        if not query:
            raise ValueError("query must not be empty")
        trace_id = request.trace_id or uuid.uuid4().hex
        request_hash = self._request_hash(query, request.order_context)
        audit = [{"state": "INTAKE", "status": "completed", "requestHash": request_hash}]

        hits = self.retriever.search(query, request.top_k)
        audit.append({
            "state": "RETRIEVE",
            "status": "completed",
            "tool": "rule_search",
            "resultCount": len(hits),
        })

        constraints = extract_constraints(query, request.order_context)
        audit.append({
            "state": "EXTRACT",
            "status": "completed",
            "tool": "constraint_extractor",
            "fields": sorted(constraints.keys()),
        })

        missing, violations, warnings = validate_constraints(constraints)
        audit.append({
            "state": "VALIDATE",
            "status": "blocked" if violations else "completed",
            "tool": "constraint_validator",
            "violationCount": len(violations),
        })

        job_type = job_type_for(constraints)
        executable = not missing and not violations
        audit.append({
            "state": "ROUTE",
            "status": "completed" if executable else "awaiting_constraints",
            "tool": "solver_router",
            "jobType": job_type,
        })
        citations = [hit.to_dict() for hit in hits]
        return {
            "traceId": trace_id,
            "requestHash": request_hash,
            "ruleVersion": self.retriever.rule_version,
            "corpusHash": self.retriever.corpus_hash,
            "constraints": constraints,
            "missingRequiredFields": missing,
            "violations": violations,
            "warnings": warnings,
            "decision": {
                "jobType": job_type,
                "executable": executable,
                "idempotencyKey": f"plan:{request_hash}:{job_type}",
            },
            "citations": citations,
            "groundedExplanation": self._explanation(citations, missing, violations, job_type),
            "auditTrail": audit,
        }

    @staticmethod
    def _request_hash(query: str, context: Dict[str, Any]) -> str:
        canonical = json.dumps(
            {"query": query, "orderContext": context},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:24]

    @staticmethod
    def _explanation(citations, missing, violations, job_type: str) -> str:
        sources = ", ".join(item["document_id"] for item in citations) or "no matched rule"
        if violations:
            return f"Constraint validation failed for {job_type}; evidence: {sources}."
        if missing:
            return f"Draft routed to {job_type}; required fields pending: {', '.join(missing)}; evidence: {sources}."
        return f"Constraints validated and routed to {job_type}; evidence: {sources}."
