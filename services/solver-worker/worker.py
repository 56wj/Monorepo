import logging
import multiprocessing
import os
import queue
import random
import signal
import socket
import threading
import time
import traceback
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


LOG = logging.getLogger("solver-worker")
STOP_EVENT = threading.Event()


class LeaseLost(RuntimeError):
    pass


class CompletionUncertain(RuntimeError):
    pass


@dataclass(frozen=True)
class WorkerConfig:
    control_plane_url: str
    worker_token: str
    worker_id: str
    capabilities: List[str]
    concurrency: int
    lease_seconds: int
    heartbeat_seconds: int
    max_runtime_seconds: int
    poll_seconds: float

    @staticmethod
    def from_env() -> "WorkerConfig":
        capabilities = [
            value.strip()
            for value in os.getenv(
                "WORKER_CAPABILITIES",
                "PALLET_FIRST,PALLET_SECOND,SUSPEND_FIRST",
            ).split(",")
            if value.strip()
        ]
        return WorkerConfig(
            control_plane_url=os.getenv(
                "INTERNAL_API_BASE_URL", "http://localhost:8101"
            ).rstrip("/"),
            worker_token=os.getenv("JOB_WORKER_TOKEN", "local-dev-worker-token"),
            worker_id=os.getenv("WORKER_ID", f"{socket.gethostname()}-{os.getpid()}"),
            capabilities=capabilities,
            concurrency=max(1, int(os.getenv("WORKER_CONCURRENCY", "1"))),
            lease_seconds=max(10, int(os.getenv("JOB_LEASE_SECONDS", "90"))),
            heartbeat_seconds=max(2, int(os.getenv("JOB_HEARTBEAT_SECONDS", "20"))),
            max_runtime_seconds=max(1, int(os.getenv("JOB_MAX_RUNTIME_SECONDS", "3000"))),
            poll_seconds=max(0.1, float(os.getenv("JOB_POLL_SECONDS", "1.0"))),
        )


class JobClient:
    def __init__(self, config: WorkerConfig, session: Optional[requests.Session] = None):
        self.config = config
        self.session = session or requests.Session()
        self.headers = {"X-Worker-Token": config.worker_token}

    def claim(self, worker_id: str) -> Optional[Dict[str, Any]]:
        response = self.session.post(
            f"{self.config.control_plane_url}/internal/v1/jobs/claim",
            headers=self.headers,
            json={
                "workerId": worker_id,
                "capabilities": self.config.capabilities,
                "leaseSeconds": self.config.lease_seconds,
            },
            timeout=(3, 30),
        )
        if response.status_code == 204:
            return None
        response.raise_for_status()
        return response.json()

    def heartbeat(self, job: Dict[str, Any]) -> None:
        response = self.session.post(
            self._job_url(job, "heartbeat"),
            headers=self.headers,
            json={"leaseToken": job["leaseToken"]},
            timeout=(3, 10),
        )
        if response.status_code == 409:
            raise LeaseLost(f"lease lost for job {job['jobId']}")
        response.raise_for_status()

    def complete(self, job: Dict[str, Any], output: Dict[str, Any]) -> None:
        last_error = None
        for attempt in range(3):
            try:
                response = self.session.post(
                    self._job_url(job, "complete"),
                    headers=self.headers,
                    json={"leaseToken": job["leaseToken"], "output": output},
                    timeout=(3, 30),
                )
                if response.status_code == 409:
                    raise LeaseLost(f"lease lost while completing job {job['jobId']}")
                response.raise_for_status()
                return
            except LeaseLost:
                raise
            except requests.RequestException as error:
                last_error = error
                if attempt < 2:
                    time.sleep(1 << attempt)
        raise CompletionUncertain(
            f"completion acknowledgement is uncertain for job {job['jobId']}: {last_error}"
        )

    def fail(self, job: Dict[str, Any], code: str, message: str, retryable: bool) -> None:
        response = self.session.post(
            self._job_url(job, "fail"),
            headers=self.headers,
            json={
                "leaseToken": job["leaseToken"],
                "errorCode": code,
                "errorMessage": message[:1000],
                "retryable": retryable,
            },
            timeout=(3, 30),
        )
        if response.status_code == 409:
            raise LeaseLost(f"lease lost while failing job {job['jobId']}")
        response.raise_for_status()

    def _job_url(self, job: Dict[str, Any], action: str) -> str:
        return (
            f"{self.config.control_plane_url}/internal/v1/jobs/"
            f"{job['jobId']}/{action}"
        )


def execute_solver(job_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    # Heavy scientific dependencies are imported only inside the child process.
    from api_test import task_to_run1, task_to_run2, task_to_run3

    handlers = {
        "PALLET_FIRST": task_to_run1,
        "PALLET_SECOND": task_to_run2,
        "SUSPEND_FIRST": task_to_run3,
    }
    if job_type not in handlers:
        raise ValueError(f"unsupported job type: {job_type}")
    output = handlers[job_type](payload)
    if not isinstance(output, dict) or "result" not in output:
        raise RuntimeError("solver returned an invalid output contract")
    return output


def child_entry(job_type: str, payload: Dict[str, Any], result_queue) -> None:
    try:
        result_queue.put({"ok": True, "output": execute_solver(job_type, payload)})
    except BaseException as error:
        result_queue.put(
            {
                "ok": False,
                "errorType": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(limit=30),
            }
        )


def run_claimed_job(client: JobClient, config: WorkerConfig, job: Dict[str, Any]) -> None:
    result_queue = multiprocessing.Queue(maxsize=1)
    process = multiprocessing.Process(
        target=child_entry,
        args=(job["jobType"], job["payload"], result_queue),
        name=f"solver-{job['jobId'][:8]}",
    )
    process.start()
    started_at = time.monotonic()
    last_heartbeat_success = started_at
    next_heartbeat_at = started_at + config.heartbeat_seconds
    child_result = None

    try:
        while child_result is None:
            try:
                # Read while the child is alive. Waiting for process exit first can
                # deadlock when a large solver result fills the multiprocessing pipe.
                child_result = result_queue.get(timeout=0.5)
                break
            except queue.Empty:
                pass

            if STOP_EVENT.is_set():
                raise InterruptedError("worker shutdown requested")

            if not process.is_alive():
                try:
                    child_result = result_queue.get(timeout=2)
                    break
                except queue.Empty:
                    raise RuntimeError(
                        f"solver exited with code {process.exitcode} without output"
                    )

            now = time.monotonic()
            if now - started_at >= config.max_runtime_seconds:
                raise TimeoutError(
                    f"solver exceeded {config.max_runtime_seconds} seconds"
                )
            if now >= next_heartbeat_at:
                try:
                    client.heartbeat(job)
                    last_heartbeat_success = now
                    next_heartbeat_at = now + config.heartbeat_seconds
                except requests.RequestException as error:
                    LOG.warning(
                        "heartbeat_failed job_id=%s error=%s", job["jobId"], error
                    )
                    next_heartbeat_at = now + min(5, config.heartbeat_seconds)
                    if now - last_heartbeat_success >= config.lease_seconds - 2:
                        raise LeaseLost(
                            f"heartbeat unavailable until lease deadline for {job['jobId']}"
                        )
        process.join(timeout=2)
        if process.is_alive():
            terminate_process(process)

        if child_result.get("ok"):
            client.complete(job, child_result["output"])
            LOG.info(
                "job_succeeded job_id=%s type=%s attempt=%s duration_ms=%d",
                job["jobId"],
                job["jobType"],
                job["attempt"],
                int((time.monotonic() - started_at) * 1000),
            )
            return

        message = child_result.get("error") or "solver child failed"
        LOG.error(
            "job_failed job_id=%s type=%s error_type=%s error=%s\n%s",
            job["jobId"],
            job["jobType"],
            child_result.get("errorType"),
            message,
            child_result.get("traceback", ""),
        )
        client.fail(job, child_result.get("errorType", "SOLVER_ERROR"), message, True)
    except LeaseLost:
        terminate_process(process)
        raise
    except CompletionUncertain:
        # The control plane may already have committed success. Leave the lease
        # untouched; the idempotent complete endpoint or lease reaper resolves it.
        raise
    except InterruptedError as error:
        terminate_process(process)
        if not STOP_EVENT.is_set():
            client.fail(job, "WORKER_INTERRUPTED", str(error), True)
    except TimeoutError as error:
        terminate_process(process)
        client.fail(job, "SOLVER_TIMEOUT", str(error), True)
    except Exception as error:
        terminate_process(process)
        client.fail(job, type(error).__name__, str(error), True)
        raise
    finally:
        result_queue.close()


def terminate_process(process: multiprocessing.Process) -> None:
    if process.is_alive():
        process.terminate()
        process.join(timeout=5)
    if process.is_alive() and hasattr(process, "kill"):
        process.kill()
        process.join(timeout=2)


def worker_loop(config: WorkerConfig, slot: int) -> None:
    worker_id = f"{config.worker_id}-slot-{slot}"
    client = JobClient(config)
    while not STOP_EVENT.is_set():
        try:
            job = client.claim(worker_id)
            if job is None:
                STOP_EVENT.wait(config.poll_seconds + random.uniform(0, 0.25))
                continue
            LOG.info(
                "job_claimed job_id=%s task_id=%s type=%s attempt=%s worker=%s",
                job["jobId"],
                job["taskId"],
                job["jobType"],
                job["attempt"],
                worker_id,
            )
            run_claimed_job(client, config, job)
        except LeaseLost as error:
            LOG.warning("%s", error)
        except requests.RequestException as error:
            LOG.warning("control_plane_unavailable worker=%s error=%s", worker_id, error)
            STOP_EVENT.wait(min(5.0, config.poll_seconds * 2))
        except Exception:
            LOG.exception("worker_iteration_failed worker=%s", worker_id)
            STOP_EVENT.wait(1.0)


def request_shutdown(signum, _frame) -> None:
    LOG.info("shutdown_requested signal=%s", signum)
    STOP_EVENT.set()


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    config = WorkerConfig.from_env()
    signal.signal(signal.SIGTERM, request_shutdown)
    signal.signal(signal.SIGINT, request_shutdown)
    LOG.info(
        "worker_started worker_id=%s concurrency=%d capabilities=%s",
        config.worker_id,
        config.concurrency,
        ",".join(config.capabilities),
    )

    threads = [
        threading.Thread(
            target=worker_loop,
            args=(config, slot),
            name=f"worker-slot-{slot}",
            daemon=False,
        )
        for slot in range(config.concurrency)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
