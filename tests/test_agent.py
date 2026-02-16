from Agent import Agent
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestAgent(unittest.TestCase):
    """Test cases for the Agent module."""

    def setUp(self):
        """Set up test fixtures."""
        self.start_pos_1 = (5, 5)
        self.start_pos_2 = (0, 0)
        self.start_pos_3 = (50, 50)
        self.agent_1 = Agent(self.start_pos_1)
        self.agent_2 = Agent(self.start_pos_2)
        self.agent_3 = Agent(self.start_pos_3)

    def tearDown(self):
        """Clean up after tests."""
        self.agent_1 = None
        self.agent_2 = None
        self.agent_3 = None

    # ===== Initialization Tests =====
    def test_agent_initialization_position(self):
        """Test that agent initializes with correct starting position."""
        self.assertEqual(self.agent_1.current_position, self.start_pos_1)

    def test_agent_initialization_active_state(self):
        """Test that agent initializes in active state."""
        self.assertTrue(self.agent_1.active)

    def test_agent_initialization_stop_reason(self):
        """Test that agent initializes with None stop reason."""
        self.assertIsNone(self.agent_1.stop_reason)

    def test_agent_initialization_steps_count(self):
        """Test that agent initializes with zero steps."""
        self.assertEqual(self.agent_1.steps_taken, 0)

    def test_agent_initialization_waste_collected(self):
        """Test that agent initializes with zero waste collected."""
        self.assertEqual(self.agent_1.waste_collected, 0)

    def test_agent_initialization_visited_positions(self):
        """Test that starting position is marked as visited."""
        self.assertIn(self.start_pos_1, self.agent_1.visited_positions)

    def test_agent_initialization_path(self):
        """Test that path contains starting position."""
        self.assertEqual(self.agent_1.path[0], self.start_pos_1)
        self.assertEqual(len(self.agent_1.path), 1)

    def test_agent_initialization_visited_set_type(self):
        """Test that visited_positions is a set."""
        self.assertIsInstance(self.agent_1.visited_positions, set)

    def test_agent_initialization_path_list_type(self):
        """Test that path is a list."""
        self.assertIsInstance(self.agent_1.path, list)

    # ===== Position Update Tests =====
    def test_update_position_changes_current_position(self):
        """Test that update_position changes current position."""
        new_pos = (6, 6)
        self.agent_1.update_position(new_pos)
        self.assertEqual(self.agent_1.current_position, new_pos)

    def test_update_position_increments_steps(self):
        """Test that update_position increments step counter."""
        initial_steps = self.agent_1.steps_taken
        self.agent_1.update_position((6, 6))
        self.assertEqual(self.agent_1.steps_taken, initial_steps + 1)

    def test_update_position_multiple_increments(self):
        """Test multiple position updates increment steps correctly."""
        self.agent_1.update_position((6, 6))
        self.agent_1.update_position((7, 7))
        self.agent_1.update_position((8, 8))
        self.assertEqual(self.agent_1.steps_taken, 3)

    def test_update_position_adds_to_visited(self):
        """Test that new position is added to visited set."""
        new_pos = (10, 10)
        self.agent_1.update_position(new_pos)
        self.assertIn(new_pos, self.agent_1.visited_positions)

    def test_update_position_adds_to_path(self):
        """Test that new position is added to path."""
        new_pos = (10, 10)
        self.agent_1.update_position(new_pos)
        self.assertIn(new_pos, self.agent_1.path)

    def test_update_position_maintains_path_order(self):
        """Test that path maintains insertion order."""
        self.agent_1.update_position((6, 6))
        self.agent_1.update_position((7, 7))
        self.agent_1.update_position((8, 8))
        expected_path = [self.start_pos_1, (6, 6), (7, 7), (8, 8)]
        self.assertEqual(self.agent_1.path, expected_path)

    # ===== Waste Collection Tests =====
    def test_collect_waste_increments_count(self):
        """Test that collect_waste increments waste counter."""
        initial_waste = self.agent_1.waste_collected
        self.agent_1.collect_waste()
        self.assertEqual(self.agent_1.waste_collected, initial_waste + 1)

    def test_collect_waste_multiple_times(self):
        """Test collecting waste multiple times."""
        for _ in range(5):
            self.agent_1.collect_waste()
        self.assertEqual(self.agent_1.waste_collected, 5)

    def test_collect_waste_large_count(self):
        """Test collecting large amount of waste."""
        for _ in range(100):
            self.agent_1.collect_waste()
        self.assertEqual(self.agent_1.waste_collected, 100)

    def test_collect_waste_independent_from_steps(self):
        """Test that waste collection is independent from movement."""
        self.agent_1.update_position((6, 6))
        self.agent_1.collect_waste()
        # Steps should be 1, waste should be 1
        self.assertEqual(self.agent_1.steps_taken, 1)
        self.assertEqual(self.agent_1.waste_collected, 1)

    # ===== Termination Tests =====
    def test_stop_changes_active_state(self):
        """Test that stop changes active to False."""
        self.agent_1.stop("Test reason")
        self.assertFalse(self.agent_1.active)

    def test_stop_sets_stop_reason(self):
        """Test that stop sets the stop reason."""
        reason = "No valid moves"
        self.agent_1.stop(reason)
        self.assertEqual(self.agent_1.stop_reason, reason)

    def test_stop_different_reasons(self):
        """Test stop with different reason strings."""
        reasons = ["No valid moves", "Hit border", "Task completed", "Timeout"]
        for i, reason in enumerate(reasons):
            agent = Agent((i, i))
            agent.stop(reason)
            self.assertEqual(agent.stop_reason, reason)

    def test_stop_once_set_remains(self):
        """Test that once stopped, agent remains stopped."""
        self.agent_1.stop("First reason")
        self.assertFalse(self.agent_1.active)
        # Try to update position (though in real usage shouldn't happen)
        # State should remain unchanged
        self.assertFalse(self.agent_1.active)

    # ===== has_visited Tests =====
    def test_has_visited_starting_position(self):
        """Test has_visited returns True for starting position."""
        self.assertTrue(self.agent_1.has_visited(self.start_pos_1))

    def test_has_visited_after_movement(self):
        """Test has_visited returns True after move."""
        new_pos = (7, 7)
        self.agent_1.update_position(new_pos)
        self.assertTrue(self.agent_1.has_visited(new_pos))

    def test_has_visited_unvisited_position(self):
        """Test has_visited returns False for unvisited position."""
        self.assertFalse(self.agent_1.has_visited((99, 99)))

    def test_has_visited_multiple_positions(self):
        """Test has_visited with multiple positions."""
        positions = [(6, 6), (7, 7), (8, 8)]
        for pos in positions:
            self.agent_1.update_position(pos)

        for pos in positions:
            self.assertTrue(self.agent_1.has_visited(pos))

    # ===== Getter Methods Tests =====
    def test_get_current_position(self):
        """Test get_current_position returns correct position."""
        self.assertEqual(self.agent_1.get_current_position(), self.start_pos_1)
        self.agent_1.update_position((10, 10))
        self.assertEqual(self.agent_1.get_current_position(), (10, 10))

    def test_get_path_contains_start(self):
        """Test get_path contains starting position."""
        path = self.agent_1.get_path()
        self.assertEqual(path[0], self.start_pos_1)

    def test_get_path_correct_length(self):
        """Test get_path returns correct path length."""
        self.agent_1.update_position((6, 6))
        self.agent_1.update_position((7, 7))
        path = self.agent_1.get_path()
        self.assertEqual(len(path), 3)

    def test_get_path_returns_copy(self):
        """Test that get_path returns a copy, not reference."""
        path1 = self.agent_1.get_path()
        path1.append((999, 999))
        path2 = self.agent_1.get_path()
        self.assertNotEqual(path1, path2)

    def test_get_path_maintains_order(self):
        """Test that get_path maintains insertion order."""
        positions = [(6, 6), (7, 7), (8, 8)]
        for pos in positions:
            self.agent_1.update_position(pos)

        path = self.agent_1.get_path()
        expected = [self.start_pos_1] + positions
        self.assertEqual(path, expected)

    # ===== Statistics Tests =====
    def test_get_statistics_returns_dict(self):
        """Test get_statistics returns a dictionary."""
        stats = self.agent_1.get_statistics()
        self.assertIsInstance(stats, dict)

    def test_get_statistics_has_required_keys(self):
        """Test that statistics dict has all required keys."""
        stats = self.agent_1.get_statistics()
        self.assertIn("steps_taken", stats)
        self.assertIn("waste_collected", stats)
        self.assertIn("stop_reason", stats)

    def test_get_statistics_initial_values(self):
        """Test statistics initial values."""
        stats = self.agent_1.get_statistics()
        self.assertEqual(stats["steps_taken"], 0)
        self.assertEqual(stats["waste_collected"], 0)
        self.assertIsNone(stats["stop_reason"])

    def test_get_statistics_after_movement(self):
        """Test statistics after movement."""
        self.agent_1.update_position((6, 6))
        stats = self.agent_1.get_statistics()
        self.assertEqual(stats["steps_taken"], 1)

    def test_get_statistics_after_collection(self):
        """Test statistics after waste collection."""
        self.agent_1.collect_waste()
        stats = self.agent_1.get_statistics()
        self.assertEqual(stats["waste_collected"], 1)

    def test_get_statistics_after_stop(self):
        """Test statistics after stopping."""
        reason = "Test stop"
        self.agent_1.stop(reason)
        stats = self.agent_1.get_statistics()
        self.assertEqual(stats["stop_reason"], reason)

    def test_get_statistics_combined(self):
        """Test statistics with multiple operations."""
        self.agent_1.update_position((6, 6))
        self.agent_1.collect_waste()
        self.agent_1.update_position((7, 7))
        self.agent_1.collect_waste()
        self.agent_1.collect_waste()
        self.agent_1.stop("Completed")

        stats = self.agent_1.get_statistics()
        self.assertEqual(stats["steps_taken"], 2)
        self.assertEqual(stats["waste_collected"], 3)
        self.assertEqual(stats["stop_reason"], "Completed")

    # ===== Boundary Value Analysis =====
    def test_agent_with_zero_position(self):
        """Test agent initialization with zero coordinates."""
        agent = Agent((0, 0))
        self.assertEqual(agent.current_position, (0, 0))

    def test_agent_with_large_position(self):
        """Test agent initialization with large coordinates."""
        agent = Agent((9999, 9999))
        self.assertEqual(agent.current_position, (9999, 9999))

    def test_agent_with_negative_position(self):
        """Test agent initialization with negative coordinates (edge case)."""
        agent = Agent((-10, -10))
        self.assertEqual(agent.current_position, (-10, -10))

    # ===== State Consistency Tests =====
    def test_visited_positions_represents_path_uniqueness(self):
        """Test that visited_positions set has same length as unique path elements."""
        positions = [(6, 6), (7, 7), (8, 8), (6, 6), (7, 7)]
        for pos in positions:
            self.agent_1.update_position(pos)

        # Visited set should have unique positions only
        # Path may be longer due to revisits in real scenario
        unique_path = set(self.agent_1.path)
        self.assertEqual(len(self.agent_1.visited_positions), len(unique_path))

    def test_steps_equals_path_length_minus_one(self):
        """Test that steps_taken equals number of movements."""
        for i in range(5):
            self.agent_1.update_position((6 + i, 6 + i))

        # Path length = steps + 1 (for starting position)
        self.assertEqual(self.agent_1.steps_taken, len(self.agent_1.path) - 1)

    # ===== Edge Cases =====
    def test_rapid_movements(self):
        """Test rapid successive movements."""
        for i in range(50):
            self.agent_1.update_position((6 + i, 6))
        self.assertEqual(self.agent_1.steps_taken, 50)

    def test_same_position_multiple_times(self):
        """Test tracking when trying to update with same position (edge case)."""
        original_pos = self.agent_1.current_position
        self.agent_1.update_position(original_pos)
        # Position updates to same - it's added to visited and path
        self.assertIn(original_pos, self.agent_1.visited_positions)


if __name__ == '__main__':
    unittest.main()
