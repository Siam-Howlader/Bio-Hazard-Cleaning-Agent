from Movement import Movement
from Agent import Agent
from Environment import Environment
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestMovement(unittest.TestCase):
    def setUp(self):
        self.env_small = Environment(20)
        self.env_medium = Environment(50)
        self.env_large = Environment(100)

        self.agent_small = Agent((10, 10))
        self.agent_medium = Agent((25, 25))
        self.agent_large = Agent((50, 50))

        self.movement_small = Movement(self.env_small, self.agent_small)
        self.movement_medium = Movement(self.env_medium, self.agent_medium)
        self.movement_large = Movement(self.env_large, self.agent_large)

    def test_initialization(self):
        self.assertIsNotNone(self.movement_small.environment)
        self.assertEqual(self.movement_small.environment, self.env_small)
        self.assertIsNotNone(self.movement_small.agent)
        self.assertEqual(self.movement_small.agent, self.agent_small)

    def test_valid_moves_all_directions(self):
        current_position = (10, 10)
        visited = set()

        positions = {
            "up": (9, 10),
            "down": (11, 10),
            "left": (10, 9),
            "right": (10, 11)
        }

        for direction, new_position in positions.items():
            is_valid = self.movement_small.is_move_valid(
                current_position, new_position, visited)
            self.assertTrue(is_valid, f"Move {direction} should be valid")

    def test_boundary_violations(self):
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        boundary_positions = [
            ((10, 10), (10, 20)),
            ((18, 10), (20, 10)),
            ((10, 1), (10, -1)),
            ((1, 10), (-1, 10)),
            ((10, 10), (100, 100)),
            ((10, 10), (-5, -5))
        ]

        for current, new in boundary_positions:
            is_valid = movement.is_move_valid(current, new, set())
            self.assertFalse(
                is_valid, f"Move from {current} to {new} should fail")

    def test_inaccessible_areas(self):
        agent = Agent((10, 1))
        movement = Movement(self.env_small, agent)

        inaccessible_moves = [
            ((10, 1), (10, 0)),
            ((10, 1), (10, 1)),
            ((10, 18), (10, 19))
        ]

        for current, new in inaccessible_moves:
            is_valid = movement.is_move_valid(current, new, set())
            self.assertFalse(
                is_valid, f"Move to inaccessible area should fail")

        env100 = Environment(100)
        agent100 = Agent((25, 25))
        movement100 = Movement(env100, agent100)

        self.assertFalse(movement100.is_move_valid((25, 25), (10, 85), set()))
        self.assertFalse(movement100.is_move_valid((32, 32), (45, 45), set()))

    def test_visited_position_blocking(self):
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        current_position = (10, 10)
        new_position = (10, 10)
        visited = {(10, 10)}
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

        visited = {(10, 10), (10, 11)}
        is_valid = movement.is_move_valid((10, 11), (10, 10), visited)
        self.assertFalse(is_valid)

        visited_pos = (10, 10)
        current_position = (10, 11)
        for _ in range(3):
            is_valid = movement.is_move_valid(current_position, visited_pos, {
                                              visited_pos, current_position})
            self.assertFalse(is_valid)

    def test_corner_and_edge_positions(self):
        agent = Agent((1, 1))
        movement = Movement(self.env_small, agent)

        current_position = (1, 1)
        new_position = (2, 2)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertTrue(is_valid)

        current_position = (2, 2)
        new_position = (0, 0)
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    def test_large_grid_navigation(self):
        size = self.env_large.size
        agent = Agent((30, 70))
        movement = Movement(self.env_large, agent)

        current_position = (30, 70)
        new_position = (30, 69)
        visited = set()
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertTrue(is_valid)

        new_position = (99, 70)
        is_valid = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertFalse(is_valid)

    def test_agent_position_not_modified_by_validation(self):
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        original_position = agent.current_position
        movement.is_move_valid((10, 10), (20, 20), set())
        self.assertEqual(agent.current_position, original_position)

        movement.is_move_valid((10, 10), (11, 11), set())
        self.assertEqual(agent.current_position, (10, 10))

    def test_validation_consistency(self):
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        current_position = (10, 10)
        new_position = (11, 11)
        visited = set()

        result1 = movement.is_move_valid(
            current_position, new_position, visited)
        result2 = movement.is_move_valid(
            current_position, new_position, visited)
        self.assertEqual(result1, result2)

    def test_circular_path_prevention(self):
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        visited = {(10, 10)}
        current_pos = (10, 10)
        path_positions = [(10, 11), (11, 11), (11, 10)]

        for pos in path_positions:
            if movement.is_move_valid(current_pos, pos, visited):
                visited.add(pos)
                current_pos = pos

        can_return = movement.is_move_valid(current_pos, (10, 10), visited)
        self.assertFalse(can_return)

    def test_diagonal_moves(self):
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        current = (10, 10)
        is_valid = movement.is_move_valid(current, (11, 11), set())
        self.assertTrue(is_valid)

    def test_multi_condition_failures(self):
        agent = Agent((10, 10))
        movement = Movement(self.env_small, agent)

        self.assertFalse(movement.is_move_valid((10, 10), (20, 10), set()))

        env100 = Environment(100)
        agent2 = Agent((25, 25))
        movement2 = Movement(env100, agent2)
        self.assertFalse(movement2.is_move_valid((25, 25), (10, 85), set()))

        agent3 = Agent((10, 10))
        movement3 = Movement(self.env_small, agent3)
        self.assertFalse(movement3.is_move_valid(
            (10, 10), (10, 10), {(10, 10)}))


if __name__ == '__main__':
    unittest.main()
