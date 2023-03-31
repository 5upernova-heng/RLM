"""界面的逻辑结构构建
    比如：按钮的逻辑
    画迷宫的逻辑等"""

from main_window_ui import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from algorithm_framework import AlgorithmFramework
from q_learning import QLearning
from sarsa import SARSA
from value_iteration import ValueIteration
from policy_iteration import PolicyIteration

from recursive_walk import RecursiveWalk
from kruskal import Kruskal
from typing import *
import threading

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
action_list = [UP, DOWN, LEFT, RIGHT]
rl_algorithm_list = {
    "Q_Learning": QLearning,
    "SARSA": SARSA,
    "Policy Iteration": PolicyIteration,
    "Value Iteration": ValueIteration,
}
maze_generator_list = {"Recursive Walk": RecursiveWalk, "Kruskal": Kruskal}


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.maze_generator = maze_generator_list[
            self.maze_generator_combo_box.currentText()
        ]()
        self.maze = self.maze_generator.generate(self.maze_radius_spin_box.value())
        self.rlm = AlgorithmFramework()
        self.showRoutine = False
        self.routine = []
        self.bind_signal()
        self.show()

    def bind_signal(self):
        self.start_button.clicked.connect(self.start)
        self.generate_maze_button.clicked.connect(self.new_maze)
        self.rl_algorithm_combo_box.currentTextChanged.connect(self.change_rl_algorithm)
        self.maze_generator_combo_box.currentIndexChanged.connect(
            self.change_maze_generator
        )
        self.maze.move_finished.connect(self.update)
        self.maze.recover_Button.connect(self.recover)
        self.maze.iterate_finished.connect(self.iteration_terminated)

    def draw_maze(self, painter: QPainter) -> None:
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

    def draw_action(
        self,
        x: int,
        y: int,
        action: int,
        grid_size: int,
        line_width: int,
        painter: QPainter,
    ) -> Tuple[int, int]:
        COLOR = Qt.GlobalColor.blue
        if action == UP:
            x_start = x - line_width
            y_start = y - grid_size - line_width
            painter.fillRect(
                x_start, y_start, 2 * line_width, grid_size + 2 * line_width, COLOR
            )
            return x, y - grid_size
        if action == DOWN:
            x_start = x - line_width
            y_start = y - line_width
            painter.fillRect(x_start, y_start, 2 * line_width, grid_size, COLOR)
            return x, y + grid_size
        if action == LEFT:
            x_start = x - grid_size - line_width
            y_start = y - line_width
            painter.fillRect(
                x_start, y_start, grid_size + 2 * line_width, 2 * line_width, COLOR
            )
            return x - grid_size, y
        if action == RIGHT:
            x_start = x - line_width
            y_start = y - line_width
            painter.fillRect(x_start, y_start, grid_size, 2 * line_width, COLOR)
            return x + grid_size, y
        if action < 0 or action > 3:
            print(action)

    def draw_routine(self, painter: QPainter, routine: List[int]) -> None:
        """draw out the routine"""
        canvas_rect = self.canvas.frameGeometry()
        grid_size = min(
            canvas_rect.width() // self.maze.width,
            canvas_rect.height() // self.maze.height,
        )
        canvas_center = canvas_rect.center()
        if self.maze.width % 2 == 0:
            x = canvas_center.x() - grid_size * (self.maze.width // 2) + grid_size // 2
            y = canvas_center.y() - grid_size * (self.maze.height // 2) + grid_size // 2
        else:
            x = canvas_center.x() - grid_size * (self.maze.width // 2)
            y = canvas_center.y() - grid_size * (self.maze.height // 2)
        line_width = grid_size // 8
        for action in routine:
            x_next, y_next = self.draw_action(
                x, y, action, grid_size, line_width, painter
            )
            x = x_next
            y = y_next

    def paintEvent(self, event) -> None:
        painter = QPainter()
        painter.begin(self)
        self.draw_maze(painter)
        if self.showRoutine:
            self.draw_routine(painter, self.routine)
            # print(self.routine)
        painter.end()

    def start(self):
        self.iteration_time_label.setText("")
        self.start_button.setText("Stop")
        self.start_button.clicked.disconnect(self.start)
        self.start_button.clicked.connect(self.stop)
        self.generate_maze_button.setEnabled(False)
        self.rl_algorithm_combo_box.setEnabled(False)
        self.maze_generator_combo_box.setEnabled(False)
        self.brain = rl_algorithm_list[self.rl_algorithm_combo_box.currentText()](
            action_list
        )
        self.rlm = AlgorithmFramework()
        self.algo_thread = threading.Thread(
            target=self.rlm.start, args=(self.maze, self.brain)
        )
        self.algo_thread.start()

    def stop(self):
        self.rlm.stop()
        self.algo_thread.join()
        self.recover()

    def recover(self):
        self.start_button.setText("Start")
        self.start_button.clicked.disconnect(self.stop)
        self.start_button.clicked.connect(self.start)
        self.start_button.setEnabled(True)
        self.generate_maze_button.setEnabled(True)
        self.rl_algorithm_combo_box.setEnabled(True)
        self.maze_generator_combo_box.setEnabled(True)

    def change_rl_algorithm(self):
        self.brain = rl_algorithm_list[self.rl_algorithm_combo_box.currentText()](
            action_list
        )

    def change_maze_generator(self):
        self.maze_generator = maze_generator_list[
            self.maze_generator_combo_box.currentText()
        ]()

    def iteration_terminated(self, iteration_time: int, routine: List[int]):
        self.iteration_time_label.setText(
            f"Agent has iterate: {str(iteration_time)} times"
        )
        self.showRoutine = True
        self.routine = routine

    def new_maze(self):
        self.routine = []
        self.showRoutine = False
        self.maze.iterate_finished.disconnect(self.iteration_terminated)
        self.maze.move_finished.disconnect(self.update)
        self.maze.recover_Button.disconnect(self.recover)
        self.maze_generator = maze_generator_list[
            self.maze_generator_combo_box.currentText()
        ]()
        self.maze = self.maze_generator.generate(self.maze_radius_spin_box.value())
        self.maze.move_finished.connect(self.update)
        self.maze.recover_Button.connect(self.recover)
        self.maze.iterate_finished.connect(self.iteration_terminated)
        self.update()
