import numpy as np


class Environment:

    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)

        self._create_inaccessible_areas()

    def _create_inaccessible_areas(self):
        size = self.size
        self.grid[0, :] = 2
        self.grid[size - 1, :] = 2
        self.grid[:, 0] = 2
        self.grid[:, size - 1] = 2

        if size >= 100:
            self.grid[1:21, 79:99] = 2
            self.grid[39:60, 79:99] = 2
            self.grid[79:99, 79:99] = 2
            self.grid[1:21, 1:21] = 2
            self.grid[69:99, 1:31] = 2
            self.grid[69:99, 40:65] = 2
            self.grid[40:50, 0:15] = 2
            self.grid[35:61, 35:61] = 2

    def place_bio_hazards(self, bio_hazard_count):
        if bio_hazard_count <= 0:
            # Clear all existing bio hazards
            self.grid[self.grid == 1] = 0
            return 0

        empty_positions = np.argwhere(self.grid == 0)

        if len(empty_positions) == 0:
            return 0

        actual_count = min(int(bio_hazard_count), len(empty_positions))

        if actual_count <= 0:
            return 0

        selected_indices = np.random.choice(
            len(empty_positions),
            actual_count,
            replace=False
        )

        rows, cols = empty_positions[selected_indices].T
        self.grid[rows, cols] = 1

        return int(actual_count)

    def is_inside_grid(self, position):
        if position is None or len(position) != 2:
            return False
        r, c = position
        return bool(0 <= r < self.size and 0 <= c < self.size)

    def is_accessible(self, position):
        if not self.is_inside_grid(position):
            return False
        r, c = position
        return bool(self.grid[r, c] != 2)

    def is_bio_hazard(self, position):
        if not self.is_inside_grid(position):
            return False
        r, c = position
        return bool(self.grid[r, c] == 1)

    def is_clean(self, position):
        if not self.is_inside_grid(position):
            return False
        r, c = position
        return bool(self.grid[r, c] == 0)

    def clean_cell(self, position):
        if not self.is_inside_grid(position):
            return False

        r, c = position

        if self.grid[r, c] == 1:
            self.grid[r, c] = 0
            return True

        return False

    def count_bio_hazards(self):
        return int(np.sum(self.grid == 1))

    def count_inaccessible_areas(self):
        return int(np.sum(self.grid == 2))

    def count_clean_areas(self):
        return int(np.sum(self.grid == 0))

    def count_accessible_areas(self):
        return int(np.sum(self.grid != 2))

    def get_grid(self):
        return self.grid.copy()

    def get_bio_hazard_coordinates(self):
        return np.argwhere(self.grid == 1).tolist()

    def get_inaccessible_coordinates(self):
        return np.argwhere(self.grid == 2).tolist()

    def get_clean_area_coordinates(self):
        return np.argwhere(self.grid == 0).tolist()
