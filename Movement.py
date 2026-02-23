class Movement:
    def __init__(self, environment, agent):
        self.environment = environment
        self.agent = agent

    def is_move_valid(self, next_position):
        next_position = tuple(next_position)
        cur = tuple(self.agent.get_current_position())
        visited = getattr(self.agent, "visited_positions", set())
        if not self.environment.is_inside_grid(next_position):
            if hasattr(self.agent, "stop"):
                self.agent.stop("Hit border")
            return False
        if not self.environment.is_accessible(next_position):
            return False
        if next_position in visited or next_position == cur:
            return False
        return True
