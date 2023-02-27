"""
Abstract Class
Reinforcement Learning Maze Solver
"""


class Solver:
    def make_decision(self, state: str) -> int:
        pass

    def learn(self, state: str, action: int, reward: int, next_state: str):
        pass
