class Action:
    def __init__(self):
        self.actions = {
            "MOVE_UP": (-1, 0),
            "MOVE_DOWN": (1, 0),
            "MOVE_LEFT": (0, -1),
            "MOVE_RIGHT": (0, 1)
        }
    def get_all_actions(self):
        return list(self.actions.keys())

    def get_action_delta(self, action_name):
        return self.actions.get(action_name)

    def is_valid_action(self, action_name):
        return action_name in self.actions
    

    # python -m pytest tests -v
    # python -m pytest tests/test_environment.py -v
    # python -m pytest tests/test_action.py -v
    # python -m pytest tests/test_movement.py -v
    # python -m pytest tests/test_agent.py -v