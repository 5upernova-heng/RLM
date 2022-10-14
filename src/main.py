import time

import numpy as np
import sys
from settings import *
from PyQt6.QtWidgets import QApplication
from maze import Maze
from rl import Q_Learning

WIDTH = 5
HEIGHT = 5
LOOP_TIME = 1000

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_pos = (0, 0)
    end_pos = (2, 4)
    walls = np.array([[1, 0], [1, 1], [3, 1], [3, 2],
                     [3, 3], [2, 3], [1, 3], [1, 4]])
    maz = Maze(WIDTH, HEIGHT, start_pos, end_pos, walls)
    brain = Q_Learning(action_list)
    # loop and learn
    for i in range(LOOP_TIME):
        success = False
        print(i)
        maz.reset()
        state = start_pos
        while True:
            # The key of each state is simply string itself
            action = brain.make_decision(str(state))
            reward = maz.move(action)
            next_state = maz.get_agent_pos()
            brain.learn(str(state), action, reward, str(next_state))
            state = next_state
            if reward != 0:
                if reward == 1:
                    print("First success at Round", i)
                    success = True
                break
        if success:
            break
    sys.exit(app.exec())
