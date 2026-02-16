class Agent:

    def __init__(self, start_position):

        # Agent State
        self.current_position = start_position
        self.active = True
        self.stop_reason = None

        # Movement Tracking
        self.visited_positions = set()
        self.path = []

        # Performance Statistics
        self.steps_taken = 0
        self.waste_collected = 0

        # Initialize starting position
        self._visit_position(start_position)

    # Internal Helpers
    def _visit_position(self, position):
        self.visited_positions.add(position)
        self.path.append(position)

    # Agent Movement State
    def update_position(self, new_position):
        self.current_position = new_position
        self.steps_taken += 1
        self._visit_position(new_position)

    # Waste Collection
    def collect_waste(self):
        self.waste_collected += 1

    # Termination Handling
    def stop(self, reason):
        self.active = False
        # Only set stop_reason once (do not overwrite if already set)
        if self.stop_reason is None:
            self.stop_reason = reason

    # Query Methods
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
