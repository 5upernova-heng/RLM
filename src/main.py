from main_window import MainWindow

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()


if __name__ == "__main__":
    main()
