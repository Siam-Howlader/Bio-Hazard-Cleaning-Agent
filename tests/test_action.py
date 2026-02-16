from Action import Action
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestAction(unittest.TestCase):
    """Test cases for the Action module."""

    def setUp(self):
        """Set up test fixtures."""
        self.action = Action()

    def tearDown(self):
        """Clean up after tests."""
        self.action = None

    # ===== Initialization Tests =====
    def test_action_initialization(self):
        """Test that Action initializes correctly."""
        self.assertIsNotNone(self.action.actions)

    def test_action_has_four_directions(self):
        """Test that Action contains four movement directions."""
        self.assertEqual(len(self.action.actions), 4)

    def test_action_has_move_up(self):
        """Test that MOVE_UP action exists."""
        self.assertIn("MOVE_UP", self.action.actions)

    def test_action_has_move_down(self):
        """Test that MOVE_DOWN action exists."""
        self.assertIn("MOVE_DOWN", self.action.actions)

    def test_action_has_move_left(self):
        """Test that MOVE_LEFT action exists."""
        self.assertIn("MOVE_LEFT", self.action.actions)

    def test_action_has_move_right(self):
        """Test that MOVE_RIGHT action exists."""
        self.assertIn("MOVE_RIGHT", self.action.actions)

    # ===== Action Delta Tests =====
    def test_move_up_delta(self):
        """Test MOVE_UP returns correct delta (-1, 0)."""
        delta = self.action.get_action_delta("MOVE_UP")
        self.assertEqual(delta, (-1, 0))

    def test_move_down_delta(self):
        """Test MOVE_DOWN returns correct delta (1, 0)."""
        delta = self.action.get_action_delta("MOVE_DOWN")
        self.assertEqual(delta, (1, 0))

    def test_move_left_delta(self):
        """Test MOVE_LEFT returns correct delta (0, -1)."""
        delta = self.action.get_action_delta("MOVE_LEFT")
        self.assertEqual(delta, (0, -1))

    def test_move_right_delta(self):
        """Test MOVE_RIGHT returns correct delta (0, 1)."""
        delta = self.action.get_action_delta("MOVE_RIGHT")
        self.assertEqual(delta, (0, 1))

    def test_delta_values_are_tuples(self):
        """Test that deltas are returned as tuples."""
        for action_name in self.action.get_all_actions():
            delta = self.action.get_action_delta(action_name)
            self.assertIsInstance(delta, tuple)

    def test_delta_tuple_length(self):
        """Test that delta tuples have length 2."""
        for action_name in self.action.get_all_actions():
            delta = self.action.get_action_delta(action_name)
            self.assertEqual(len(delta), 2)

    def test_delta_values_are_integers(self):
        """Test that delta components are integers."""
        for action_name in self.action.get_all_actions():
            delta = self.action.get_action_delta(action_name)
            self.assertIsInstance(delta[0], int)
            self.assertIsInstance(delta[1], int)

    # ===== Invalid Action Delta Tests =====
    def test_get_action_delta_invalid_action(self):
        """Test get_action_delta with invalid action name."""
        delta = self.action.get_action_delta("INVALID_ACTION")
        self.assertIsNone(delta)

    def test_get_action_delta_empty_string(self):
        """Test get_action_delta with empty string."""
        delta = self.action.get_action_delta("")
        self.assertIsNone(delta)

    def test_get_action_delta_none_input(self):
        """Test get_action_delta with None input."""
        delta = self.action.get_action_delta(None)
        self.assertIsNone(delta)

    def test_get_action_delta_case_sensitive(self):
        """Test that action names are case-sensitive."""
        # Lowercase should not match uppercase
        delta = self.action.get_action_delta("move_up")
        self.assertIsNone(delta)

    def test_get_action_delta_typo(self):
        """Test get_action_delta with typo in action name."""
        delta = self.action.get_action_delta("MOVE_UPPP")
        self.assertIsNone(delta)

    # ===== get_all_actions Tests =====
    def test_get_all_actions_returns_list(self):
        """Test that get_all_actions returns a list."""
        actions = self.action.get_all_actions()
        self.assertIsInstance(actions, list)

    def test_get_all_actions_count(self):
        """Test that get_all_actions returns all four actions."""
        actions = self.action.get_all_actions()
        self.assertEqual(len(actions), 4)

    def test_get_all_actions_contains_up(self):
        """Test that get_all_actions includes MOVE_UP."""
        actions = self.action.get_all_actions()
        self.assertIn("MOVE_UP", actions)

    def test_get_all_actions_contains_down(self):
        """Test that get_all_actions includes MOVE_DOWN."""
        actions = self.action.get_all_actions()
        self.assertIn("MOVE_DOWN", actions)

    def test_get_all_actions_contains_left(self):
        """Test that get_all_actions includes MOVE_LEFT."""
        actions = self.action.get_all_actions()
        self.assertIn("MOVE_LEFT", actions)

    def test_get_all_actions_contains_right(self):
        """Test that get_all_actions includes MOVE_RIGHT."""
        actions = self.action.get_all_actions()
        self.assertIn("MOVE_RIGHT", actions)

    def test_get_all_actions_no_duplicates(self):
        """Test that get_all_actions has no duplicate actions."""
        actions = self.action.get_all_actions()
        unique_actions = set(actions)
        self.assertEqual(len(actions), len(unique_actions))

    def test_get_all_actions_returns_strings(self):
        """Test that all actions are strings."""
        actions = self.action.get_all_actions()
        for action in actions:
            self.assertIsInstance(action, str)

    def test_get_all_actions_returns_copy(self):
        """Test that get_all_actions returns a list (not reference to internal)."""
        actions1 = self.action.get_all_actions()
        actions1.append("FAKE_ACTION")
        actions2 = self.action.get_all_actions()
        self.assertNotEqual(len(actions1), len(actions2))

    # ===== is_valid_action Tests =====
    def test_is_valid_action_move_up(self):
        """Test is_valid_action with MOVE_UP."""
        self.assertTrue(self.action.is_valid_action("MOVE_UP"))

    def test_is_valid_action_move_down(self):
        """Test is_valid_action with MOVE_DOWN."""
        self.assertTrue(self.action.is_valid_action("MOVE_DOWN"))

    def test_is_valid_action_move_left(self):
        """Test is_valid_action with MOVE_LEFT."""
        self.assertTrue(self.action.is_valid_action("MOVE_LEFT"))

    def test_is_valid_action_move_right(self):
        """Test is_valid_action with MOVE_RIGHT."""
        self.assertTrue(self.action.is_valid_action("MOVE_RIGHT"))

    def test_is_valid_action_all_valid(self):
        """Test is_valid_action for all valid actions."""
        valid_actions = ["MOVE_UP", "MOVE_DOWN", "MOVE_LEFT", "MOVE_RIGHT"]
        for action in valid_actions:
            self.assertTrue(self.action.is_valid_action(action))

    def test_is_valid_action_invalid_action(self):
        """Test is_valid_action with invalid action."""
        self.assertFalse(self.action.is_valid_action("INVALID_ACTION"))

    def test_is_valid_action_empty_string(self):
        """Test is_valid_action with empty string."""
        self.assertFalse(self.action.is_valid_action(""))

    def test_is_valid_action_none(self):
        """Test is_valid_action with None."""
        self.assertFalse(self.action.is_valid_action(None))

    def test_is_valid_action_case_sensitive(self):
        """Test that is_valid_action is case-sensitive."""
        self.assertFalse(self.action.is_valid_action("move_up"))
        self.assertFalse(self.action.is_valid_action("Move_Up"))

    def test_is_valid_action_partial_match(self):
        """Test is_valid_action with partial match."""
        self.assertFalse(self.action.is_valid_action("MOVE"))
        self.assertFalse(self.action.is_valid_action("UP"))

    def test_is_valid_action_typo(self):
        """Test is_valid_action with typo."""
        self.assertFalse(self.action.is_valid_action("MOVE_UPPP"))
        self.assertFalse(self.action.is_valid_action("MOVE_DOWWN"))

    def test_is_valid_action_special_characters(self):
        """Test is_valid_action with special characters."""
        self.assertFalse(self.action.is_valid_action("MOVE_UP!"))
        self.assertFalse(self.action.is_valid_action("@MOVE_DOWN"))

    def test_is_valid_action_whitespace(self):
        """Test is_valid_action with whitespace."""
        self.assertFalse(self.action.is_valid_action(" MOVE_UP"))
        self.assertFalse(self.action.is_valid_action("MOVE_UP "))
        self.assertFalse(self.action.is_valid_action("MOVE UP"))

    # ===== Boundary Value Analysis =====
    def test_action_delta_components_range(self):
        """Test that delta components are within expected range."""
        for action_name in self.action.get_all_actions():
            delta = self.action.get_action_delta(action_name)
            # Each component should be -1, 0, or 1
            self.assertIn(delta[0], [-1, 0, 1])
            self.assertIn(delta[1], [-1, 0, 1])

    def test_action_delta_exactly_one_component_changed(self):
        """Test that each action changes exactly one coordinate."""
        for action_name in self.action.get_all_actions():
            delta = self.action.get_action_delta(action_name)
            # Sum of absolute values should be 1
            magnitude = abs(delta[0]) + abs(delta[1])
            self.assertEqual(magnitude, 1)

    def test_action_delta_no_diagonal_movement(self):
        """Test that no action produces diagonal movement."""
        for action_name in self.action.get_all_actions():
            delta = self.action.get_action_delta(action_name)
            # Either row change is 0 or column change is 0
            is_horizontal = delta[0] == 0
            is_vertical = delta[1] == 0
            self.assertTrue(is_horizontal or is_vertical)

    # ===== Opposite Actions Tests =====
    def test_move_up_down_are_opposite(self):
        """Test that MOVE_UP and MOVE_DOWN are opposite."""
        up = self.action.get_action_delta("MOVE_UP")
        down = self.action.get_action_delta("MOVE_DOWN")
        self.assertEqual(up[0], -down[0])

    def test_move_left_right_are_opposite(self):
        """Test that MOVE_LEFT and MOVE_RIGHT are opposite."""
        left = self.action.get_action_delta("MOVE_LEFT")
        right = self.action.get_action_delta("MOVE_RIGHT")
        self.assertEqual(left[1], -right[1])

    # ===== Equivalence Partitioning Tests =====
    def test_valid_action_partition(self):
        """Test valid action equivalence partition."""
        valid_actions = ["MOVE_UP", "MOVE_DOWN", "MOVE_LEFT", "MOVE_RIGHT"]
        for action in valid_actions:
            self.assertTrue(self.action.is_valid_action(action))
            self.assertIsNotNone(self.action.get_action_delta(action))

    def test_invalid_action_partition(self):
        """Test invalid action equivalence partition."""
        invalid_actions = ["INVALID", "", None, "move_up", "MOVE", "UP", 123]
        for action in invalid_actions:
            self.assertFalse(self.action.is_valid_action(action))
            self.assertIsNone(self.action.get_action_delta(action))

    # ===== Consistency Tests =====
    def test_get_all_actions_matches_delta_availability(self):
        """Test that all returned actions have deltas."""
        actions = self.action.get_all_actions()
        for action in actions:
            delta = self.action.get_action_delta(action)
            self.assertIsNotNone(delta)

    def test_get_all_actions_matches_valid_action_check(self):
        """Test that all returned actions are valid."""
        actions = self.action.get_all_actions()
        for action in actions:
            self.assertTrue(self.action.is_valid_action(action))

    def test_all_valid_actions_in_returned_list(self):
        """Test that all valid actions are in get_all_actions result."""
        actions = self.action.get_all_actions()
        # Verify known valid actions are present
        known_valid = ["MOVE_UP", "MOVE_DOWN", "MOVE_LEFT", "MOVE_RIGHT"]
        for action in known_valid:
            self.assertIn(action, actions)


if __name__ == '__main__':
    unittest.main()
