from Environment import Environment
import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.env_small = Environment(10)
        self.env_medium = Environment(50)
        self.env_large = Environment(100)

    def test_initialization(self):
        self.assertEqual(self.env_small.size, 10)
        self.assertEqual(self.env_small.grid.shape, (10, 10))
        self.assertEqual(self.env_medium.size, 50)
        self.assertEqual(self.env_medium.grid.shape, (50, 50))
        self.assertEqual(self.env_small.grid.dtype, np.int_)
        self.assertIsInstance(self.env_small.grid, np.ndarray)

    def test_inaccessible_areas(self):
        env = Environment(20)
        self.assertTrue(np.all(env.grid[0, :] == 2))
        self.assertTrue(np.all(env.grid[19, :] == 2))
        self.assertTrue(np.all(env.grid[:, 0] == 2))
        self.assertTrue(np.all(env.grid[:, 19] == 2))

        env100 = Environment(100)
        self.assertTrue(np.all(env100.grid[1:21, 79:99] == 2))
        self.assertTrue(np.all(env100.grid[69:99, 1:31] == 2))
        self.assertTrue(np.all(env100.grid[35:61, 35:61] == 2))
        self.assertTrue(np.all(env100.grid[40:50, 0:15] == 2))

    def test_is_inside_grid(self):
        self.assertTrue(self.env_small.is_inside_grid((0, 0)))
        self.assertTrue(self.env_small.is_inside_grid((5, 5)))
        self.assertTrue(self.env_small.is_inside_grid((9, 9)))
        self.assertFalse(self.env_small.is_inside_grid((5, 10)))
        self.assertFalse(self.env_small.is_inside_grid((10, 5)))
        self.assertFalse(self.env_small.is_inside_grid((-1, 5)))
        self.assertFalse(self.env_small.is_inside_grid((5, -1)))

    def test_is_accessible(self):
        env = Environment(20)
        self.assertTrue(env.is_accessible((10, 10)))
        self.assertFalse(self.env_small.is_accessible((0, 0)))
        self.assertFalse(self.env_small.is_accessible((9, 0)))

        env100 = Environment(100)
        self.assertFalse(env100.is_accessible((10, 85)))

    def test_place_and_count_bio_hazards(self):
        self.env_small.place_bio_hazards(5)
        hazard_count = np.sum(self.env_small.grid == 1)
        self.assertEqual(hazard_count, 5)
        self.assertEqual(self.env_small.count_bio_hazards(), 5)

        self.env_small.place_bio_hazards(0)
        self.assertEqual(self.env_small.count_bio_hazards(), 0)

        self.env_medium.place_bio_hazards(10)
        bio_hazard_positions = np.argwhere(self.env_medium.grid == 1)
        unique_positions = len(np.unique(bio_hazard_positions, axis=0))
        self.assertEqual(len(bio_hazard_positions), unique_positions)

    def test_is_bio_hazard(self):
        self.env_small.place_bio_hazards(1)
        hazard_pos = np.argwhere(self.env_small.grid == 1)[0]
        self.assertTrue(self.env_small.is_bio_hazard(tuple(hazard_pos)))
        self.assertFalse(self.env_small.is_bio_hazard((5, 5)))

    def test_is_clean(self):
        self.env_small.place_bio_hazards(1)
        self.assertTrue(self.env_small.is_clean((5, 5)))

        hazard_pos = np.argwhere(self.env_small.grid == 1)[0]
        hazard_tuple = tuple(hazard_pos)
        self.assertFalse(self.env_small.is_clean(hazard_tuple))

        self.env_small.clean_cell(hazard_tuple)
        self.assertTrue(self.env_small.is_clean(hazard_tuple))

    def test_clean_cell(self):
        self.env_small.place_bio_hazards(3)
        initial_count = self.env_small.count_bio_hazards()
        hazard_pos = np.argwhere(self.env_small.grid == 1)[0]
        hazard_tuple = tuple(hazard_pos)

        result = self.env_small.clean_cell(hazard_tuple)
        self.assertTrue(result)
        self.assertEqual(self.env_small.grid[hazard_tuple], 0)
        self.assertEqual(self.env_small.count_bio_hazards(), initial_count - 1)

        result = self.env_small.clean_cell(hazard_tuple)
        self.assertFalse(result)

        result = self.env_small.clean_cell((5, 5))
        self.assertFalse(result)

    def test_count_areas(self):
        self.env_small.place_bio_hazards(3)
        total = (self.env_small.count_bio_hazards() +
                 self.env_small.count_inaccessible_areas() +
                 self.env_small.count_clean_areas())
        self.assertEqual(total, self.env_small.size ** 2)

        inaccessible_count = self.env_medium.count_inaccessible_areas()
        self.assertGreater(inaccessible_count, 0)

        clean_count = self.env_small.count_clean_areas()
        self.assertGreater(clean_count, 0)

    def test_get_coordinates(self):
        self.env_small.place_bio_hazards(3)
        coords = self.env_small.get_bio_hazard_coordinates()
        self.assertEqual(len(coords), 3)

        coords_empty = Environment(10).get_bio_hazard_coordinates()
        self.assertEqual(len(coords_empty), 0)

        inaccessible_coords = self.env_medium.get_inaccessible_coordinates()
        self.assertGreater(len(inaccessible_coords), 0)
        self.assertEqual(len(inaccessible_coords),
                         self.env_medium.count_inaccessible_areas())

    def test_get_grid(self):
        grid_copy = self.env_small.get_grid()
        grid_copy[0, 0] = 999
        self.assertNotEqual(self.env_small.grid[0, 0], 999)

        grid_copy_med = self.env_medium.get_grid()
        self.assertEqual(grid_copy_med.shape, (50, 50))

    def test_edge_cases(self):
        env_min = Environment(5)
        self.assertEqual(env_min.size, 5)
        self.assertIsNotNone(env_min.grid)

        env_large = Environment(500)
        self.assertEqual(env_large.size, 500)
        self.assertEqual(env_large.grid.shape, (500, 500))

        accessible_area_count = np.sum(env_min.grid != 2)
        env_min.place_bio_hazards(accessible_area_count - 1)
        self.assertEqual(env_min.count_bio_hazards(),
                         accessible_area_count - 1)

        self.env_small.place_bio_hazards(5)
        hazard_positions = np.argwhere(self.env_small.grid == 1)
        for pos in hazard_positions:
            self.env_small.clean_cell(tuple(pos))
        self.assertEqual(self.env_small.count_bio_hazards(), 0)


if __name__ == '__main__':
    unittest.main()
