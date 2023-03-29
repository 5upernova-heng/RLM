"""
Value Iteration Method

"""
from solver import Solver
from typing import *
import random
import numpy as np

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

# value_table 用来保存状态价值表
# policy 一个字典，用来保存策略表
# left_action 一个字典，对应于每一个state，保留还可以选择的动作，（去除墙和边界）
# action_list 保存4个动作，UP DOWN LEFT RIGHT
# action_value 定义字典，key为状态state，value是一个列表，记录四个状态


class ValueIteration(Solver):
    def __init__(
        self, action_list: List[int], gamma: float = 1.0
    ) -> None:  # gamma 表示折扣因子
        self.action_list = action_list
        self.gamma = gamma
        self.policy = {}
        self.value_table = {}
        self.left_action = {}
        self.action_value = {}

    def add_state(self, state: str) -> None:  # 添加新状态进去
        self.value_table[state] = 0

    def add_action_list(self, state: str) -> None:  # 为新的状态创建一个四元组，记录action_value
        newlist = [-1000.0] * 4
        self.action_value[state] = newlist

    def make_decision(self, state: str) -> int:
        if state in self.policy.keys():
            return self.policy[state]
        else:
            if state in self.value_table.keys():
                this_list = self.left_action[state]
                return random.choice(this_list)
            else:  # 此时表示为新状态，需要添加进去
                self.add_state(state)
                self.left_action[state] = [UP, DOWN, LEFT, RIGHT]  # 为新状态创建一个剩余可选动作的四元组

                # 为新状态的动作价值创建四元组，用于迭代
                self.add_action_list(state)
                random_action = random.choice(self.left_action[state])
                return random_action

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

    def learn(self, state: str, action: int, reward: int, next_state: str):
        probability = 1.0
        if next_state not in self.value_table:
            self.add_state(next_state)
            self.add_action_list(next_state)
            # 为新状态创建一个剩余可选动作的四元组
            self.left_action[next_state] = [UP, DOWN, LEFT, RIGHT]

        new_value = reward + self.gamma * probability * (self.value_table[next_state])
        self.action_value[state][action] = new_value
        max_value = np.max(self.action_value[state])
        min_value = np.min(self.action_value[state])
        if min_value != -1000.0:
            self.value_table[state] = max_value

        if self.action_value[state][action] == -1.0:
            if action in self.left_action[state]:
                self.left_action[state].remove(action)

        elif reward == 0:
            reverse = self.reverse_action(action)
            if reverse in self.left_action[next_state]:
                self.left_action[next_state].remove(reverse)

        if len(self.left_action[state]) == 1:
            self.policy[state] = self.left_action[state][0]
