#!/usr/bin/env python3
import argparse
import concurrent.futures
import json
import math
import sys
import time
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "services" / "planning-agent"))

from planning_agent.engine import PlanningAgent  # noqa: E402
from planning_agent.models import PlanningRequest  # noqa: E402


PAYLOADS = [
    {"query": "托盘装箱，最大承重1200kg，最大高度1600mm，禁止混装，优先利用率"},
    {"query": "悬挂装箱，最大承重900kg，最大高度1800mm，纸卷直径800mm"},
    {"query": "最大承重400kg，最大高度1500mm，单卷重500kg"},
]


def percentile(values: List[float], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = max(0, math.ceil(quantile * len(ordered)) - 1)
    return ordered[rank]


def summarize(results: List[Tuple[bool, float, str]], elapsed: float, concurrency: int) -> Dict[str, Any]:
    latencies = [latency for _ok, latency, _error in results]
    errors = [error for ok, _latency, error in results if not ok]
    count = len(results)
    return {
        "requestCount": count,
        "concurrency": concurrency,
        "elapsedSeconds": round(elapsed, 6),
        "throughputRps": round(count / elapsed, 3) if elapsed else 0,
        "errorCount": len(errors),
        "errorRate": round(len(errors) / count, 6) if count else 0,
        "latencyMs": {
            "min": round(min(latencies), 3) if latencies else 0,
            "p50": round(percentile(latencies, 0.50), 3),
            "p95": round(percentile(latencies, 0.95), 3),
            "p99": round(percentile(latencies, 0.99), 3),
            "max": round(max(latencies), 3) if latencies else 0,
        },
        "sampleErrors": errors[:5],
    }


def evaluate_slo(report: Dict[str, Any], thresholds: Dict[str, float]) -> Dict[str, Any]:
    checks = {
        "errorRate": report["errorRate"] <= thresholds["maxErrorRate"],
        "p95": report["latencyMs"]["p95"] <= thresholds["maxP95Ms"],
        "p99": report["latencyMs"]["p99"] <= thresholds["maxP99Ms"],
        "throughput": report["throughputRps"] >= thresholds["minThroughputRps"],
    }
    return {"passed": all(checks.values()), "checks": checks, "thresholds": thresholds}


def inprocess_callable() -> Callable[[int], Tuple[bool, float, str]]:
    agent = PlanningAgent.from_corpus()

    def invoke(index: int) -> Tuple[bool, float, str]:
        started = time.perf_counter()
        try:
            payload = PAYLOADS[index % len(PAYLOADS)]
            result = agent.plan(PlanningRequest(query=payload["query"]))
            ok = bool(result["citations"] and result["auditTrail"])
            return ok, (time.perf_counter() - started) * 1000, "" if ok else "invalid result"
        except Exception as error:
            return False, (time.perf_counter() - started) * 1000, repr(error)

    return invoke


def http_callable(url: str, timeout: float) -> Callable[[int], Tuple[bool, float, str]]:
    def invoke(index: int) -> Tuple[bool, float, str]:
        body = json.dumps(PAYLOADS[index % len(PAYLOADS)], ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-Trace-Id": f"bench-{uuid.uuid4().hex}",
            },
        )
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                result = json.loads(response.read())
                ok = response.status == 200 and bool(result.get("citations"))
                return ok, (time.perf_counter() - started) * 1000, "" if ok else "invalid response"
        except Exception as error:
            return False, (time.perf_counter() - started) * 1000, repr(error)

    return invoke


def run(invoke: Callable[[int], Tuple[bool, float, str]], count: int, concurrency: int) -> Dict[str, Any]:
    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        results = list(executor.map(invoke, range(count)))
    return summarize(results, time.perf_counter() - started, concurrency)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("inprocess", "http"), default="inprocess")
    parser.add_argument("--url", default="http://localhost:8200/v1/plans")
    parser.add_argument("--requests", type=int, default=1000)
    parser.add_argument("--concurrency", type=int, default=32)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--slo", type=Path, default=Path(__file__).with_name("slo.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.requests < 1 or args.concurrency < 1:
        parser.error("requests and concurrency must be positive")

    invoke = inprocess_callable() if args.mode == "inprocess" else http_callable(args.url, args.timeout)
    report = run(invoke, args.requests, args.concurrency)
    thresholds = json.loads(args.slo.read_text(encoding="utf-8"))["planningAgent"]
    report.update({"mode": args.mode, "slo": evaluate_slo(report, thresholds)})
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if report["slo"]["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
