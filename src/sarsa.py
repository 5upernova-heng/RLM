from solver import Solver


class SARSA(Solver):
    def __init__(self, action_list):
        self.action_list = action_list
        pass

    def make_decision(self, state: str) -> int:
        pass

    def learn(self, state: str, action: int, reward: int, next_state: str):
        pass
