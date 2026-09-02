import unittest

from planning_agent.engine import PlanningAgent
from planning_agent.models import PlanningRequest


class RetrievalAndAgentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agent = PlanningAgent.from_corpus()

    def test_weight_query_returns_weight_rule_first(self):
        hits = self.agent.retriever.search("最大承重和单卷重量怎么校验", 3)
        self.assertEqual("RULE-WEIGHT-001", hits[0].document_id)

    def test_plan_is_grounded_and_executable(self):
        result = self.agent.plan(PlanningRequest(
            query="托盘装箱，最大承重1200kg，最大高度1600mm，禁止混装，优先利用率",
            trace_id="trace-12345678",
        ))
        self.assertTrue(result["decision"]["executable"])
        self.assertEqual("PALLET_FIRST", result["decision"]["jobType"])
        self.assertEqual("trace-12345678", result["traceId"])
        self.assertGreater(len(result["citations"]), 0)
        self.assertEqual(
            ["INTAKE", "RETRIEVE", "EXTRACT", "VALIDATE", "ROUTE"],
            [step["state"] for step in result["auditTrail"]],
        )

    def test_request_hash_and_idempotency_key_are_deterministic(self):
        request = PlanningRequest(
            query="最大承重1200kg，最大高度1600mm",
            order_context={"allow_mixed_batch": False},
        )
        first = self.agent.plan(request)
        second = self.agent.plan(request)
        self.assertEqual(first["requestHash"], second["requestHash"])
        self.assertEqual(first["decision"]["idempotencyKey"], second["decision"]["idempotencyKey"])

    def test_incomplete_prompt_stays_non_executable(self):
        result = self.agent.plan(PlanningRequest(query="需要悬挂装箱，禁止混装"))
        self.assertFalse(result["decision"]["executable"])
        self.assertEqual("SUSPEND_FIRST", result["decision"]["jobType"])
        self.assertEqual(["max_weight_kg", "max_height_mm"], result["missingRequiredFields"])


if __name__ == "__main__":
    unittest.main()
