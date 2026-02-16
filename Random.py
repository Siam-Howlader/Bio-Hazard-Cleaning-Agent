import random

class Random:
    def __init__(self, agent, action_module, movement_validator):
        self.agent = agent
        self.action_module = action_module
        self.movement_validator = movement_validator

    # Perform One Random Move
    def perform_random_move(self):
        # Get all possible actions
        actions = self.action_module.get_all_actions()
        random.shuffle(actions)  # Shuffle for randomness

        # Try each action until a valid one is found
        for action_name in actions:
            dr, dc = self.action_module.get_action_delta(action_name)
            new_r = self.agent.get_current_position()[0] + dr
            new_c = self.agent.get_current_position()[1] + dc
            new_position = (new_r, new_c)

            if self.movement_validator.is_move_valid(new_position):
                # Valid move, update agent
                self.agent.update_position(new_position)
                return True

        # No valid moves found → agent stops automatically
        self.agent.stop("No valid moves")
        return False
