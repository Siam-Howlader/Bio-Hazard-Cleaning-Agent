import random
from human_avoidance import handle_human_encounter


class Random:
    def __init__(self, agent, action_module, movement_validator):
        self.agent = agent
        self.action_module = action_module
        self.movement_validator = movement_validator

    def perform_random_move(self):
        actions = self.action_module.get_all_actions()
        random.shuffle(actions)
        env = getattr(self.movement_validator, "environment", None)

        # quick adjacency check: if any neighboring cell has a human, handle it
        if env:
            ar, ac = self.agent.get_current_position()
            for name in actions:
                dr, dc = self.action_module.get_action_delta(name)
                neigh = (ar + dr, ac + dc)
                if env.is_human(neigh):
                    if handle_human_encounter(self.agent, env, self.movement_validator):
                        return True

        def sign(x):
            return (x > 0) - (x < 0)

        for name in actions:
            dr, dc = self.action_module.get_action_delta(name)
            ar, ac = self.agent.get_current_position()
            new = (ar + dr, ac + dc)
            if env and env.is_human(new):
                # delegate to human_avoidance logic
                if handle_human_encounter(self.agent, env, self.movement_validator):
                    return True
                continue
            if self.movement_validator.is_move_valid(self.agent.get_current_position(), new, getattr(self.agent, "visited_positions", set())):
                self.agent.update_position(new)
                if env and env.is_bio_hazard(new):
                    env.clean_cell(new)
                    self.agent.collect_waste()
                return True
        self.agent.stop("No valid moves")
        return False
