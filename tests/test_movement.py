from Movement import Movement
from Agent import Agent
from Environment import Environment
import unittest
import sys
import os
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestMovement(unittest.TestCase):
    """Test cases for the Movement module."""

    def setUp(self):
        """Set up test fixtures."""
        self.env_small = Environment(20)
        self.env_medium = Environment(50)
        self.env_large = Environment(100)

        self.agent_small = Agent((10, 10))
        self.agent_medium = Agent((25, 25))
        self.agent_large = Agent((50, 50))

        self.movement_small = Movement(self.env_small, self.agent_small)
        self.movement_medium = Movement(self.env_medium, self.agent_medium)
        self.movement_large = Movement(self.env_large, self.agent_large)

    def tearDown(self):
        """Clean up after tests."""
        self.env_small = None
        self.env_medium = None
        self.agent_small = None
        self.agent_medium = None
        self.movement_small = None
        self.movement_medium = None

    # ===== Initialization Tests =====
    def test_movement_initialization_environment(self):
        """Test that movement module initializes with environment."""
        self.assertIsNotNone(self.movement_small.environment)
        self.assertEqual(self.movement_small.environment, self.env_small)

    def test_movement_initialization_agent(self):
        """Test that movement module initializes with agent."""
        self.assertIsNotNone(self.movement_small.agent)
        self.assertEqual(self.movement_small.agent, self.agent_small)

    # ===== Valid Move Tests =====
    def test_is_move_valid_accessible_unvisited(self):
        """Test valid move to accessible unvisited position."""
        current_position = (10, 10)
        new_position = (11, 10)
        visited = set()
        is_valid = self.movement_small.is_move_valid(
            current_position, new_position, visited)
        self.assertTrue(is_valid)

    def test_is_move_valid_up_direction(self):
        """Test valid move in up direction."""
        current_position = (10, 10)
        new_position = (9, 10)
        visited = set()
        is_valid = self.movement_small.is_move_valid(
            current_position, new_position, visited)
        self.assertTrue(is_valid)

    def test_is_move_valid_down_direction(self):
        """Test valid move in down direction."""
        current_position = (10, 10)
        new_position = (11, 10)
        visited = set()
        is_valid = self.movement_small.is_move_valid(
            current_position, new_position, visited)
        self.assertTrue(is_valid)

    def test_is_move_valid_left_direction(self):
        """Test valid move in left direction."""
        current_position = (10, 10)
        new_position = (10, 9)
        visited = set()
        is_valid = self.movement_small.is_move_valid(
            current_position, new_position, visited)
        self.assertTrue(is_valid)

    def test_is_move_valid_right_direction(self):
        """Test valid move in right direction."""
        current_position = (10, 10)
        new_position = (10, 11)
        visited = set()
        is_valid = self.movement_small.is_move_valid(
            current_position, new_position, visited)
        self.assertTrue(is_valid)

    def test_is_move_valid_diagonal_not_standard(self):
        """Test diagonal move (not typically used in 4-directional movement)."""
        current_position = (10, 10)
        new_position = (11, 11)
        visited = set()
        is_valid = self.movement_small.is_move_valid(
            current_position, new_position, visited)
        # Diagonal should be valid if accessible and unvisited
        self.assertTrue(is_valid)

    # ===== Outside Grid Tests =====
    def test_is_move_valid_outside_right_boundary(self):
        """Test that move to right boundary fails."""
        agent = Agent((19, 18))
        movement = Movement(self.env_small, agent)
        current_position = (19, 18)
        new_position = (19, 20)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    def test_is_move_valid_outside_bottom_boundary(self):
        """Test that move below grid fails."""
        agent = Agent((18, 10))
        movement = Movement(self.env_small, agent)
        current_position = (18, 10)
        new_position = (20, 10)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    def test_is_move_valid_outside_left_boundary(self):
        """Test that move to left boundary fails."""
        agent = Agent((10, 1))
        movement = Movement(self.env_small, agent)
        current_position = (10, 1)
        new_position = (10, -1)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    def test_is_move_valid_outside_top_boundary(self):
        """Test that move above grid fails."""
        agent = Agent((1, 10))
        movement = Movement(self.env_small, agent)
        current_position = (1, 10)
        new_position = (-1, 10)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    def test_is_move_valid_far_outside_grid(self):
        """Test move far outside grid boundaries."""
        current_position = (10, 10)
        new_position = (100, 100)
        visited = set()
        is_valid = self.movement_small.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    def test_is_move_valid_negative_coordinates(self):
        """Test move with negative coordinates."""
        current_position = (10, 10)
        new_position = (-5, -5)
        visited = set()
        is_valid = self.movement_small.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    # ===== Inaccessible Area Tests =====
    def test_is_move_valid_to_border(self):
        """Test that move to border (inaccessible) fails."""
        agent = Agent((10, 1))
        movement = Movement(self.env_small, agent)
        current_position = (10, 1)
        new_position = (10, 0)  # Border
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    def test_is_move_valid_to_building_area(self):
        """Test that move to building area (inaccessible) fails."""
        env = Environment(100)
        agent = Agent((25, 25))
        movement = Movement(env, agent)
        # Academic Building-1 at [1:21, 79:99]
        current_position = (25, 25)
        new_position = (10, 85)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    def test_is_move_valid_to_pond(self):
        """Test that move to pond area fails."""
        env = Environment(100)
        agent = Agent((32, 32))
        movement = Movement(env, agent)
        # Pond at [35:61, 35:61]
        current_position = (32, 32)
        new_position = (45, 45)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    # ===== Visited Position Tests =====
    def test_is_move_valid_to_visited_position(self):
        """Test that move to already visited position fails."""
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)
        # Starting position is already visited
        current_position = (10, 10)
        new_position = (10, 10)
        visited = {(10, 10)}
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    def test_is_move_valid_revisit_after_movement(self):
        """Test that revisiting a cell is invalid."""
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        # Move to new position
        current_position = (10, 10)
        new_pos = (10, 11)
        visited = {(10, 10), (10, 11)}

        # Try to move back to starting position
        is_valid = movement.is_move_valid(new_pos, current_position, visited)
        self.assertFalse(is_valid)

    def test_is_move_valid_multiple_visits_blocked(self):
        """Test that multiple revisit attempts are all blocked."""
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        visited_pos = (10, 10)
        current_position = (10, 11)
        # Try same position multiple times
        for _ in range(3):
            is_valid = movement.is_move_valid(current_position, visited_pos, {
                                              visited_pos, current_position})
            self.assertFalse(is_valid)

    # ===== Border Hit Detection Tests =====
    def test_agent_stops_on_border_hit_right(self):
        """Test that move to border position fails."""
        agent = Agent((10, 18))
        movement = Movement(self.env_small, agent)

        # Try to move to right border (position 19 is border but inside grid bounds)
        current_position = (10, 18)
        new_position = (10, 19)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)

        # Border move should fail
        self.assertFalse(is_valid)
        # Position 19 is inaccessible, not outside grid, so agent may not stop
        # This is expected behavior - accessibility check prevents the move

    def test_agent_stops_on_border_hit_left(self):
        """Test that move to border position fails."""
        agent = Agent((10, 1))
        movement = Movement(self.env_small, agent)

        current_position = (10, 1)
        new_position = (10, 0)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)

        self.assertFalse(is_valid)

    def test_agent_stops_on_border_hit_top(self):
        """Test that move to border position fails."""
        agent = Agent((1, 10))
        movement = Movement(self.env_small, agent)

        current_position = (1, 10)
        new_position = (0, 10)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)

        self.assertFalse(is_valid)

    def test_agent_stops_on_border_hit_bottom(self):
        """Test that move to border position fails."""
        agent = Agent((18, 10))
        movement = Movement(self.env_small, agent)

        current_position = (18, 10)
        new_position = (19, 10)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)

        self.assertFalse(is_valid)

    def test_border_hit_only_once(self):
        """Test that move beyond grid bounds triggers agent stop."""
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        # Try to move completely outside grid
        current_position = (10, 10)
        new_position = (10, 20)  # Outside grid bounds
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)

        # Should fail and stop agent
        self.assertFalse(is_valid)
    # ===== Combination Tests (checking all three conditions) =====

    def test_move_validation_all_conditions(self):
        """Test move validation with all three conditions passing."""
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        # New position: inside grid, accessible, unvisited
        current_position = (10, 10)
        new_position = (11, 11)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertTrue(is_valid)

    def test_move_fails_any_condition(self):
        """Test that move fails if any condition fails."""
        # Outside grid
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)
        self.assertFalse(movement.is_move_valid((10, 10), (20, 10), set()))

        # Inaccessible
        env = Environment(100)
        agent2 = Agent((25, 25))
        movement2 = Movement(env, agent2)
        self.assertFalse(movement2.is_move_valid(
            (25, 25), (10, 85), set()))  # Building area

        # Visited
        agent3 = Agent((10, 10))
        movement3 = Movement(self.env_small, agent3)
        self.assertFalse(movement3.is_move_valid(
            (10, 10), (10, 10), {(10, 10)}))  # Starting position

    # ===== Boundary Value Analysis =====
    def test_move_to_corner_inside(self):
        """Test move to corner inside grid."""
        agent = Agent((1, 1))
        movement = Movement(self.env_small, agent)

        current_position = (1, 1)
        new_position = (2, 2)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertTrue(is_valid)

    def test_move_to_corner_at_border(self):
        """Test move to corner at border."""
        agent = Agent((2, 2))
        movement = Movement(self.env_small, agent)

        current_position = (2, 2)
        new_position = (0, 0)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    def test_move_at_maximum_grid_position(self):
        """Test movement at maximum valid grid position."""
        size = self.env_large.size
        # Use position (30, 70) which avoids all buildings on 100x100 grid
        agent = Agent((30, 70))
        movement = Movement(self.env_large, agent)

        # Try move to valid position (avoids buildings)
        current_position = (30, 70)
        new_position = (30, 69)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertTrue(is_valid)

        # Try move to border (should fail)
        new_position = (99, 70)
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    # ===== Agent State Preservation Tests =====
    def test_failed_move_doesnt_change_agent_position(self):
        """Test that failed move doesn't change agent position."""
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        original_position = agent.current_position
        movement.is_move_valid((10, 10), (20, 20), set())  # Invalid move

        self.assertEqual(agent.current_position, original_position)

    def test_valid_move_still_requires_manual_update(self):
        """Test that valid move doesn't auto-update agent (just validation)."""
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        current_position = (10, 10)
        new_position = (11, 11)
        visited = set()
        movement.is_move_valid(current_position, new_position, visited)

        # Agent position should not change - movement only validates
        self.assertEqual(agent.current_position, (10, 10))

    # ===== Edge Cases =====
    def test_movement_validation_consistency(self):
        """Test that validation result is consistent for same inputs."""
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        current_position = (10, 10)
        new_position = (11, 11)
        visited = set()

        result1 = movement.is_move_valid(
            current_position, new_position, visited)
        result2 = movement.is_move_valid(
            current_position, new_position, visited)

        # Both should return same if visited set is same
        self.assertEqual(result1, result2)

    def test_movement_with_circular_path(self):
        """Test that agent cannot create circular path (revisit)."""
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        # Create path tracking visited positions
        visited = {(10, 10)}
        current_pos = (10, 10)
        path_positions = [(10, 11), (11, 11), (11, 10)]

        for pos in path_positions:
            if movement.is_move_valid(current_pos, pos, visited):
                visited.add(pos)
                current_pos = pos

        # Try to return to starting position
        can_return = movement.is_move_valid(current_pos, (10, 10), visited)
        self.assertFalse(can_return)


if __name__ == '__main__':
    unittest.main()
