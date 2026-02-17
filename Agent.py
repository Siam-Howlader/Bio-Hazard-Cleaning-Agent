class Agent:

    def __init__(self, start_position):
        self.current_position = start_position
        self.active = True
        self.stop_reason = None
        self.visited_positions = set()
        self.path = []
        self.steps_taken = 0
        self.waste_collected = 0
        self._visit_position(start_position)

    def _visit_position(self, position):
        self.visited_positions.add(position)
        self.path.append(position)

    def update_position(self, new_position):
        self.current_position = new_position
        self.steps_taken += 1
        self._visit_position(new_position)

    def collect_waste(self):
        self.waste_collected += 1

    def stop(self, reason):
        self.active = False
        if self.stop_reason is None:
            self.stop_reason = reason

    def has_visited(self, position):
        return position in self.visited_positions

    def get_current_position(self):
        return self.current_position

    def get_path(self):
        return list(self.path)

    def get_statistics(self):
        return {
            "steps_taken": self.steps_taken,
            "waste_collected": self.waste_collected,
            "stop_reason": self.stop_reason
        }
