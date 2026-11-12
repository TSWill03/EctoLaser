import unittest

from host.ectolaser_bridge import (
    TARGET_CLASS,
    command_for_predictions,
    focus_found,
    send_to_arduino,
)


class BridgeDecisionTests(unittest.TestCase):
    def test_detects_only_valid_cluster(self):
        self.assertTrue(focus_found([(TARGET_CLASS, 0.9)]))

    def test_ignores_other_classes(self):
        self.assertFalse(focus_found([("seed_head", 0.99)]))
        self.assertFalse(focus_found([("tick", 0.99)]))

    def test_respects_threshold(self):
        self.assertFalse(focus_found([(TARGET_CLASS, 0.6)], 0.65))
        self.assertTrue(focus_found([(TARGET_CLASS, 0.65)], 0.65))

    def test_empty_is_clear(self):
        self.assertEqual(command_for_predictions([]), "CLEAR")

    def test_positive_is_indicator_only(self):
        self.assertEqual(
            command_for_predictions([(TARGET_CLASS, 0.8)]), "INDICATE"
        )

    def test_invalid_threshold_is_rejected(self):
        for value in [-0.2, 1.1]:
            with self.assertRaises(ValueError):
                focus_found([], value)

    def test_disallows_hazardous_serial_commands(self):
        with self.assertRaises(ValueError):
            send_to_arduino("COM5", "LASER ON")


if __name__ == "__main__":
    unittest.main()
