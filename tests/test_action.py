from Action import Action
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestAction(unittest.TestCase):
    def setUp(self):
        self.action = Action()

    def test_init(self):
        self.assertEqual(len(self.action.actions), 4)
        for action in ["MOVE_UP", "MOVE_DOWN", "MOVE_LEFT", "MOVE_RIGHT"]:
            self.assertIn(action, self.action.actions)

    def test_deltas(self):
        self.assertEqual(self.action.get_action_delta("MOVE_UP"), (-1, 0))
        self.assertEqual(self.action.get_action_delta("MOVE_DOWN"), (1, 0))
        self.assertEqual(self.action.get_action_delta("MOVE_LEFT"), (0, -1))
        self.assertEqual(self.action.get_action_delta("MOVE_RIGHT"), (0, 1))

    def test_delta_properties(self):
        for action in self.action.get_all_actions():
            delta = self.action.get_action_delta(action)
            self.assertIsInstance(delta, tuple)
            self.assertEqual(len(delta), 2)
            self.assertIn(delta[0], [-1, 0, 1])
            self.assertIn(delta[1], [-1, 0, 1])
            self.assertEqual(abs(delta[0]) + abs(delta[1]), 1)

    def test_invalid_actions(self):
        for action in ["INVALID", "", None, "move_up", 123]:
            self.assertFalse(self.action.is_valid_action(action))
            self.assertIsNone(self.action.get_action_delta(action))

    def test_get_all_actions(self):
        actions = self.action.get_all_actions()
        self.assertEqual(len(actions), 4)
        for a in actions:
            self.assertIsInstance(a, str)
            self.assertTrue(self.action.is_valid_action(a))

    def test_is_valid_action(self):
        valid = ["MOVE_UP", "MOVE_DOWN", "MOVE_LEFT", "MOVE_RIGHT"]
        for a in valid:
            self.assertTrue(self.action.is_valid_action(a))
        invalid = ["invalid", "", None, "move_up"]
        for a in invalid:
            self.assertFalse(self.action.is_valid_action(a))

    def test_opposite_directions(self):
        self.assertEqual(self.action.get_action_delta("MOVE_UP")[
                         0], -self.action.get_action_delta("MOVE_DOWN")[0])
        self.assertEqual(self.action.get_action_delta("MOVE_LEFT")[
                         1], -self.action.get_action_delta("MOVE_RIGHT")[1])


if __name__ == '__main__':
    unittest.main()
