import os
import unittest
from unittest.mock import patch

import requests

from worker import JobClient, LeaseLost, WorkerConfig


class FakeResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self.payload = payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


def config():
    return WorkerConfig(
        control_plane_url="http://control-plane:8101",
        worker_token="test-token",
        worker_id="worker-1",
        capabilities=["PALLET_FIRST"],
        concurrency=2,
        lease_seconds=90,
        heartbeat_seconds=20,
        max_runtime_seconds=3000,
        poll_seconds=1.0,
    )


class WorkerContractTest(unittest.TestCase):

    def test_claim_sends_capabilities_and_internal_token(self):
        job = {"jobId": "job-1", "leaseToken": "lease-1"}
        session = FakeSession([FakeResponse(200, job)])
        client = JobClient(config(), session)

        self.assertEqual(job, client.claim("worker-1-slot-0"))
        url, kwargs = session.calls[0]
        self.assertEqual(
            "http://control-plane:8101/internal/v1/jobs/claim", url
        )
        self.assertEqual("test-token", kwargs["headers"]["X-Worker-Token"])
        self.assertEqual(["PALLET_FIRST"], kwargs["json"]["capabilities"])
        self.assertEqual(90, kwargs["json"]["leaseSeconds"])

    def test_empty_queue_returns_none(self):
        client = JobClient(config(), FakeSession([FakeResponse(204)]))
        self.assertIsNone(client.claim("worker-1-slot-0"))

    def test_heartbeat_detects_lost_lease(self):
        client = JobClient(config(), FakeSession([FakeResponse(409)]))
        with self.assertRaises(LeaseLost):
            client.heartbeat({"jobId": "job-1", "leaseToken": "lease-1"})

    def test_completion_retries_an_uncertain_network_response(self):
        session = FakeSession([
            requests.ConnectionError("reset"),
            FakeResponse(204),
        ])
        client = JobClient(config(), session)
        job = {"jobId": "job-1", "leaseToken": "lease-1"}

        with patch("worker.time.sleep"):
            client.complete(job, {"result": "{}", "taskId": 1})

        self.assertEqual(2, len(session.calls))

    def test_completion_detects_lost_lease(self):
        client = JobClient(config(), FakeSession([FakeResponse(409)]))
        with self.assertRaises(LeaseLost):
            client.complete(
                {"jobId": "job-1", "leaseToken": "lease-1"},
                {"result": "{}", "taskId": 1},
            )

    def test_environment_controls_worker_parallelism(self):
        values = {
            "WORKER_CONCURRENCY": "4",
            "WORKER_CAPABILITIES": "PALLET_FIRST,SUSPEND_FIRST",
            "JOB_LEASE_SECONDS": "120",
        }
        with patch.dict(os.environ, values, clear=False):
            loaded = WorkerConfig.from_env()
        self.assertEqual(4, loaded.concurrency)
        self.assertEqual(["PALLET_FIRST", "SUSPEND_FIRST"], loaded.capabilities)
        self.assertEqual(120, loaded.lease_seconds)


if __name__ == "__main__":
    unittest.main()
