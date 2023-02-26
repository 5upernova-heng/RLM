"""迷宫类，包含迷宫的属性和方法

Agent: class
attribute: pos
method: change_pos(): change the position of agent

Maze
attributes:
start/end_pos: the start and end position
agent: a position of agent
width/height: the number of pixels of width and height
walls: a position list of
methods:
reset: move agent to the start point
move: pick a action from the action list, and change the state
is_dead: agent is dead or not
is_end: agent is reach the end or not
is_out_bound: agent is out of bound or not"""

from typing import Tuple
from PyQt6.QtCore import pyqtSignal, QObject
import numpy as np


class Agent:
    def __init__(self, start_pos) -> None:
        Agent.pos = start_pos

    def change_pos(self, new_pos):
        Agent.pos = new_pos


class Maze(QObject):
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

    move_finished = pyqtSignal()
    recover_Button = pyqtSignal()

    def get_agent_pos(self) -> Tuple[int, int]:
        return self.agent.pos

    def move(self, action: int) -> None:
        """移动 Agent 并检查是否结束或者撞墙，结束或者撞墙时返回 True"""
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
        self.move_finished.emit()

    def feedback(self) -> int:
        """获取反馈 (rewards)"""
        if self.isWall() or self.isOut():
            return -1
        if self.isEnd():
            # print("clicked")
            self.recover_Button.emit()
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
