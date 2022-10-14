import sys
import numpy as np
from agent import *
from settings import *
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt


class Maze(QMainWindow):
    def __init__(self, width, height, start_pos, end_pos, walls) -> None:
        super().__init__()
        self.agent = agent(start_pos)
        self.width = width
        self.height = height
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.walls = walls
        self.draw()

    def get_agent_pos(self):
        return self.agent.get_pos()

    def draw(self):
        """用 PyQt 库画出迷宫"""
        self.setGeometry(0, 0, self.width * GRID_SIZE, self.height * GRID_SIZE)
        self.show()

    def paintEvent(self, event) -> None:
        painter = QPainter()
        painter.begin(self)
        for i in range(self.width):
            x = i * GRID_SIZE
            painter.drawLine(x, 0, x, self.height * GRID_SIZE)
        for i in range(self.height):
            y = i * GRID_SIZE
            painter.drawLine(0, y, self.width * GRID_SIZE, y)
        for pos in self.walls:
            painter.fillRect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE,
                             GRID_SIZE, GRID_SIZE, Qt.GlobalColor.black)
        x, y = self.agent.pos
        painter.fillRect(x * GRID_SIZE, y * GRID_SIZE,
                         GRID_SIZE, GRID_SIZE, Qt.GlobalColor.red)
        painter.end()

    def move(self, dir):
        """移动 Agent 并检查是否结束或者撞墙，结束或者撞墙时返回 True"""
        x, y = self.agent.pos
        if dir == UP:
            y -= 1
        if dir == DOWN:
            y += 1
        if dir == LEFT:
            x -= 1
        if dir == RIGHT:
            x += 1
        self.agent.change_pos((x, y))
        self.repaint()
        reward = 0
        if self.isWall() or self.isOut():
            reward = -1
        if self.isEnd():
            reward = 1
        return reward

    def reset(self):
        self.agent.change_pos(self.start_pos)

    def isWall(self):
        x, y = self.agent.get_pos()
        return ([x, y] == self.walls).all(1).any()

    def isEnd(self):
        return self.agent.get_pos() == self.end_pos

    def isOut(self):
        x, y = self.agent.get_pos()
        return x < 0 or x >= self.width or y < 0 or y >= self.height
