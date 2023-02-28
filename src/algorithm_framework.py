from threading import Event
from maze import Maze
from solver import Solver

"""
The Algorithm Framework of Reinforcement Learning in solving maze problem.

It takes in a maze and a solver (brain) and runs the algorithm.
"""


class AlgorithmFramework:
    def __init__(self):
        self.stop_event = Event()

    def start(self, maze: Maze, brain: Solver):
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
                if dead or success or self.stop_event.is_set():
                    break
            if success or self.stop_event.is_set():
                if success:
                    print("Maze solved.")
                else:
                    print("\nStopped.")
                break

    def stop(self):
        self.stop_event.set()
