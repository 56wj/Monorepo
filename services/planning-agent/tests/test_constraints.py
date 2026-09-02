import unittest

from planning_agent.constraints import extract_constraints, job_type_for, validate_constraints


class ConstraintExtractionTest(unittest.TestCase):
    def test_extracts_and_normalizes_chinese_units(self):
        result = extract_constraints(
            "最大承重1.2吨，最大高度1.6米，纸卷直径80厘米，单卷重500kg，禁止混装，优先利用率"
        )
        self.assertEqual(1200.0, result["max_weight_kg"])
        self.assertEqual(1600.0, result["max_height_mm"])
        self.assertEqual(800.0, result["roll_diameter_mm"])
        self.assertEqual(500.0, result["roll_weight_kg"])
        self.assertFalse(result["allow_mixed_batch"])
        self.assertEqual("MAX_UTILIZATION", result["optimization_goal"])

    def test_context_is_merged_and_query_wins(self):
        result = extract_constraints(
            "最大承重900kg，允许混装",
            {"max_weight_kg": 1000, "max_height_mm": 1700, "allow_mixed_batch": False},
        )
        self.assertEqual(900.0, result["max_weight_kg"])
        self.assertEqual(1700.0, result["max_height_mm"])
        self.assertTrue(result["allow_mixed_batch"])

    def test_routes_suspend_and_second_stage(self):
        self.assertEqual("SUSPEND_FIRST", job_type_for(extract_constraints("做悬挂装箱")))
        self.assertEqual("PALLET_SECOND", job_type_for(extract_constraints("执行二次规划")))

    def test_reports_missing_and_impossible_weight(self):
        constraints = extract_constraints("最大承重400kg，最大高度1500mm，单卷重500kg")
        missing, violations, _warnings = validate_constraints(constraints)
        self.assertEqual([], missing)
        self.assertIn("roll_weight_kg exceeds max_weight_kg", violations)


if __name__ == "__main__":
    unittest.main()
