import unittest

from overlap_rules import (
    can_stack_layer,
    parse_overlap_limits_cm,
    roll_width_mm_to_cm,
)


class OverlapRulesTest(unittest.TestCase):

    def test_roll_width_is_converted_from_mm_to_cm(self):
        self.assertEqual(70, roll_width_mm_to_cm(700))
        self.assertEqual(78, roll_width_mm_to_cm(780))

    def test_overlap_limits_are_required_when_enabled(self):
        with self.assertRaisesRegex(ValueError, "单层"):
            parse_overlap_limits_cm({
                "overlap": True,
                "single_max_height": "",
                "entire_max_height": "",
            })

        with self.assertRaisesRegex(ValueError, "总高度"):
            parse_overlap_limits_cm({
                "overlap": True,
                "single_max_height": 70,
                "entire_max_height": "",
            })

    def test_780_mm_roll_does_not_pass_70_cm_single_limit(self):
        self.assertFalse(can_stack_layer(
            "35*780*4000*5", "35*780*4000*5", False, False,
            roll_width_mm_to_cm(780), roll_width_mm_to_cm(780),
            roll_width_mm_to_cm(780), 70, 200,
        ))

    def test_700_mm_roll_passes_70_cm_single_limit_and_total_limit(self):
        self.assertTrue(can_stack_layer(
            "35*700*4000*5", "35*700*4000*5", False, False,
            roll_width_mm_to_cm(700), roll_width_mm_to_cm(700),
            roll_width_mm_to_cm(700), 70, 140,
        ))

    def test_total_height_limit_is_applied_to_body_height_sum(self):
        self.assertFalse(can_stack_layer(
            "35*700*4000*5", "35*700*4000*5", False, False,
            70, 70, 70, 70, 139.9,
        ))

    def test_different_or_mixed_trays_do_not_stack(self):
        self.assertFalse(can_stack_layer("A", "B", False, False, 60, 60, 60, 70, 140))
        self.assertFalse(can_stack_layer("A", "A", False, True, 60, 60, 60, 70, 140))


if __name__ == "__main__":
    unittest.main()
