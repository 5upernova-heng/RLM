from solver import Solver
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

    def make_decision(self, state: str) -> int:
        self.check_state_exist(state)
        # action selection
        if np.random.rand() < self.epsilon:
            # choose best action
            state_action = self.q_table[state]
            best_actions = [
                action
                for action in self.action_list
                if state_action[action] == max(state_action.values())
            ]
            action = np.random.choice(best_actions)
        else:
            # choose random action
            action = np.random.choice(self.action_list)
        return action

    def learn(self, state: str, action: int, reward: int, next_state: str):
        self.check_state_exist(next_state)
        q_predict = self.q_table[state][action]
        next_action = self.make_decision(next_state)
        if next_state != "terminal":
            q_target = reward + self.gamma * self.q_table[next_state][next_action]
        else:
            q_target = reward
        self.q_table[state][action] += self.lr * (q_target - q_predict)
