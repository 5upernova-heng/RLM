"""主程序文件"""


import numpy as np
from MainWindow import *
from Maze import *
from QLearning import *

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
LOOP_TIME = 1000


def algorithm_start(maze: Maze, brain: QLearning):
    for i in range(LOOP_TIME):
        success = False
        dead = False
        maze.reset()
        state = str(start_pos)
        while True:
            action = brain.make_decision(state)
            maze.move(action)
            next_state = str(maze.get_agent_pos())
            reward = maze.feedback()
            brain.learn(state, action, reward, next_state)
            state = next_state
            success = True if reward == 1 else False
            dead = True if reward == -1 else False
            if dead or success:
                break
        if success:
            print("Maze solved.")
            break


if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # window = MainWindow()
    start_pos = (0, 0)
    end_pos = (2, 4)
    walls = np.array([[1, 0], [1, 1], [3, 1], [3, 2],
                     [3, 3], [2, 3], [1, 3], [1, 4]])
    action_list = [UP, DOWN, LEFT, RIGHT]
    maz = Maze(5, 5, start_pos, end_pos, walls)
    brain = QLearning(action_list)
    algorithm_start(maz, brain)
    # app.exec()
