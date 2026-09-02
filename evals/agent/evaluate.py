#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "services" / "planning-agent"))

from planning_agent.engine import PlanningAgent  # noqa: E402
from planning_agent.models import PlanningRequest  # noqa: E402


def evaluate(cases_path: Path) -> dict:
    agent = PlanningAgent.from_corpus()
    cases = [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    details = []
    exact = 0
    grounded = 0
    for case in cases:
        result = agent.plan(PlanningRequest(
            query=case["query"],
            order_context=case.get("orderContext", {}),
        ))
        fields_match = all(result["constraints"].get(key) == value for key, value in case["expected"].items())
        route_match = result["decision"]["jobType"] == case["jobType"]
        executable_match = result["decision"]["executable"] == case["executable"]
        citation_ids = {item["document_id"] for item in result["citations"]}
        citation_match = case["citationContains"] in citation_ids
        exact_match = fields_match and route_match and executable_match
        exact += int(exact_match)
        grounded += int(citation_match)
        details.append({
            "id": case["id"],
            "exactMatch": exact_match,
            "citationMatch": citation_match,
            "jobType": result["decision"]["jobType"],
            "requestHash": result["requestHash"],
        })
    count = len(cases)
    return {
        "caseCount": count,
        "exactMatchAccuracy": exact / count if count else 0,
        "citationCoverage": grounded / count if count else 0,
        "ruleVersion": agent.retriever.rule_version,
        "corpusHash": agent.retriever.corpus_hash,
        "details": details,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("cases.jsonl"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--min-exact", type=float, default=0.95)
    parser.add_argument("--min-grounded", type=float, default=1.0)
    args = parser.parse_args()
    report = evaluate(args.cases)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return int(
        report["exactMatchAccuracy"] < args.min_exact
        or report["citationCoverage"] < args.min_grounded
    )


if __name__ == "__main__":
    raise SystemExit(main())
