import Environment


class Movement:
    def __init__(self, environment, agent):
        self.environment = environment
        self.agent = agent

    def is_move_valid(self, next_position):
        next_position = tuple(next_position)
        current_position = tuple(self.agent.get_current_position())
        visited_positions = getattr(self.agent, "visited_positions", set())

        if not bool(self.environment.is_inside_grid(next_position)):
            if hasattr(self.agent, "stop"):
                self.agent.stop("Hit border")
            return False

        if not bool(self.environment.is_accessible(next_position)):
            return False

        if next_position in visited_positions:
            return False

        if next_position == current_position:
            return False

        return True
