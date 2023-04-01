"""
CLI test version of maze, without signals send to ui
"""
import numpy as np
from typing import *


class Agent:
    def __init__(self, start_pos) -> None:
        Agent.pos = start_pos

    def change_pos(self, new_pos):
        Agent.pos = new_pos


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        start_pos: Tuple[int, int],
        end_pos: Tuple[int, int],
        walls: np.array,
    ) -> None:
        super().__init__()
        self.agent = Agent(start_pos)
        self.width = width
        self.height = height
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.walls = walls
        self.iterations_num = 0

    def get_agent_pos(self) -> Tuple[int, int]:
        return self.agent.pos

    def move(self, action: int) -> None:
        x, y = self.agent.pos
        UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
        if action == UP:
            y -= 1
        if action == DOWN:
            y += 1
        if action == LEFT:
            x -= 1
        if action == RIGHT:
            x += 1
        self.agent.change_pos((x, y))

    def feedback(self) -> int:
        """获取反馈 (rewards)"""
        if self.isWall() or self.isOut():
            return -1
        if self.isEnd():
            return 1
        return 0

    def reset(self) -> None:
        """将 agent 移动到起点"""
        self.agent.change_pos(self.start_pos)

    def isWall(self) -> bool:
        x, y = self.agent.pos
        return ([x, y] == self.walls).all(1).any()

    def isEnd(self) -> bool:
        return self.agent.pos == self.end_pos

    def isOut(self) -> bool:
        x, y = self.agent.pos
        return x < 0 or x >= self.width or y < 0 or y >= self.height
