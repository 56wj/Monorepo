import unittest

from job_reliability_benchmark import latency_summary, percentile


class ReliabilityBenchmarkUtilitiesTest(unittest.TestCase):
    def test_percentile_uses_nearest_rank(self):
        self.assertEqual(3, percentile([1, 2, 3, 4], 0.75))
        self.assertEqual(0.0, percentile([], 0.95))

    def test_latency_summary_converts_seconds_to_ms(self):
        summary = latency_summary([0.001, 0.002, 0.004])
        self.assertEqual(1.0, summary["min"])
        self.assertEqual(2.0, summary["p50"])
        self.assertEqual(4.0, summary["p95"])
        self.assertEqual(4.0, summary["max"])


if __name__ == "__main__":
    unittest.main()
