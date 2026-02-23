import random


class Random:
    def __init__(self, agent, action_module, movement_validator):
        self.agent = agent
        self.action_module = action_module
        self.movement_validator = movement_validator

    def perform_random_move(self):
        actions = self.action_module.get_all_actions()
        random.shuffle(actions)

        env = getattr(self.movement_validator, "environment", None)

        def sign(x):
            return (x > 0) - (x < 0)

        for action_name in actions:
            dr, dc = self.action_module.get_action_delta(action_name)
            new_r = self.agent.get_current_position()[0] + dr
            new_c = self.agent.get_current_position()[1] + dc
            new_position = (new_r, new_c)

            # If next cell has a human, avoid by selecting nearest bio-hazard path
            if env is not None and hasattr(env, "is_human") and env.is_human(new_position):
                self.agent.human_encounters = getattr(self.agent, "human_encounters", 0) + 1
                bio_coords = env.get_bio_hazard_coordinates()
                if not bio_coords:
                    continue

                ar, ac = self.agent.get_current_position()
                nearest = min(bio_coords, key=lambda b: abs(b[0] - ar) + abs(b[1] - ac))
                tr, tc = nearest
                step_dr = sign(tr - ar)
                step_dc = sign(tc - ac)

                candidates = []
                if step_dr != 0:
                    candidates.append((ar + step_dr, ac))
                if step_dc != 0:
                    candidates.append((ar, ac + step_dc))
                if step_dr != 0 and step_dc != 0:
                    candidates.append((ar + step_dr, ac + step_dc))

                moved = False
                for cand in candidates:
                    if self.movement_validator.is_move_valid(cand):
                        self.agent.update_position(cand)
                        self.agent.alternative_paths_used = getattr(self.agent, "alternative_paths_used", 0) + 1
                        moved = True
                        if env.is_bio_hazard(cand):
                            env.clean_cell(cand)
                            self.agent.collect_waste()
                        break

                if moved:
                    return True
                else:
                    continue

            if self.movement_validator.is_move_valid(new_position):
                self.agent.update_position(new_position)
                if env is not None and env.is_bio_hazard(new_position):
                    env.clean_cell(new_position)
                    self.agent.collect_waste()
                return True

        self.agent.stop("No valid moves")
        return False
