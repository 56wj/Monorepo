import unittest

from load_test import evaluate_slo, percentile, summarize


class LoadTestStatisticsTest(unittest.TestCase):
    def test_percentile_uses_nearest_rank(self):
        self.assertEqual(5, percentile([1, 2, 3, 4, 5], 0.95))
        self.assertEqual(0.0, percentile([], 0.95))

    def test_summary_and_slo(self):
        report = summarize(
            [(True, 10.0, ""), (True, 20.0, ""), (False, 30.0, "boom")],
            elapsed=0.1,
            concurrency=3,
        )
        self.assertEqual(30.0, report["throughputRps"])
        self.assertEqual(1, report["errorCount"])
        verdict = evaluate_slo(report, {
            "maxErrorRate": 0.5,
            "maxP95Ms": 50,
            "maxP99Ms": 50,
            "minThroughputRps": 20,
        })
        self.assertTrue(verdict["passed"])


if __name__ == "__main__":
    unittest.main()
