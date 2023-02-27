"""主程序文件"""

import sys
from main_window import *
from q_learning import *
from recursive_walk import RecursiveWalk
from kruskal import Kruskal

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


def algorithm_start(maze: Maze, brain: QLearning):
    while True:
        success = False
        dead = False
        maze.reset()
        state = str(maze.start_pos)
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
    # Maze
    # start_pos = (0, 0)
    # end_pos = (2, 4)
    # walls = np.array([[1, 0], [1, 1], [3, 1], [3, 2], [3, 3], [2, 3], [1, 3], [1, 4]])
    action_list = [UP, DOWN, LEFT, RIGHT]
    # Ui
    app = QApplication(sys.argv)
    window = MainWindow()

    # Algorithm
    # brain = QLearning(action_list)
    # threading.Thread(target=algorithm_start, args=(maze, brain)).start()
    sys.exit(app.exec())
