"""
Policy Iteration Method

"""

from solver import Solver
from typing import *
import numpy as np

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


class PolicyIteration(Solver):
    def __init__(self, action_list: List[int], gamma: float = 1.0) -> None:
        self.action_list = action_list
        self.gamma = gamma
        self.policy = {}
        self.state_value = {}
        self.is_convergence = {}
        self.need_update = {}
        self.check_lists = {}
        self.coming_direction = {}
        self.last_action = None

    def add_new_state(self, state: str):
        coming_direction = self.reverse_action(self.last_action)
        self.coming_direction[state] = coming_direction
        self.policy[state] = self.remove_action(self.action_list, coming_direction)
        self.state_value[state] = 0
        self.is_convergence[state] = False
        self.check_lists[state] = self.policy[state].copy()

    def reverse_action(self, action: int) -> int:
        if action == UP:
            return DOWN
        if action == DOWN:
            return UP
        if action == LEFT:
            return RIGHT
        if action == RIGHT:
            return LEFT
        if action == None:
            return None

    def remove_action(self, action_list, action: int) -> List[int]:
        if action in action_list:
            filtered_action_list = action_list.copy()
            filtered_action_list.remove(action)
            return filtered_action_list
        return action_list

    def convert_to_tuple(self, state: str) -> Tuple[int, int]:
        return tuple(map(int, state.replace("(", "").replace(")", "").split(",")))

    def move(self, state: str, direction: int) -> str:
        x, y = self.convert_to_tuple(state)
        if direction == UP:
            return str((x, y - 1))
        if direction == DOWN:
            return str((x, y + 1))
        if direction == LEFT:
            return str((x - 1, y))
        if direction == RIGHT:
            return str((x + 1, y))

    def update_neighbour(self, state: str):
        """
        Update neighbour state value
        """
        coming_direction = self.coming_direction[state]
        reverse_direction = self.reverse_action(coming_direction)
        last_state = self.move(state, coming_direction)
        if reverse_direction in self.policy[last_state]:
            self.policy[last_state] = self.remove_action(
                self.policy[last_state], reverse_direction
            )
        if self.policy[last_state] == []:
            self.state_value[last_state] = -1
            self.update_neighbour(last_state)

    def make_decision(self, state: str) -> int:
        if state not in self.policy.keys():
            self.add_new_state(state)
        if self.is_convergence[state]:
            return np.random.choice(self.policy[state])
        else:
            return self.check_lists[state].pop()

    def learn(self, state: str, action: int, reward: int, next_state: str):
        if reward == 0:
            pass
        if reward == -1:
            self.policy[state] = self.remove_action(self.policy[state], action)
        if self.check_lists[state] == []:
            # converge
            self.is_convergence[state] = True
            if self.policy[state] == []:
                self.state_value[state] = reward
                self.update_neighbour(state)
        self.last_action = action
        if next_state not in self.policy.keys():
            self.add_new_state(next_state)
