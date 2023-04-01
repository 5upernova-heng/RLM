import pandas as pd
from maze_cli import Maze
from solver import Solver
from q_learning import QLearning
from sarsa import SARSA
from value_iteration import ValueIteration
from policy_iteration import PolicyIteration
from kruskal_test import Kruskal
from rich import print
from tqdm import tqdm
from typing import *

import multiprocessing

"""
The Algorithm Framework of Reinforcement Learning in solving maze problem.
It takes in a maze and a solver (brain) and runs the algorithm.

The CLI version for generating statistics and testing
"""

name_map = {
    QLearning: "Q_Learning",
    SARSA: "SARSA",
    ValueIteration: "Value_Iteration",
    PolicyIteration: "Policy_Iteration",
}
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
action_list = [UP, DOWN, LEFT, RIGHT]


class AlgorithmTester:
    def __init__(self):
        self.iteration_time = 0

    def start(self, maze: Maze, brain: Solver):
        self.iteration_time = 0
        while True:
            success = False
            dead = False
            maze.reset()
            self.iteration_time += 1
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
                return self.iteration_time


def run_test_case(case: Maze, brain: Solver):
    return AlgorithmTester().start(case, brain)


def run_test_case_wrapper(args):
    return run_test_case(*args)


def run_tests(test_cases: List[Maze], brain: Solver):
    results = []
    args_list = []
    for case in test_cases:
        args_list.append((case, brain))
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    with tqdm(total=len(test_cases)) as progress_bar:
        for i, result in enumerate(pool.imap(run_test_case_wrapper, args_list)):
            results.append(result)
            progress_bar.update()
    pool.close()
    pool.join()
    return results


def create_test_cases(num: int, radius: int):
    return [Kruskal().generate(radius) for i in range(num)]


def test(algo_list: List[Solver], radius_range: List[int], num: int):
    """
    Test each algorithm with the same range with specific maze count of each radius
    """
    for algo in algo_list:
        algo_name = name_map[algo]
        print("Testing Algorithm: ", algo_name)
        data = {}
        for radius in radius_range:
            print("Maze radius:", radius)
            test_cases = create_test_cases(num, radius)
            data[radius] = run_tests(test_cases, algo(action_list))
        print("Testing complete:", algo_name)
        pd.DataFrame(data=data).to_csv("%s.csv" % algo_name)


if __name__ == "__main__":
    test(
        algo_list=[ValueIteration],
        radius_range=[i for i in range(4, 40)],
        num=1,
    )
