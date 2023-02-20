import pandas as pd
import numpy as np


class Q_Learning:
    def __init__(
        self, action_list, learning_rate=0.01, reward_decay=0.9, epsilon=0.9
    ) -> None:
        self.action_list = action_list
        self.learning_rate = learning_rate
        self.reward_decay = reward_decay
        self.epsilon = epsilon
        self.q_table = pd.DataFrame(columns=action_list, dtype=np.float64)

    def exist(self, state: str) -> bool:
        """检测目前 Q 表中是否存在 state 状态"""
        return state in self.q_table.index

    def add_new_state(self, state: str):
        """为 Q 表添加新状态"""
        new_row = pd.DataFrame(
            data=np.array([0] * len(self.action_list)).reshape(1, 4),
            index=[state],
            columns=self.action_list,
            dtype=np.float64,
        )
        self.q_table = pd.concat([self.q_table, new_row])

    def make_decision(self, state: str) -> int:
        """通过 Q 表，对于现在所处状态做决策，选出最大回报的方向"""
        if not self.exist(state):
            self.add_new_state(state)
        if np.random.uniform() < self.epsilon:
            action_reward_list = self.q_table.loc[state, :]
            choice = np.random.choice(
                action_reward_list[
                    action_reward_list == np.max(action_reward_list)
                ].index
            )
        else:
            choice = np.random.choice(self.action_list)
        return choice

    def learn(self, state: str, action: int, reward: int, next_state: str):
        """走完一步就学习。
        利用走完之后的 reward 进行学习"""
        if not self.exist(next_state):
            self.add_new_state(next_state)
        predict = self.q_table.loc[state, action]
        if reward == 0:
            # 还是路
            fixed = (
                reward + self.reward_decay * self.q_table.loc[next_state, action]
            )  # 修正后的值
        else:
            # 墙（-1）或者终点（1）
            fixed = reward
        self.q_table.loc[state, action] += self.learning_rate * (
            fixed - predict
        )  # 学习，更新刚刚那步的权重
