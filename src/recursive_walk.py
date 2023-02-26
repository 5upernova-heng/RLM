from random import shuffle, randrange
import numpy as np
from maze import Maze


class RecursiveWalk:
    def __init__(self):
        pass

    def make_maze(self, w, h):
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [["| "] * w + ["|"] for _ in range(h)] + [[]]
        hor = [["+-"] * w + ["+"] for _ in range(h + 1)]

        def walk(x, y):
            vis[y][x] = 1

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for xx, yy in d:
                if vis[yy][xx]:
                    continue
                if xx == x:
                    hor[max(y, yy)][x] = "+ "
                if yy == y:
                    ver[y][max(x, xx)] = "  "
                walk(xx, yy)

        walk(randrange(w), randrange(h))

        s = ""
        for a, b in zip(hor, ver):
            s += "".join(a + b)
        return s

    def generate(self, radius):
        (w, h) = (radius, radius)
        WIDTH = w * 2 - 1
        HEIGHT = h * 2 - 1
        walls = np.array([[-1, -1]])
        maz = self.make_maze(w, h)
        for i in range(1, WIDTH + 1):
            for j in range(1, HEIGHT + 1):
                # print(maz[i * (WIDTH + 2) + j], end = "")
                if maz[i * (WIDTH + 2) + j] != " ":
                    walls = np.append(walls, [[i - 1, j - 1]], axis=0)
            # print()
        # print(walls)
        walls = walls[1:]
        start_pos = (0, 0)
        end_pos = (0, 0)
        while 1:
            l = randrange(1, WIDTH + 1)
            r = randrange(1, HEIGHT + 1)
            if not (l == 1 and r == 1) and maz[l * (WIDTH + 2) + r] == " ":
                end_pos = (l - 1, r - 1)
                break
        # print(end_pos)
        return Maze(WIDTH, HEIGHT, start_pos, end_pos, walls)
