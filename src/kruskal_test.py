"""
Maze generator using Kruskal's algorithm.
"""
from union_find_set import UnionFindSet
from typing import *
from maze_cli import Maze
from random import shuffle
import numpy as np


class Kruskal:
    def init(self):
        self.diameter = self.radius * 2 - 1
        self._set = UnionFindSet(self.radius * self.radius)
        self._edge_list = []
        self._path_matrix = np.zeros((self.diameter, self.diameter), dtype=bool)

    def generate_edge_set(self):
        """
        Generate all the edges in the maze.
        To fit in the union find set, the edges are represented by a tuple of two integer.
        Which means all the nodes are represent in an integer.
        (x, y) -> x * width + y
        """
        for x in range(self.radius):
            for y in range(self.radius):
                if y < self.radius - 1:
                    node1 = x * self.radius + y
                    node2 = x * self.radius + y + 1
                    self._edge_list.append((node1, node2))
                    # print(f"Connect ({x}, {y}) with ({x}, {y + 1})")
                if x < self.radius - 1:
                    node1 = x * self.radius + y
                    node2 = (x + 1) * self.radius + y
                    self._edge_list.append((node1, node2))
                    # print(f"Connect ({x}, {y}) with ({x+1}, {y})")

    def unite(self):
        while self._set.isAllUnited() is False:
            edge = self._edge_list.pop()
            if self._set.isUnited(edge[0], edge[1]) is False:
                self._set.unite(edge[0], edge[1])
                # print(f"Connect {edge[0]} with {edge[1]}")
                x = (edge[0] // self.radius) * 2
                y = (edge[0] % self.radius) * 2
                self._path_matrix[x][y] = True
                if abs(edge[0] - edge[1]) != self.radius:
                    # print(f"Connect ({x//2}, {y//2}) with ({x//2}, {y//2+1})")
                    self._path_matrix[x][y + 1] = True
                    self._path_matrix[x][y + 2] = True
                else:
                    # print(f"Connect ({x//2}, {y//2}) with ({x//2+1}, {y//2})")
                    self._path_matrix[x + 1][y] = True
                    self._path_matrix[x + 2][y] = True

    def generate_walls(self):
        self._walls = np.array([[-1, -1]])
        for x in range(self.diameter):
            for y in range(self.diameter):
                if not self._path_matrix[x][y]:
                    self._walls = np.append(self._walls, [[x, y]], axis=0)
        self._walls = self._walls[1:]

    def generate(self, radius):
        self.radius = radius
        self.init()
        self.generate_edge_set()
        shuffle(self._edge_list)
        self.unite()
        self.generate_walls()
        start_pos = (0, 0)
        end_pos = (self.diameter - 1, self.diameter - 1)
        width, height = self.diameter, self.diameter
        return Maze(width, height, start_pos, end_pos, self._walls)


if __name__ == "__main__":
    """
    Testing
    """
    kruskal = Kruskal()
    kruskal.generate(5)
