from solver import Solver
import numpy as np
from typing import *
import numpy as np


class SARSA(Solver):
    def __init__(self, action_list, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.action_list = action_list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy

        self.q_table = {}

    def check_state_exist(self, state):
        if state not in self.q_table.keys():
            # append new state to q table
            self.q_table[state] = {}
            for action in self.action_list:
                self.q_table[state][action] = 0.0


class SARSA(Solver):
    def __init__(self, action_list, learning_rate=1, reward_decay=1, e_greedy=0.9):
        self.action_list = action_list
        self.learning_rate = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy

        self.last_action = None
        self.deprecated_state = []
        self.coming_direction = {}
        self.q_table = {}

    def add_new_state(self, state: str):
        self.q_table[state] = [0] * 4
        if self.last_action != None:
            coming_direction = self.reverse_action(self.last_action)
            self.coming_direction[state] = coming_direction
            self.q_table[state][coming_direction] = -1

    def check_state_exist(self, state: str):
        """
        make sure that state are in the q_table
        """
        if state not in self.q_table.keys():
            # append new state to q table
            self.add_new_state(state)

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

    def remove_action(self, action_reward_list, action: int):
        """
        Set it to -1 means never choose it again in this environment situation
        """
        action_reward_list[action] = -1

    def update_neighbour(self, state: str):
        coming_direction = self.coming_direction[state]
        reverse_direction = self.reverse_action(coming_direction)
        last_state = self.move(state, coming_direction)
        self.remove_action(self.q_table[last_state], reverse_direction)
        if np.max(self.q_table[last_state]) == -1:
            self.deprecated_state.append(last_state)
            self.update_neighbour(last_state)

    def make_decision(self, state: str) -> int:
        self.check_state_exist(state)
        # action selection
        state_action = self.q_table[state]
        allowed_actions = [
            action for action in self.action_list if state_action[action] != -1
        ]
        action = np.random.choice(allowed_actions)
        return action

    def learn(self, state: str, action: int, reward: int, next_state: str):
        self.last_action = action
        self.check_state_exist(next_state)

        if reward == -1 or next_state in self.deprecated_state:
            self.q_table[state][action] = -1

        if np.max(self.q_table[state]) == -1:
            self.deprecated_state.append(state)
            self.update_neighbour(state)
