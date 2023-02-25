from random import shuffle, randrange
import numpy as np
def make_maze(w, h):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["| "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+-"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+ "
            if yy == y: ver[y][max(x, xx)] = "  "
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + b)
    return s


def generate_maze():
    rad = randrange(5, 10)
    (w, h) = (rad, rad)
    WIDTH = w * 2 - 1
    HEIGHT = h * 2 - 1
    walls = np.array([[-1, -1]])
    maz = make_maze(w, h)
    for i in range(1, WIDTH + 1):
        for j in range(1, HEIGHT + 1):
            #print(maz[i * (WIDTH + 2) + j], end = "")
            if(maz[i * (WIDTH + 2) + j] != ' '):
                walls = np.append(walls, [[i - 1, j - 1]], axis = 0 )
        #print()
    #print(walls)
    start_pos = (0, 0)
    end_pos = (0, 0)
    while(1):
        l = randrange(1, WIDTH + 1)
        r = randrange(1, HEIGHT + 1)
        if(not(l == 1 and r == 1) and maz[l * (WIDTH + 2) + r] == ' '):
            end_pos = (l - 1, r - 1)
            break
    #print(end_pos)
    return Maze(WIDTH, HEIGHT, start_pos, end_pos, walls)


