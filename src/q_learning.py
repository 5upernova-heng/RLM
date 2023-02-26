import pandas as pd
import numpy as np


class QLearning:
    def __init__(
        self,
        action_list,
        learning_rate: float = 0.01,
        reward_decay: float = 0.9,
        epsilon: float = 1,
    ) -> None:
        self.action_list = action_list
        self.learning_rate = learning_rate
        self.reward_decay = reward_decay
        self.epsilon = epsilon
        self.q_table = pd.DataFrame(columns=action_list, dtype=np.float64)
        self.last_action = None

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

    def remove_action(self, action_list, action: int):
        if action in action_list:
            filtered_action_list = action_list.copy()
            filtered_action_list.remove(action)
            return filtered_action_list

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

    def make_decision(self, state: str) -> int:
        """通过 Q 表，对于现在所处状态做决策，选出最大回报的方向"""
        if not self.exist(state):
            self.add_new_state(state)
        if np.random.uniform() < self.epsilon:
            action_reward_list = self.q_table.loc[state, :]
            if self.last_action is not None:
                filtered_action_list = self.remove_action(
                    self.action_list, self.reverse_action(self.last_action)
                )
                action_reward_list = action_reward_list[filtered_action_list]
            best_choices = action_reward_list[
                action_reward_list == np.max(action_reward_list)
            ].index.tolist()
        else:
            best_choices = self.action_list
        # never look back
        if self.last_action is not None:
            self.remove_action(best_choices, self.reverse_action(self.last_action))
        choice = np.random.choice(best_choices)

        self.last_action = choice
        # action_str = {0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}
        # print(f"last_action: {action_str[self.last_action]}")
        # print(f"this_action: {action_str[choice]}")
        return choice

    def learn(self, state: str, action: int, reward: int, next_state: str):
        """走完一步就学习。
        利用走完之后的 reward 进行学习"""
        # It will not add state when it's dead
        predict_value = self.q_table.loc[state, action]
        if reward == 0:
            # road
            if not self.exist(next_state):
                self.add_new_state(next_state)
            fixed_value = (
                reward + self.reward_decay * self.q_table.loc[next_state, action]
            )  # 修正后的值
        else:
            # wall(-1) or end(1)
            fixed_value = reward
            # print(self.q_table)
        # learn
        self.q_table.loc[state, action] += self.learning_rate * (
            fixed_value - predict_value
        )  # 学习，更新刚刚那步的权重
