import numpy as np


class Environment:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self._create_inaccessible_areas()

    def _create_inaccessible_areas(self):
        s = self.size
        self.grid[0, :] = 2
        self.grid[s - 1, :] = 2
        self.grid[:, 0] = 2
        self.grid[:, s - 1] = 2

    def place_bio_hazards(self, count):
        if count <= 0:
            self.grid[self.grid == 1] = 0
            return 0
        empty = np.argwhere(self.grid == 0)
        if len(empty) == 0:
            return 0
        n = min(int(count), len(empty))
        idx = np.random.choice(len(empty), n, replace=False)
        r, c = empty[idx].T
        self.grid[r, c] = 1
        return int(n)

    def place_humans(self, count):
        if count <= 0:
            self.grid[self.grid == 3] = 0
            return 0
        empty = np.argwhere(self.grid == 0)
        if len(empty) == 0:
            return 0
        n = min(int(count), len(empty))
        idx = np.random.choice(len(empty), n, replace=False)
        r, c = empty[idx].T
        self.grid[r, c] = 3
        return int(n)

    def is_inside_grid(self, pos):
        if not pos or len(pos) != 2:
            return False
        r, c = pos
        return 0 <= r < self.size and 0 <= c < self.size

    def is_accessible(self, pos):
        if not self.is_inside_grid(pos):
            return False
        r, c = pos
        return self.grid[r, c] != 2

    def is_bio_hazard(self, pos):
        if not self.is_inside_grid(pos):
            return False
        r, c = pos
        return self.grid[r, c] == 1

    def is_human(self, pos):
        if not self.is_inside_grid(pos):
            return False
        r, c = pos
        return self.grid[r, c] == 3

    def clean_cell(self, pos):
        if not self.is_inside_grid(pos):
            return False
        r, c = pos
        if self.grid[r, c] == 1:
            self.grid[r, c] = 0
            return True
        return False

    def get_bio_hazard_coordinates(self):
        return np.argwhere(self.grid == 1).tolist()

    def get_clean_area_coordinates(self):
        return np.argwhere(self.grid == 0).tolist()

    def count_bio_hazards(self):
        return int(np.sum(self.grid == 1))

    def count_clean_areas(self):
        return int(np.sum(self.grid == 0))

    def count_inaccessible_areas(self):
        return int(np.sum(self.grid == 2))

    def place_humans(self, human_count):
        if human_count <= 0:
            self.grid[self.grid == 3] = 0
            return 0

        empty_positions = np.argwhere(self.grid == 0)
        if len(empty_positions) == 0:
            return 0

        actual_count = min(int(human_count), len(empty_positions))
        if actual_count <= 0:
            return 0

        selected_indices = np.random.choice(
            len(empty_positions), actual_count, replace=False)
        rows, cols = empty_positions[selected_indices].T
        self.grid[rows, cols] = 3
        return int(actual_count)

    def is_human(self, position):
        if not self.is_inside_grid(position):
            return False
        r, c = position
        return bool(self.grid[r, c] == 3)
