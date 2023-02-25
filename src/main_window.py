"""界面的逻辑结构构建
    比如：按钮的逻辑
    画迷宫的逻辑等"""

import sys
from main_window_ui import *
from PyQt6.QtWidgets import *


class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()

    def draw():
        """def draw(self, maze(height, width, agent_pos, drawType, ...)):
        通过迷宫数据画出迷宫
        canvas.frameGeometry(), drawEvent(), ..."""

    def start(self):
        """开始算法, 并禁用 comboBox 和 start 按钮
        setEnable(False)"""

    def change_algorithm(self):
        """根据 comboBox 里面的 Text, 改变当前使用的算法"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
