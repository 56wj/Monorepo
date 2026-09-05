#!/usr/bin/env python3
"""End-to-end reliability benchmark for the durable packing job control plane.

The benchmark seeds isolated fixture rows in MySQL, drives the real HTTP worker
contract, injects expired leases and duplicate completion requests, and exercises
the production worker's child-process timeout path.  It deliberately uses only
the Python standard library plus the worker's existing ``requests`` dependency.
"""

import argparse
import concurrent.futures
import json
import math
import multiprocessing
import os
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "services" / "solver-worker"))

import worker as solver_worker  # noqa: E402


def percentile(values: Sequence[float], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = max(0, math.ceil(quantile * len(ordered)) - 1)
    return ordered[rank]


def latency_summary(values_seconds: Sequence[float]) -> Dict[str, float]:
    values_ms = [value * 1000 for value in values_seconds]
    return {
        "min": round(min(values_ms), 3) if values_ms else 0.0,
        "p50": round(percentile(values_ms, 0.50), 3),
        "p95": round(percentile(values_ms, 0.95), 3),
        "p99": round(percentile(values_ms, 0.99), 3),
        "max": round(max(values_ms), 3) if values_ms else 0.0,
    }


class MysqlFixture:
    def __init__(self, args: argparse.Namespace):
        self.command = [
            str(args.mysql_binary),
            f"--host={args.mysql_host}",
            f"--port={args.mysql_port}",
            f"--user={args.mysql_user}",
            "--batch",
            "--skip-column-names",
            args.mysql_database,
        ]
        self.env = dict(os.environ)
        self.env["MYSQL_PWD"] = args.mysql_password

    def execute(self, sql: str) -> str:
        completed = subprocess.run(
            self.command,
            input=sql,
            text=True,
            capture_output=True,
            env=self.env,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"mysql failed: {completed.stderr.strip()}")
        return completed.stdout.strip()

    def scalar(self, sql: str) -> int:
        output = self.execute(sql)
        if not output:
            return 0
        return int(output.splitlines()[-1])

    def prepare_schema(self) -> None:
        # The production database already owns ctask.  This minimal table exists
        # only so JobResultHandler executes its real success side effect in an
        # isolated benchmark database.
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS ctask (
              id INT NOT NULL PRIMARY KEY,
              order_id VARCHAR(128) NULL,
              source_json LONGTEXT NULL,
              type VARCHAR(64) NULL,
              state VARCHAR(64) NULL,
              create_user INT NULL,
              result_json VARCHAR(1024) NULL,
              middle_json VARCHAR(1024) NULL,
              result_excel VARCHAR(1024) NULL,
              tag_middle INT NOT NULL DEFAULT 0,
              create_time DATETIME(3) NULL,
              update_time DATETIME(3) NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            CREATE TABLE IF NOT EXISTS ctask_update_audit (
              id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              task_id INT NOT NULL,
              changed_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            DROP TRIGGER IF EXISTS benchmark_ctask_update_audit;
            CREATE TRIGGER benchmark_ctask_update_audit
              AFTER UPDATE ON ctask FOR EACH ROW
              INSERT INTO ctask_update_audit(task_id) VALUES (NEW.id);
            """
        )

    def clear(self) -> None:
        self.execute(
            "DELETE FROM ctask_update_audit; DELETE FROM packing_job; DELETE FROM ctask;"
        )

    def seed_jobs(self, count: int, task_base: int, run_id: str) -> None:
        chunk_size = 250
        for offset in range(0, count, chunk_size):
            rows = range(offset, min(offset + chunk_size, count))
            tasks = []
            jobs = []
            for index in rows:
                task_id = task_base + index
                public_id = str(uuid.uuid4())
                trace_id = f"bench-{run_id}-{index}"
                key = f"bench:{run_id}:{index}"
                tasks.append(
                    f"({task_id},'ORDER-{run_id}-{index}','{{}}','托盘装箱',"
                    f"'计算中',1,NOW(3),NOW(3))"
                )
                jobs.append(
                    f"('{public_id}','{trace_id}',{task_id},'PALLET_FIRST','QUEUED',"
                    f"'{{\"benchmark\":true}}',0,0,3,NOW(3),'{key}',NOW(3),NOW(3),0)"
                )
            self.execute(
                "INSERT INTO ctask "
                "(id,order_id,source_json,type,state,create_user,create_time,update_time) VALUES "
                + ",".join(tasks)
                + "; INSERT INTO packing_job "
                "(public_id,trace_id,task_id,job_type,status,payload_json,priority,attempt,"
                "max_attempts,available_at,idempotency_key,created_at,updated_at,version) VALUES "
                + ",".join(jobs)
                + ";"
            )


class ControlPlaneClient:
    def __init__(self, base_url: str, worker_token: str, timeout: float):
        self.base_url = base_url.rstrip("/")
        self.worker_token = worker_token
        self.timeout = timeout

    def post(self, path: str, payload: Dict[str, Any]) -> Tuple[int, Any, float]:
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-Worker-Token": self.worker_token,
                "X-Trace-Id": f"bench-{uuid.uuid4().hex}",
            },
        )
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read()
                decoded = json.loads(body) if body else None
                return response.status, decoded, time.perf_counter() - started
        except urllib.error.HTTPError as error:
            body = error.read()
            try:
                decoded = json.loads(body) if body else None
            except json.JSONDecodeError:
                decoded = body.decode("utf-8", errors="replace")
            return error.code, decoded, time.perf_counter() - started

    def claim(self, worker_id: str, lease_seconds: int) -> Tuple[int, Any, float]:
        return self.post(
            "/internal/v1/jobs/claim",
            {
                "workerId": worker_id,
                "capabilities": ["PALLET_FIRST"],
                "leaseSeconds": lease_seconds,
            },
        )

    def complete(self, job: Dict[str, Any]) -> Tuple[int, Any, float]:
        return self.post(
            f"/internal/v1/jobs/{job['jobId']}/complete",
            {
                "leaseToken": job["leaseToken"],
                "output": {"result": '{"benchmark":true}'},
            },
        )

    def heartbeat_with_token(
        self, job_id: str, lease_token: str
    ) -> Tuple[int, Any, float]:
        return self.post(
            f"/internal/v1/jobs/{job_id}/heartbeat",
            {"leaseToken": lease_token},
        )


def parallel_map(
    function: Callable[[int], Any], count: int, concurrency: int
) -> List[Any]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        return list(executor.map(function, range(count)))


def claim_exactly(
    client: ControlPlaneClient,
    count: int,
    concurrency: int,
    lease_seconds: int,
    worker_prefix: str,
) -> Tuple[List[Dict[str, Any]], List[float], List[str], Dict[str, int]]:
    status_counts: Counter = Counter()
    diagnostics_lock = threading.Lock()
    transient_errors: List[str] = []
    deadline = time.perf_counter() + 30

    def invoke(index: int) -> Tuple[Optional[Dict[str, Any]], float, str]:
        started = time.perf_counter()
        while time.perf_counter() < deadline:
            status, body, _request_latency = client.claim(
                f"{worker_prefix}-{index}", lease_seconds
            )
            with diagnostics_lock:
                status_counts[str(status)] += 1
            if status == 200 and isinstance(body, dict):
                return body, time.perf_counter() - started, ""
            if status == 204:
                time.sleep(0.005)
                continue
            error = f"claim status={status} body={body!r}"
            if status >= 500:
                with diagnostics_lock:
                    transient_errors.append(error)
                time.sleep(0.02)
                continue
            return None, time.perf_counter() - started, error
        return None, time.perf_counter() - started, "claim deadline exceeded"

    results = parallel_map(invoke, count, concurrency)
    jobs = [job for job, _latency, _error in results if job is not None]
    latencies = [latency for _job, latency, _error in results]
    errors = [error for _job, _latency, error in results if error]
    return jobs, latencies, transient_errors + errors, dict(sorted(status_counts.items()))


def benchmark_claims(
    fixture: MysqlFixture,
    client: ControlPlaneClient,
    count: int,
    concurrency: int,
    lease_seconds: int,
) -> Dict[str, Any]:
    fixture.clear()
    fixture.seed_jobs(count, 100_000, f"claim-{uuid.uuid4().hex[:8]}")
    started = time.perf_counter()
    jobs, latencies, errors, status_counts = claim_exactly(
        client, count, concurrency, lease_seconds, "claim-worker"
    )
    elapsed = time.perf_counter() - started
    ids = [job["jobId"] for job in jobs]
    duplicate_claims = len(ids) - len(set(ids))
    running = fixture.scalar("SELECT COUNT(*) FROM packing_job WHERE status='RUNNING';")
    return {
        "jobCount": count,
        "concurrency": concurrency,
        "elapsedSeconds": round(elapsed, 6),
        "throughputRps": round(len(jobs) / elapsed, 3) if elapsed else 0.0,
        "claimed": len(jobs),
        "runningRows": running,
        "duplicateClaims": duplicate_claims,
        "errorCount": len(errors),
        "httpStatusCounts": status_counts,
        "successRate": round(len(jobs) / count, 6),
        "latencyMs": latency_summary(latencies),
        "sampleErrors": errors[:5],
        "passed": len(jobs) == count
        and running == count
        and duplicate_claims == 0
        and not errors,
    }


def benchmark_idempotent_completion(
    fixture: MysqlFixture,
    client: ControlPlaneClient,
    count: int,
    concurrency: int,
    lease_seconds: int,
) -> Dict[str, Any]:
    fixture.clear()
    fixture.seed_jobs(count, 200_000, f"idem-{uuid.uuid4().hex[:8]}")
    jobs, _claim_latencies, claim_errors, claim_status_counts = claim_exactly(
        client, count, concurrency, lease_seconds, "idem-worker"
    )

    requests_to_send: List[Dict[str, Any]] = []
    for job in jobs:
        requests_to_send.extend((job, job))

    started = time.perf_counter()

    def invoke(index: int) -> Tuple[int, float, str]:
        status, body, latency = client.complete(requests_to_send[index])
        error = "" if status == 204 else f"complete status={status} body={body!r}"
        return status, latency, error

    results = parallel_map(invoke, len(requests_to_send), concurrency)
    elapsed = time.perf_counter() - started
    errors = [error for _status, _latency, error in results if error]
    latencies = [latency for _status, latency, _error in results]
    succeeded = fixture.scalar("SELECT COUNT(*) FROM packing_job WHERE status='SUCCEEDED';")
    side_effects = fixture.scalar("SELECT COUNT(*) FROM ctask_update_audit;")
    duplicate_side_effects = fixture.scalar(
        "SELECT COALESCE(SUM(extra),0) FROM ("
        "SELECT GREATEST(COUNT(*)-1,0) AS extra FROM ctask_update_audit GROUP BY task_id"
        ") AS duplicate_updates;"
    )
    return {
        "logicalJobs": count,
        "completionRequests": len(requests_to_send),
        "duplicateRequestsInjected": count,
        "elapsedSeconds": round(elapsed, 6),
        "requestThroughputRps": round(len(results) / elapsed, 3) if elapsed else 0.0,
        "succeededJobs": succeeded,
        "businessSideEffects": side_effects,
        "duplicateBusinessSideEffects": duplicate_side_effects,
        "idempotentConvergenceRate": round(succeeded / count, 6) if count else 0.0,
        "errorCount": len(errors) + len(claim_errors),
        "claimHttpStatusCounts": claim_status_counts,
        "latencyMs": latency_summary(latencies),
        "sampleErrors": (claim_errors + errors)[:5],
        "passed": len(jobs) == count
        and succeeded == count
        and side_effects == count
        and duplicate_side_effects == 0
        and not claim_errors
        and not errors,
    }


def benchmark_crash_recovery(
    fixture: MysqlFixture,
    client: ControlPlaneClient,
    count: int,
    concurrency: int,
    lease_seconds: int,
) -> Dict[str, Any]:
    fixture.clear()
    fixture.seed_jobs(count, 300_000, f"recover-{uuid.uuid4().hex[:8]}")
    original_jobs, _latencies, claim_errors, claim_status_counts = claim_exactly(
        client, count, concurrency, lease_seconds, "crashed-worker"
    )
    if len(original_jobs) != count:
        return {
            "jobs": count,
            "recovered": 0,
            "errorCount": len(claim_errors),
            "claimHttpStatusCounts": claim_status_counts,
            "sampleErrors": claim_errors[:5],
            "passed": False,
        }

    failure_started = time.perf_counter()
    # The synthetic worker is now considered dead: no heartbeat or completion is
    # sent. Start polling just before lease expiry so recovery timing includes the
    # actual failure-detection window.
    time.sleep(max(0.0, lease_seconds - 0.5))
    deadline = failure_started + lease_seconds + 15

    def reclaim(index: int) -> Tuple[Optional[Dict[str, Any]], float, str]:
        while time.perf_counter() < deadline:
            status, body, _latency = client.claim(
                f"recovery-worker-{index}", lease_seconds
            )
            if status == 200 and isinstance(body, dict):
                return body, time.perf_counter() - failure_started, ""
            if status != 204:
                return None, time.perf_counter() - failure_started, (
                    f"reclaim status={status} body={body!r}"
                )
            time.sleep(0.02)
        return None, time.perf_counter() - failure_started, "reclaim deadline exceeded"

    reclaims = parallel_map(reclaim, count, concurrency)
    recovered_jobs = [job for job, _elapsed, _error in reclaims if job is not None]
    reclaim_elapsed = [elapsed for job, elapsed, _error in reclaims if job is not None]
    reclaim_errors = [error for _job, _elapsed, error in reclaims if error]

    original_tokens = {job["jobId"]: job["leaseToken"] for job in original_jobs}

    def stale_heartbeat(index: int) -> Tuple[int, float]:
        job = original_jobs[index]
        status, _body, latency = client.heartbeat_with_token(
            job["jobId"], original_tokens[job["jobId"]]
        )
        return status, latency

    stale_results = parallel_map(stale_heartbeat, len(original_jobs), concurrency)
    stale_rejected = sum(1 for status, _latency in stale_results if status == 409)
    stale_status_counts = dict(
        sorted(Counter(str(status) for status, _latency in stale_results).items())
    )

    def complete_recovered(index: int) -> Tuple[int, float, str]:
        status, body, latency = client.complete(recovered_jobs[index])
        return status, latency, "" if status == 204 else repr(body)

    completion_results = parallel_map(
        complete_recovered, len(recovered_jobs), concurrency
    )
    completion_errors = [
        f"complete status={status} body={error}"
        for status, _latency, error in completion_results
        if status != 204
    ]
    succeeded = fixture.scalar("SELECT COUNT(*) FROM packing_job WHERE status='SUCCEEDED';")
    second_attempts = fixture.scalar("SELECT COUNT(*) FROM packing_job WHERE attempt=2;")
    total_elapsed = time.perf_counter() - failure_started
    all_errors = claim_errors + reclaim_errors + completion_errors
    return {
        "jobsWithInjectedWorkerCrash": count,
        "leaseSeconds": lease_seconds,
        "recoveredAndSucceeded": succeeded,
        "secondAttemptRows": second_attempts,
        "recoverySuccessRate": round(succeeded / count, 6) if count else 0.0,
        "staleLeaseWritesAttempted": len(original_jobs),
        "staleLeaseWritesRejected": stale_rejected,
        "staleLeaseRejectionRate": round(stale_rejected / count, 6) if count else 0.0,
        "staleLeaseHttpStatusCounts": stale_status_counts,
        "failureToReclaimMs": latency_summary(reclaim_elapsed),
        "scenarioElapsedSeconds": round(total_elapsed, 6),
        "errorCount": len(all_errors),
        "initialClaimHttpStatusCounts": claim_status_counts,
        "sampleErrors": all_errors[:5],
        "passed": len(recovered_jobs) == count
        and succeeded == count
        and second_attempts == count
        and stale_rejected == count
        and not all_errors,
    }


class RecordingClient:
    def __init__(self):
        self.lock = threading.Lock()
        self.completed_at: Dict[str, float] = {}
        self.failed_at: Dict[str, float] = {}
        self.fail_codes: Dict[str, str] = {}

    def heartbeat(self, _job: Dict[str, Any]) -> None:
        return None

    def complete(self, job: Dict[str, Any], _output: Dict[str, Any]) -> None:
        with self.lock:
            self.completed_at[job["jobId"]] = time.perf_counter()

    def fail(
        self,
        job: Dict[str, Any],
        code: str,
        _message: str,
        _retryable: bool,
    ) -> None:
        with self.lock:
            self.failed_at[job["jobId"]] = time.perf_counter()
            self.fail_codes[job["jobId"]] = code


def synthetic_child_entry(
    _job_type: str, payload: Dict[str, Any], result_queue: Any
) -> None:
    if payload["behavior"] == "hang":
        time.sleep(payload.get("sleepSeconds", 60))
        return
    if payload["behavior"] == "crash":
        raise RuntimeError("synthetic child crash")
    time.sleep(payload.get("sleepSeconds", 0.01))
    result_queue.put({"ok": True, "output": {"result": "{}"}})


def benchmark_worker_isolation(total_jobs: int, concurrency: int) -> Dict[str, Any]:
    hanging_jobs = max(1, total_jobs // 5)
    client = RecordingClient()
    config = solver_worker.WorkerConfig(
        control_plane_url="http://benchmark.invalid",
        worker_token="benchmark",
        worker_id="isolation-benchmark",
        capabilities=["PALLET_FIRST"],
        concurrency=concurrency,
        lease_seconds=10,
        heartbeat_seconds=2,
        max_runtime_seconds=1,
        poll_seconds=0.1,
    )
    jobs = []
    for index in range(total_jobs):
        behavior = "hang" if index < hanging_jobs else "fast"
        jobs.append(
            {
                "jobId": f"isolation-{index}",
                "traceId": f"isolation-trace-{index}",
                "taskId": 400_000 + index,
                "jobType": "PALLET_FIRST",
                "attempt": 1,
                "leaseToken": f"isolation-token-{index}",
                "payload": {"behavior": behavior, "sleepSeconds": 60 if behavior == "hang" else 0.01},
            }
        )

    starts: Dict[str, float] = {}
    durations: Dict[str, float] = {}
    invocation_errors: List[str] = []
    children_before = {child.pid for child in multiprocessing.active_children()}

    def invoke(index: int) -> None:
        job = jobs[index]
        starts[job["jobId"]] = time.perf_counter()
        try:
            solver_worker.run_claimed_job(client, config, job)
        except Exception as error:  # Captured in the report instead of hiding a broken run.
            invocation_errors.append(f"{job['jobId']}: {error!r}")
        finally:
            durations[job["jobId"]] = time.perf_counter() - starts[job["jobId"]]

    scenario_started = time.perf_counter()
    with patch.object(solver_worker, "child_entry", synthetic_child_entry):
        parallel_map(invoke, total_jobs, concurrency)
    scenario_elapsed = time.perf_counter() - scenario_started
    time.sleep(0.2)
    orphaned = [
        child.pid
        for child in multiprocessing.active_children()
        if child.pid not in children_before
    ]

    hanging_ids = {job["jobId"] for job in jobs[:hanging_jobs]}
    healthy_ids = {job["jobId"] for job in jobs[hanging_jobs:]}
    timed_out = {
        job_id
        for job_id, code in client.fail_codes.items()
        if code == "SOLVER_TIMEOUT"
    }
    timeout_durations = [durations[job_id] for job_id in timed_out]
    healthy_durations = [
        durations[job_id] for job_id in healthy_ids if job_id in client.completed_at
    ]
    return {
        "totalJobs": total_jobs,
        "concurrency": concurrency,
        "hangingJobsInjected": hanging_jobs,
        "healthyJobs": len(healthy_ids),
        "healthyJobsSucceeded": len(healthy_ids & set(client.completed_at)),
        "hungProcessesTerminated": len(hanging_ids & timed_out),
        "orphanedChildProcesses": orphaned,
        "healthyJobLatencyMs": latency_summary(healthy_durations),
        "timeoutTerminationLatencyMs": latency_summary(timeout_durations),
        "scenarioElapsedSeconds": round(scenario_elapsed, 6),
        "errorCount": len(invocation_errors),
        "sampleErrors": invocation_errors[:5],
        "passed": healthy_ids.issubset(client.completed_at)
        and hanging_ids == timed_out
        and not orphaned
        and not invocation_errors,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--control-plane-url", default="http://127.0.0.1:18101")
    parser.add_argument("--worker-token", default="bench-token")
    parser.add_argument("--http-timeout", type=float, default=10.0)
    parser.add_argument("--mysql-binary", type=Path, default=Path("/usr/local/mysql/bin/mysql"))
    parser.add_argument("--mysql-host", default="127.0.0.1")
    parser.add_argument("--mysql-port", type=int, default=33306)
    parser.add_argument("--mysql-user", default=os.getenv("MYSQL_BENCH_USER", "root"))
    parser.add_argument(
        "--mysql-password",
        default=os.getenv("MYSQL_BENCH_PASSWORD", "local-root-change-me"),
    )
    parser.add_argument("--mysql-database", default="db_kindlead")
    parser.add_argument("--claim-jobs", type=int, default=1000)
    parser.add_argument("--idempotency-jobs", type=int, default=100)
    parser.add_argument("--recovery-jobs", type=int, default=20)
    parser.add_argument("--isolation-jobs", type=int, default=40)
    parser.add_argument("--concurrency", type=int, default=32)
    parser.add_argument("--lease-seconds", type=int, default=10)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for name in ("claim_jobs", "idempotency_jobs", "recovery_jobs", "isolation_jobs", "concurrency"):
        if getattr(args, name) < 1:
            raise SystemExit(f"--{name.replace('_', '-')} must be positive")
    if args.lease_seconds < 10:
        raise SystemExit("--lease-seconds must be at least 10 (control-plane contract)")

    fixture = MysqlFixture(args)
    fixture.prepare_schema()
    client = ControlPlaneClient(
        args.control_plane_url, args.worker_token, args.http_timeout
    )
    report = {
        "schemaVersion": 1,
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "environment": {
            "kind": "local-docker-mysql-plus-local-jvm",
            "mysql": fixture.execute("SELECT VERSION();"),
            "python": sys.version.split()[0],
            "leaseSeconds": args.lease_seconds,
            "note": (
                "Synthetic job payloads; real MySQL 8 row locks, HTTP control-plane, "
                "and production worker process-isolation path."
            ),
        },
    }
    report["concurrentClaim"] = benchmark_claims(
        fixture, client, args.claim_jobs, args.concurrency, args.lease_seconds
    )
    report["idempotentCompletion"] = benchmark_idempotent_completion(
        fixture,
        client,
        args.idempotency_jobs,
        args.concurrency,
        args.lease_seconds,
    )
    report["workerCrashRecovery"] = benchmark_crash_recovery(
        fixture,
        client,
        args.recovery_jobs,
        min(args.concurrency, args.recovery_jobs),
        args.lease_seconds,
    )
    report["processIsolation"] = benchmark_worker_isolation(
        args.isolation_jobs, min(args.concurrency, args.isolation_jobs)
    )
    checks = {
        key: value["passed"]
        for key, value in report.items()
        if isinstance(value, dict) and "passed" in value
    }
    report["verdict"] = {"passed": all(checks.values()), "checks": checks}
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if report["verdict"]["passed"] else 2


if __name__ == "__main__":
    multiprocessing.freeze_support()
    raise SystemExit(main())
