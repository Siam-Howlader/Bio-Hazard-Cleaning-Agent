from Agent import Agent
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.start_pos_1 = (5, 5)
        self.start_pos_2 = (0, 0)
        self.start_pos_3 = (50, 50)
        self.agent_1 = Agent(self.start_pos_1)
        self.agent_2 = Agent(self.start_pos_2)
        self.agent_3 = Agent(self.start_pos_3)

    def test_initialization(self):
        self.assertEqual(self.agent_1.current_position, self.start_pos_1)
        self.assertTrue(self.agent_1.active)
        self.assertIsNone(self.agent_1.stop_reason)
        self.assertEqual(self.agent_1.steps_taken, 0)
        self.assertEqual(self.agent_1.waste_collected, 0)
        self.assertIn(self.start_pos_1, self.agent_1.visited_positions)
        self.assertEqual(self.agent_1.path[0], self.start_pos_1)
        self.assertIsInstance(self.agent_1.visited_positions, set)
        self.assertIsInstance(self.agent_1.path, list)

    def test_update_position(self):
        new_pos = (6, 6)
        self.agent_1.update_position(new_pos)
        self.assertEqual(self.agent_1.current_position, new_pos)
        self.assertEqual(self.agent_1.steps_taken, 1)
        self.assertIn(new_pos, self.agent_1.visited_positions)
        self.assertIn(new_pos, self.agent_1.path)

        self.agent_1.update_position((7, 7))
        self.agent_1.update_position((8, 8))
        self.assertEqual(self.agent_1.steps_taken, 3)
        expected_path = [self.start_pos_1, (6, 6), (7, 7), (8, 8)]
        self.assertEqual(self.agent_1.path, expected_path)

    def test_collect_waste(self):
        initial_waste = self.agent_1.waste_collected
        self.agent_1.collect_waste()
        self.assertEqual(self.agent_1.waste_collected, initial_waste + 1)

        for _ in range(5):
            self.agent_1.collect_waste()
        self.assertEqual(self.agent_1.waste_collected, 6)

        self.agent_1.update_position((6, 6))
        self.agent_1.collect_waste()
        self.assertEqual(self.agent_1.steps_taken, 1)
        self.assertEqual(self.agent_1.waste_collected, 7)

    def test_stop(self):
        self.agent_1.stop("Test reason")
        self.assertFalse(self.agent_1.active)
        self.assertEqual(self.agent_1.stop_reason, "Test reason")

        agent = Agent((1, 1))
        agent.stop("No valid moves")
        self.assertFalse(agent.active)
        self.assertEqual(agent.stop_reason, "No valid moves")

    def test_has_visited(self):
        self.assertTrue(self.agent_1.has_visited(self.start_pos_1))

        new_pos = (7, 7)
        self.agent_1.update_position(new_pos)
        self.assertTrue(self.agent_1.has_visited(new_pos))
        self.assertFalse(self.agent_1.has_visited((99, 99)))

        positions = [(6, 6), (8, 8)]
        for pos in positions:
            self.agent_1.update_position(pos)
        for pos in positions:
            self.assertTrue(self.agent_1.has_visited(pos))

    def test_get_current_position(self):
        self.assertEqual(self.agent_1.get_current_position(), self.start_pos_1)
        self.agent_1.update_position((10, 10))
        self.assertEqual(self.agent_1.get_current_position(), (10, 10))

    def test_get_path(self):
        path = self.agent_1.get_path()
        self.assertEqual(path[0], self.start_pos_1)

        self.agent_1.update_position((6, 6))
        self.agent_1.update_position((7, 7))
        path = self.agent_1.get_path()
        self.assertEqual(len(path), 3)

        path1 = self.agent_1.get_path()
        path1.append((999, 999))
        path2 = self.agent_1.get_path()
        self.assertNotEqual(path1, path2)

    def test_get_statistics(self):
        stats = self.agent_1.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn("steps_taken", stats)
        self.assertIn("waste_collected", stats)
        self.assertIn("stop_reason", stats)
        self.assertEqual(stats["steps_taken"], 0)
        self.assertEqual(stats["waste_collected"], 0)
        self.assertIsNone(stats["stop_reason"])

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

    def test_edge_cases(self):
        agent0 = Agent((0, 0))
        self.assertEqual(agent0.current_position, (0, 0))

        agent_large = Agent((9999, 9999))
        self.assertEqual(agent_large.current_position, (9999, 9999))

        agent_neg = Agent((-10, -10))
        self.assertEqual(agent_neg.current_position, (-10, -10))

        for i in range(50):
            self.agent_1.update_position((6 + i, 6))
        self.assertEqual(self.agent_1.steps_taken, 50)
        self.assertEqual(self.agent_1.steps_taken, len(self.agent_1.path) - 1)


if __name__ == '__main__':
    unittest.main()
