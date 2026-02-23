class Action:
    actions = {
        "MOVE_UP": (-1, 0),
        "MOVE_DOWN": (1, 0),
        "MOVE_LEFT": (0, -1),
        "MOVE_RIGHT": (0, 1),
    }

    def get_all_actions(self):
        return list(self.actions)

    def get_action_delta(self, name):
        return self.actions.get(name)

    def is_valid_action(self, name):
        return name in self.actions
    # python -m pytest -q -s tests/test_human_avoidance.py
