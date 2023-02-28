import pandas as pd
import numpy as np


class ValueIteration:
    def __init__(
        self,
        action_list,                    #MDP中所有可能动作的列表
        learning_rate: float = 0.01,    #更新Q值的学习率
        reward_decay: float = 0.9,      #奖励的折扣因子
        epsilon: float = 1,             #通过espilon-greedy来探索epsilon值
        max_iterations: int = 100,      #值迭代算法的最大迭代次数
        tolerance: float =0.01,         
        delta: float =0.2,              
        greatest:int =0
        
    ) -> None:
        self.action_list = action_list
        self.learning_rate = learning_rate
        self.reward_decay = reward_decay
        self.epsilon = epsilon
        self.max_iterations = max_iterations
        self.tolerance=tolerance
        self.delta=delta
        self.greatest=greatest
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


    def reverse_action(self, action: int) -> int:
        """返回给定动作的相反方向"""
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

    def remove_action(self, action_list, action: int):
        """从可能动作的列表中删除给定的动作"""
        if action in action_list:
            filtered_action_list = action_list.copy()
            filtered_action_list.remove(action)
            return filtered_action_list
        
    def make_decision(self, state: str) -> int:
        """使用epsilon-greedy探索选择执行的动作"""
        if not self.exist(state):
            self.add_new_state(state)
        action_reward_list = self.q_table.loc[state, :]
        best_choices = action_reward_list[
            action_reward_list == np.max(action_reward_list)
        ].index.tolist()
        # choice = np.random.choice(best_choices)

        #never look back
        if self.last_action is not None:
            self.remove_action(best_choices, self.reverse_action(self.last_action))
        
        choice = np.random.choice(best_choices)

        self.last_action = choice

        return choice    

    def learn(self, state: str, action: int, reward: int, next_state: str):
        """,使用贝尔曼方程更新给定状态-动作的Q值"""
        if not self.exist(next_state):
            self.add_new_state(next_state)
        while True:
            next_q_values = self.q_table.loc[next_state, :]
            max_q_value = np.max(next_q_values)
            if np.abs(max_q_value-(self.greatest))<self.delta:
                target_value = reward + self.reward_decay * max_q_value
                self.q_table.loc[state, action] += self.learning_rate * (
                    target_value - self.q_table.loc[state, action]
                )
                break
            else:
                self.greatest=max_q_value
                target_value = reward + self.reward_decay * max_q_value
                self.q_table.loc[state, action] += self.learning_rate * (
                    target_value - self.q_table.loc[state, action]
                )

            

                 
        
    

