import numpy as np
from solver import Solver
from typing import *


class QLearning(Solver):
    def __init__(
        self,
        action_list,
        learning_rate: float = 1,
        reward_decay: float = 1,
        epsilon: float = 1,
    ) -> None:
        self.action_list = action_list
        self.learning_rate = learning_rate
        self.reward_decay = reward_decay
        self.epsilon = epsilon
        self.q_table = {}
        self.coming_direction = {}
        self.deprecated_state = []
        self.last_action = None

    def exist(self, state: str) -> bool:
        return state in self.q_table.keys()

    def add_new_state(self, state: str):
        self.q_table[state] = [0] * 4
        if self.last_action != None:
            coming_direction = self.reverse_action(self.last_action)
            self.coming_direction[state] = coming_direction
            self.q_table[state][coming_direction] = -1

    def remove_action(self, action_reward_list, action: int):
        """
        Set it to -1 means never choose it again in this environment situation
        """
        action_reward_list[action] = -1

    def filter_action(self, action_reward_list: List[int]) -> List[int]:
        """
        Give the action_reward_list, return an avaiable action set.
        """
        filtered_action = []
        for action in range(len(action_reward_list)):
            if action_reward_list[action] != -1:
                filtered_action.append(action)
        return filtered_action

    def reverse_action(self, action: int) -> int:
        """reverse action"""
        UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
        if action == UP:
            return DOWN
        elif action == DOWN:
            return UP
        elif action == LEFT:
            return RIGHT
        elif action == RIGHT:
            return LEFT
        else:
            raise ValueError("action is not valid")

    def convert_to_tuple(self, state: str) -> Tuple[int, int]:
        return tuple(map(int, state.replace("(", "").replace(")", "").split(",")))

    def move(self, state: str, direction: int) -> str:
        UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
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
        coming_direction = self.coming_direction[state]
        reverse_direction = self.reverse_action(coming_direction)
        last_state = self.move(state, coming_direction)
        self.remove_action(self.q_table[last_state], reverse_direction)
        if np.max(self.q_table[last_state]) == -1:
            self.deprecated_state.append(last_state)
            self.update_neighbour(last_state)

    def make_decision(self, state: str) -> int:
        if not self.exist(state):
            self.add_new_state(state)
        action_reward_list = self.q_table[state]
        filtered_action = self.filter_action(action_reward_list)
        choice = np.random.choice(filtered_action)
        return choice

    def learn(self, state: str, action: int, reward: int, next_state: str):
        self.last_action = action
        if reward == 0:
            """
            reward == 0 means that the next_state is still a road
            so the best value of four direction of next_state should also be zero
            (Because we finish the process with reaching end only once,
            there's almost all the road that best value of four dir is zero)
            And because the reward of one direction is initialize with zero
            we can literally jump this meaningless calculation
            """
            if next_state not in self.q_table.keys():
                self.add_new_state(next_state)
        if reward == -1 or next_state in self.deprecated_state:
            """
            reward == -1 means that the next_state is wall/out-bound
            when agent choose to go random this time, it should also not
            choose a direction like this.
            """
            self.q_table[state][action] += (
                self.learning_rate
                * self.reward_decay
                * (-1 - self.q_table[state][action])
            )
            if np.max(self.q_table[state]) == -1:
                self.deprecated_state.append(state)
                self.update_neighbour(state)
