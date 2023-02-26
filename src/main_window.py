"""界面的逻辑结构构建
    比如：按钮的逻辑
    画迷宫的逻辑等"""

from main_window_ui import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from maze import *
from q_learning import *
from maze_maker import *
from main import algorithm_start
import threading

UP,DOWN,LEFT,RIGHT = 0,1,2,3
action_list = [UP, DOWN, LEFT, RIGHT]
algorithm_list = {"Q_Learning": "QLearning", "Sarsa": "Sarsa"}

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, maze: Maze) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.maze = maze
        self.brain = QLearning(action_list)
        # self.dead_time=0
        
        self.spinBox.setMinimum(5)
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.new_maze)
        self.comboBox.currentTextChanged.connect(self.change_algorithm)
        self.maze.move_finished.connect(self.update)
        self.maze.recover_Button.connect(self.recover)
        # self.maze.dead_happen.connect(self.dead_time_calculate)
        self.show()

    def paintEvent(self, event) -> None:
        painter = QPainter()
        painter.begin(self)
        # print("clicked")
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
        painter.end()
        

    def start(self,brain):
        self.pushButton.setEnabled(False)
        self.comboBox.setEnabled(False)
        self.pushButton_2.setEnabled(False)

        self.dead_time=0

        threading.Thread(target=algorithm_start, args=(self.maze,self.brain)).start()

    def recover(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.comboBox.setEnabled(True)

    def change_algorithm(self):
        self.brain=algorithm_list[self.comboBox.currentText()](action_list)

    # def dead_time_calculate(self):
    #     self.dead_time=self.dead_time+1
    #     self.label.setText("Dead Time: "+str(self.dead_time))
        

    def new_maze(self):
        # self.maze.dead_happen.disconnect(self.dead_time_calculate)
        self.maze.move_finished.disconnect(self.update)
        self.maze.recover_Button.disconnect(self.recover)
        self.maze=generate_maze(self.spinBox.value())
        self.maze.move_finished.connect(self.update)
        self.maze.recover_Button.connect(self.recover)
        # self.maze.dead_happen.connect(self.dead_time_calculate)
        self.update()

        
