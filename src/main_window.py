"""界面的逻辑结构构建
    比如：按钮的逻辑
    画迷宫的逻辑等"""

from main_window_ui import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from maze import Maze


class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self, maze: Maze) -> None:
        super(MainWindow, self).__init__()
        self.maze = maze
        self.maze.move_finished.connect(self.update)
        self.setupUi(self)
        self.show()

    def paintEvent(self, event) -> None:
        painter = QPainter()
        painter.begin(self)
        canvas_rect = self.canvas.frameGeometry()
        grid_size = min(
            canvas_rect.width() // self.maze.width,
            canvas_rect.height() // self.maze.height,
        )
        canvas_center = canvas_rect.center()
        if self.maze.width % 2 == 0:
            x_start = canvas_center.x() - grid_size * (self.maze.width // 2)
            y_start = canvas_center.y() - grid_size * (self.maze.height // 2)
        else:
            x_start = (
                canvas_center.x() - grid_size * (self.maze.width // 2) - grid_size // 2
            )
            y_start = (
                canvas_center.y() - grid_size * (self.maze.height // 2) - grid_size // 2
            )
        # horizontal lines
        for i_line in range(self.maze.width + 1):
            x = x_start + i_line * grid_size
            painter.drawLine(x, y_start, x, y_start + self.maze.height * grid_size)

        # vertical lines
        for i_line in range(self.maze.height + 1):
            y = y_start + i_line * grid_size
            painter.drawLine(x_start, y, x_start + self.maze.width * grid_size, y)

        # walls
        for pos in self.maze.walls:
            x = x_start + pos[0] * grid_size
            y = y_start + pos[1] * grid_size
            painter.fillRect(x, y, grid_size, grid_size, Qt.GlobalColor.black)

        # end
        dest_x, dest_y = self.maze.end_pos
        dest_x = x_start + dest_x * grid_size
        dest_y = y_start + dest_y * grid_size
        dest_margin = grid_size // 10
        painter.fillRect(
            dest_x + dest_margin,
            dest_y + dest_margin,
            grid_size - 2 * dest_margin,
            grid_size - 2 * dest_margin,
            Qt.GlobalColor.green,
        )

        # agent
        agent_x, agent_y = self.maze.agent.pos
        agent_x = x_start + agent_x * grid_size
        agent_y = y_start + agent_y * grid_size
        agent_margin = grid_size // 6
        painter.fillRect(
            agent_x + agent_margin,
            agent_y + agent_margin,
            grid_size - 2 * agent_margin,
            grid_size - 2 * agent_margin,
            Qt.GlobalColor.red,
        )

    def start(self):
        """开始算法, 并禁用 comboBox 和 start 按钮
        setEnable(False)"""

    def change_algorithm(self):
        """根据 comboBox 里面的 Text, 改变当前使用的算法"""
