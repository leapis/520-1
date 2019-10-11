import numpy
from matplotlib import pyplot
import minesweeper
import random
import time
import sys

# This is a very useful array to iterate over for neighbors
surroundings = [
    (-1, -1), (-1,  0), (-1,  1),
    ( 0, -1),           ( 0,  1),
    ( 1, -1), ( 1,  0), ( 1,  1)
]

def reveal_cell(grid, mines, i, j):
    d = len(grid)

    clue = grid[i][j]
    if mines[i][j] == 0: # This represents a reveal, as its the first time we're accessing it
        if clue == -1: # This means we made a wrong reveal, either due to a bug or we resorted to a random guess
            mines[i][j] = -1
            print('Boom!', flush = True)
            return
            # explosions += 1
        else:
            mines[i][j] = 1

    # This loop should capture all possibilities of the children if this call revealing information this call could use
    for x in range(0, 3):
        mineNeighbors = 0
        safeNeighbors = 0
        unknownNeighbors = 8
        wallNeighbors = 0
        # Count the number of unknown, safe, and mine neighbors on the fly
        for offset in surroundings:
            oi, oj = offset
            if 0 <= i + oi < d and 0 <= j + oj < d:
                if mines[i + oi][j + oj] == -1:
                    mineNeighbors += 1
                    unknownNeighbors -= 1
                if mines[i + oi][j + oj] == 1:
                    safeNeighbors += 1
                    unknownNeighbors -= 1
            else:
                wallNeighbors += 1
        unknownNeighbors -= wallNeighbors
        print(j, i, clue, mineNeighbors, safeNeighbors, unknownNeighbors, flush = True)

        if clue - mineNeighbors == unknownNeighbors:
            for offset in surroundings:
                oi, oj = offset
                if 0 <= i + oi < d and 0 <= j + oj < d and mines[i + oi][j + oj] == 0:
                    mines[i + oi][j + oj] = -1
        if 8 - wallNeighbors - clue - safeNeighbors == unknownNeighbors:
            for offset in surroundings:
                oi, oj = offset
                if 0 <= i + oi < len(mines) and 0 <= j + oj < len(mines) and mines[i + oi][j + oj] == 0:
                    reveal_cell(grid, mines, i + oi, j + oj)

def sweep_grid(grid):
    d = len(grid)
    mines = numpy.zeros((d, d)) # 0 for covered, -1 for mine, 1 for safe

    done = False
    while not done:
        i = random.randint(0, d - 1)
        j = random.randint(0, d - 1)
        while mines[i][j] != 0:
            i = random.randint(0, d - 1)
            j = random.randint(0, d - 1)

        reveal_cell(grid, mines, i, j)

        pyplot.matshow(grid)
        pyplot.matshow(mines)
        pyplot.show()

        done = True
        # TODO: optimize?
        for i in range(0, d):
            for j in range(0, d):
                if mines[i][j] == 0:
                    done = False

def sweep_grid2(grid):
    explosions = 0
    d = len(grid)
    mines = numpy.zeros((d, d)) # 0 for covered, -1 for mine, 1 for safe
    clues = numpy.zeros((d, d)) # Clue in the given cell, should only be accessed for safe cells
    safeNeighbors = numpy.zeros((d, d)) # Number of neighbors known to be safe
    mineNeighbors = numpy.zeros((d, d)) # Number of nieghbors known to be a mine
    unknownNeighbors = numpy.zeros((d, d)) # Number of neighbors not yet known to be a mine or safe
    candidates = [] # Track every "dirty" cell that could give us new information. This way we're not sweeping the entire grid O(d^2) times

    # Start all unknownNeighbors at their correct value
    for i in range(d):
        for j in range(d):
            # clues[i][j] = -1 # This can be used for visualization, to see where the algorithm is working
            if i == 0 or i == d - 1:
                if j == 0 or j == d - 1:
                    unknownNeighbors[i][j] = 3
                else:
                    unknownNeighbors[i][j] = 5
            else:
                if j == 0 or j == d - 1:
                    unknownNeighbors[i][j] = 5
                else:
                    unknownNeighbors[i][j] = 8

    # Loop until every cell is identified as safe or as a mine
    done = False
    while not done:
        i = 0
        j = 0
        print(candidates)
        # If we have no candidates, find some that meet evaluation criteria
        if len(candidates) == 0:
            for k in range(0, d):
                for l in range(0, d):
                    if clues[k][l] - mineNeighbors[k][l] == unknownNeighbors[k][l] or 8 - clues[k][l] - safeNeighbors[k][l] == unknownNeighbors[k][l]:
                        candidates.append((k, l))

        if len(candidates) == 0:
            i = random.randint(0, d - 1)
            j = random.randint(0, d - 1)
            while mines[i][j] != 0:
                i = random.randint(0, d - 1)
                j = random.randint(0, d - 1)
        else:
            i, j = candidates.pop()
        print(i, j)

        clue = grid[i][j]
        if clue == -1: # This means we made a wrong reveal, either due to a bug or we resorted to a random guess
            mines[i][j] = -1
            print('Boom!')
            explosions += 1
        else:
            mines[i][j] = 1
            clues[i][j] = clue
        dirty_neighbors(mines, mineNeighbors, safeNeighbors, unknownNeighbors, i, j)
        evaluate_neighbors(mines, mineNeighbors, safeNeighbors, unknownNeighbors, i, j)

        if clues[i][j] - mineNeighbors[i][j] == unknownNeighbors[i][j]:
            for offset in surroundings:
                oi, oj = offset
                if 0 <= i + oi < len(mines) and 0 <= j + oj < len(mines) and mines[i + oi][j + oj] == 0:
                    mines[i + oi][j + oj] = -1
                    dirty_neighbors(mines, mineNeighbors, safeNeighbors, unknownNeighbors, i + oi, j + oj)
        if 8 - clues[i][j] - safeNeighbors[i][j] == unknownNeighbors[i][j]:
            for offset in surroundings:
                oi, oj = offset
                if 0 <= i + oi < len(mines) and 0 <= j + oj < len(mines) and mines[i + oi][j + oj] == 0:
                    candidates.append((i + oi, j + oj))

        print(mines)
        print(clues)
        print(mineNeighbors)
        print(safeNeighbors)
        print(unknownNeighbors)
        done = True
        # TODO: optimize?
        for i in range(0, d):
            for j in range(0, d):
                if mines[i][j] == 0:
                    done = False

    print("Explosions:", explosions)
    print(grid)

def dirty_neighbors(mines, mineNeighbors, safeNeighbors, unknownNeighbors, i, j):
    """ For use when mines[i][j] has just updated, requiring all neighbors to use evaluate_neighbors """
    for offset in surroundings:
        oi, oj = offset
        if 0 <= i + oi < len(mines) and 0 <= j + oj < len(mines):
            evaluate_neighbors(mines, mineNeighbors, safeNeighbors, unknownNeighbors, i + oi, j + oj)

def evaluate_neighbors(mines, mineNeighbors, safeNeighbors, unknownNeighbors, i, j):
    """ Sets the correct values in mineNeighbors, safeNeighbors, and unknownNeighbors at (i, j) given mines """
    mineNeighbors[i][j] = 0
    safeNeighbors[i][j] = 0
    unknownNeighbors[i][j] = (8 - (3 if (i == 0 or i == len(mines)) or (j == 0 or j == len(mines)) else 0) -
            (2 if (i == 0 or i == len(mines)) and (j == 0 or j == len(mines)) else 0))
    for offset in surroundings:
        oi, oj = offset
        if 0 <= i + oi < len(mines) and 0 <= j + oj < len(mines):
            if mines[i + oi][j + oj] == -1:
                mineNeighbors[i][j] += 1
                unknownNeighbors[i][j] -= 1
            if mines[i + oi][j + oj] == 1:
                safeNeighbors[i][j] += 1
                unknownNeighbors -= 1

if __name__ == '__main__':
    numpy.set_printoptions(formatter = {'all': lambda x: (' ' if x >= 0 else '') + str(int(x))})
    grid = minesweeper.generate_environment(20, 15) # 10 x 10 with 15 mines
    sweep_grid(grid)
