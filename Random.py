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

        for name in actions:
            dr, dc = self.action_module.get_action_delta(name)
            ar, ac = self.agent.get_current_position()
            new = (ar + dr, ac + dc)
            if env and env.is_human(new):
                self.agent.human_encounters += 1
                bio = env.get_bio_hazard_coordinates()
                if not bio:
                    continue
                nearest = min(bio, key=lambda b: abs(
                    b[0] - ar) + abs(b[1] - ac))
                tr, tc = nearest
                sdr, sdc = sign(tr - ar), sign(tc - ac)
                cands = []
                if sdr:
                    cands.append((ar + sdr, ac))
                if sdc:
                    cands.append((ar, ac + sdc))
                if sdr and sdc:
                    cands.append((ar + sdr, ac + sdc))
                for cand in cands:
                    if self.movement_validator.is_move_valid(cand):
                        self.agent.update_position(cand)
                        self.agent.alternative_paths_used += 1
                        if env.is_bio_hazard(cand):
                            env.clean_cell(cand)
                            self.agent.collect_waste()
                        return True
                continue
            if self.movement_validator.is_move_valid(new):
                self.agent.update_position(new)
                if env and env.is_bio_hazard(new):
                    env.clean_cell(new)
                    self.agent.collect_waste()
                return True
        self.agent.stop("No valid moves")
        return False
