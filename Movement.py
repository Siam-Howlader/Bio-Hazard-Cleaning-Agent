import Environment


class Movement:
    def __init__(self, environment, agent):
        self.environment = environment
        self.agent = agent

    # Validate Next Move
    def is_move_valid(self, current_position, next_position, visited_positions):
        """
        Returns True only if:
        - next_position is inside the grid
        - next_position is accessible
        - next_position is not in visited_positions
        """
        # Ensure next_position is a tuple of ints
        next_position = tuple(next_position)

        # 1️⃣ Inside grid bounds
        if not bool(self.environment.is_inside_grid(next_position)):
            # Optional: agent stop message
            if hasattr(self.agent, "stop"):
                self.agent.stop("Hit border")
            return False

        # 2️⃣ Accessible
        if not bool(self.environment.is_accessible(next_position)):
            return False

        # 3️⃣ Not visited
        if next_position in visited_positions:
            return False

        # ✅ All conditions passed
        return True
