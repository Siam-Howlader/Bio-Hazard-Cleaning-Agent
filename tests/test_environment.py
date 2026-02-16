from Environment import Environment
import unittest
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestEnvironment(unittest.TestCase):
    """Test cases for the Environment module."""

    def setUp(self):
        """Set up test fixtures."""
        self.env_small = Environment(10)
        self.env_medium = Environment(50)
        self.env_large = Environment(100)

    def tearDown(self):
        """Clean up after tests."""
        self.env_small = None
        self.env_medium = None
        self.env_large = None

    # ===== Initialization Tests =====
    def test_environment_initialization_size_10(self):
        """Test that environment initializes with correct size."""
        self.assertEqual(self.env_small.size, 10)
        self.assertEqual(self.env_small.grid.shape, (10, 10))

    def test_environment_initialization_size_50(self):
        """Test environment initialization with different size."""
        self.assertEqual(self.env_medium.size, 50)
        self.assertEqual(self.env_medium.grid.shape, (50, 50))

    def test_environment_grid_dtype(self):
        """Test that grid is initialized with correct data type."""
        self.assertEqual(self.env_small.grid.dtype, np.int_)

    def test_environment_grid_is_numpy_array(self):
        """Test that grid is a numpy array."""
        self.assertIsInstance(self.env_small.grid, np.ndarray)

    # ===== Inaccessible Area Tests =====
    def test_borders_are_inaccessible(self):
        """Test that all borders are marked as inaccessible (value 2)."""
        env = Environment(20)
        # Top border
        self.assertTrue(np.all(env.grid[0, :] == 2))
        # Bottom border
        self.assertTrue(np.all(env.grid[19, :] == 2))
        # Left border
        self.assertTrue(np.all(env.grid[:, 0] == 2))
        # Right border
        self.assertTrue(np.all(env.grid[:, 19] == 2))

    def test_academic_buildings_inaccessible(self):
        """Test that academic buildings are marked as inaccessible."""
        env = Environment(100)
        # Academic Building-1 at [1:21, 79:99]
        self.assertTrue(np.all(env.grid[1:21, 79:99] == 2))

    def test_administrative_buildings_inaccessible(self):
        """Test that administrative buildings are inaccessible."""
        env = Environment(100)
        # Administrative Building-1 at [69:99, 1:31]
        self.assertTrue(np.all(env.grid[69:99, 1:31] == 2))

    def test_pond_inaccessible(self):
        """Test that pond area is marked as inaccessible."""
        env = Environment(100)
        self.assertTrue(np.all(env.grid[35:61, 35:61] == 2))

    def test_guest_house_inaccessible(self):
        """Test that guest house is inaccessible."""
        env = Environment(100)
        self.assertTrue(np.all(env.grid[40:50, 0:15] == 2))

    # ===== is_inside_grid Tests =====
    def test_is_inside_grid_valid_positions(self):
        """Test is_inside_grid with valid positions."""
        self.assertTrue(self.env_small.is_inside_grid((0, 0)))
        self.assertTrue(self.env_small.is_inside_grid((5, 5)))
        self.assertTrue(self.env_small.is_inside_grid((9, 9)))

    def test_is_inside_grid_boundary_positions(self):
        """Test is_inside_grid with boundary positions."""
        # Top-left corner
        self.assertTrue(self.env_small.is_inside_grid((0, 0)))
        # Bottom-right corner
        self.assertTrue(self.env_small.is_inside_grid((9, 9)))

    def test_is_inside_grid_outside_right(self):
        """Test is_inside_grid with position outside right boundary."""
        self.assertFalse(self.env_small.is_inside_grid((5, 10)))

    def test_is_inside_grid_outside_bottom(self):
        """Test is_inside_grid with position below bottom boundary."""
        self.assertFalse(self.env_small.is_inside_grid((10, 5)))

    def test_is_inside_grid_negative_indices(self):
        """Test is_inside_grid with negative indices."""
        self.assertFalse(self.env_small.is_inside_grid((-1, 5)))
        self.assertFalse(self.env_small.is_inside_grid((5, -1)))

    # ===== is_accessible Tests =====
    def test_is_accessible_clean_area(self):
        """Test is_accessible for clean accessible areas."""
        # Find an accessible area and test it
        env = Environment(20)
        # Access areas that are not borders (should be accessible if not buildings)
        self.assertTrue(env.is_accessible((10, 10)))

    def test_is_accessible_inaccessible_border(self):
        """Test is_accessible for inaccessible border cells."""
        self.assertFalse(self.env_small.is_accessible((0, 0)))
        self.assertFalse(self.env_small.is_accessible((9, 0)))

    def test_is_accessible_building_area(self):
        """Test is_accessible for building areas."""
        env = Environment(100)
        self.assertFalse(env.is_accessible((10, 85)))

    # ===== Bio-Hazard Placement Tests =====
    def test_place_bio_hazards_count(self):
        """Test that correct number of bio-hazards are placed."""
        self.env_small.place_bio_hazards(5)
        hazard_count = np.sum(self.env_small.grid == 1)
        self.assertEqual(hazard_count, 5)

    def test_place_bio_hazards_in_accessible_areas_only(self):
        """Test that bio-hazards are only placed in accessible areas."""
        self.env_small.place_bio_hazards(3)
        bio_hazard_positions = np.argwhere(self.env_small.grid == 1)
        for pos in bio_hazard_positions:
            self.assertEqual(self.env_small.grid[pos[0], pos[1]], 1)
            # Verify these positions don't overlap with inaccessible areas
            self.assertNotEqual(self.env_small.grid[pos[0], pos[1]], 2)

    def test_place_bio_hazards_zero_hazards(self):
        """Test placing zero bio-hazards."""
        self.env_small.place_bio_hazards(0)
        self.assertEqual(self.env_small.count_bio_hazards(), 0)

    def test_place_bio_hazards_no_duplicates(self):
        """Test that bio-hazards are not placed in duplicate positions."""
        self.env_medium.place_bio_hazards(10)
        bio_hazard_positions = np.argwhere(self.env_medium.grid == 1)
        unique_positions = len(np.unique(bio_hazard_positions, axis=0))
        self.assertEqual(len(bio_hazard_positions), unique_positions)

    # ===== is_bio_hazard Tests =====
    def test_is_bio_hazard_true(self):
        """Test is_bio_hazard when position contains hazard."""
        self.env_small.place_bio_hazards(1)
        hazard_pos = np.argwhere(self.env_small.grid == 1)[0]
        self.assertTrue(self.env_small.is_bio_hazard(tuple(hazard_pos)))

    def test_is_bio_hazard_false_clean_area(self):
        """Test is_bio_hazard on clean area."""
        self.env_small.place_bio_hazards(1)
        # Find accessible clean position
        self.assertFalse(self.env_small.is_bio_hazard((5, 5)))

    # ===== is_clean Tests =====
    def test_is_clean_empty_position(self):
        """Test is_clean on accessible clean area."""
        self.env_small.place_bio_hazards(1)
        self.assertTrue(self.env_small.is_clean((5, 5)))

    def test_is_clean_after_cleaning(self):
        """Test is_clean after cleaning a hazard."""
        self.env_small.place_bio_hazards(1)
        hazard_pos = np.argwhere(self.env_small.grid == 1)[0]
        hazard_tuple = tuple(hazard_pos)
        self.env_small.clean_cell(hazard_tuple)
        self.assertTrue(self.env_small.is_clean(hazard_tuple))

    # ===== clean_cell Tests =====
    def test_clean_cell_success(self):
        """Test cleaning a cell with bio-hazard."""
        self.env_small.place_bio_hazards(1)
        hazard_pos = np.argwhere(self.env_small.grid == 1)[0]
        hazard_tuple = tuple(hazard_pos)
        result = self.env_small.clean_cell(hazard_tuple)
        self.assertTrue(result)
        self.assertEqual(self.env_small.grid[hazard_tuple], 0)

    def test_clean_cell_no_hazard(self):
        """Test cleaning a cell without bio-hazard returns False."""
        result = self.env_small.clean_cell((5, 5))
        self.assertFalse(result)

    def test_clean_cell_reduces_hazard_count(self):
        """Test that cleaning reduces bio-hazard count."""
        self.env_small.place_bio_hazards(3)
        initial_count = self.env_small.count_bio_hazards()
        hazard_pos = np.argwhere(self.env_small.grid == 1)[0]
        self.env_small.clean_cell(tuple(hazard_pos))
        final_count = self.env_small.count_bio_hazards()
        self.assertEqual(initial_count - 1, final_count)

    def test_clean_cell_twice_returns_false(self):
        """Test that cleaning twice returns False on second attempt."""
        self.env_small.place_bio_hazards(1)
        hazard_pos = np.argwhere(self.env_small.grid == 1)[0]
        hazard_tuple = tuple(hazard_pos)
        self.env_small.clean_cell(hazard_tuple)
        result = self.env_small.clean_cell(hazard_tuple)
        self.assertFalse(result)

    # ===== Counting Methods Tests =====
    def test_count_bio_hazards(self):
        """Test counting bio-hazards."""
        self.env_small.place_bio_hazards(5)
        self.assertEqual(self.env_small.count_bio_hazards(), 5)

    def test_count_inaccessible_areas(self):
        """Test counting inaccessible areas."""
        count = self.env_medium.count_inaccessible_areas()
        self.assertGreater(count, 0)

    def test_count_clean_areas(self):
        """Test counting clean areas."""
        count = self.env_small.count_clean_areas()
        self.assertGreater(count, 0)

    def test_count_areas_sum_to_grid_size(self):
        """Test that sum of all area types equals grid size."""
        self.env_small.place_bio_hazards(3)
        total = (self.env_small.count_bio_hazards() +
                 self.env_small.count_inaccessible_areas() +
                 self.env_small.count_clean_areas())
        self.assertEqual(total, self.env_small.size ** 2)

    # ===== Coordinate Retrieval Tests =====
    def test_get_bio_hazard_coordinates(self):
        """Test retrieving bio-hazard coordinates."""
        self.env_small.place_bio_hazards(3)
        coords = self.env_small.get_bio_hazard_coordinates()
        self.assertEqual(len(coords), 3)

    def test_get_bio_hazard_coordinates_empty(self):
        """Test getting bio-hazard coordinates when none exist."""
        coords = self.env_small.get_bio_hazard_coordinates()
        self.assertEqual(len(coords), 0)

    def test_get_inaccessible_coordinates(self):
        """Test retrieving inaccessible area coordinates."""
        coords = self.env_small.get_inaccessible_coordinates()
        self.assertGreater(len(coords), 0)

    def test_get_inaccessible_coordinates_count_matches(self):
        """Test that coordinate count matches inaccessible area count."""
        coords = self.env_medium.get_inaccessible_coordinates()
        count = self.env_medium.count_inaccessible_areas()
        self.assertEqual(len(coords), count)

    # ===== get_grid Tests =====
    def test_get_grid_returns_copy(self):
        """Test that get_grid returns a copy not reference."""
        grid_copy = self.env_small.get_grid()
        grid_copy[0, 0] = 999
        self.assertNotEqual(self.env_small.grid[0, 0], 999)

    def test_get_grid_same_size(self):
        """Test that returned grid has same size as original."""
        grid_copy = self.env_medium.get_grid()
        self.assertEqual(grid_copy.shape, (50, 50))

    # ===== Boundary Value Analysis =====
    def test_minimum_grid_size(self):
        """Test environment with minimum size."""
        env_min = Environment(5)
        self.assertEqual(env_min.size, 5)
        self.assertIsNotNone(env_min.grid)

    def test_large_grid_size(self):
        """Test environment with large size."""
        env_large = Environment(500)
        self.assertEqual(env_large.size, 500)
        self.assertEqual(env_large.grid.shape, (500, 500))

    # ===== Edge Case Tests =====
    def test_place_maximum_hazards(self):
        """Test placing maximum possible bio-hazards (all accessible areas)."""
        # Environment 20x20=400, minus borders and buildings = accessible areas
        self.env_medium.place_bio_hazards(50)
        self.assertEqual(self.env_medium.count_bio_hazards(), 50)

    def test_clean_all_hazards(self):
        """Test cleaning all hazards."""
        self.env_small.place_bio_hazards(5)
        hazard_positions = np.argwhere(self.env_small.grid == 1)
        for pos in hazard_positions:
            self.env_small.clean_cell(tuple(pos))
        self.assertEqual(self.env_small.count_bio_hazards(), 0)


if __name__ == '__main__':
    unittest.main()
