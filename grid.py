import numpy as np
import random

FIRE = 1
BLOCKED = -1
UNBLOCKED = 0

def generateGrid(dimm, p):
    """
    generate grid, where each element besides the first and last is randomly assigned either one or zero, depending on probability measure p
    IMPORTANT NOTE: grid will be accessed via (y,x), not (x,y), and the direction of y is reversed from a traditional plot
    @params dimm: dimension of grid, p: probability measure of blocking elements
    @return grid
    """
    grid = np.zeros((dimm, dimm))
    for row in grid:
        for i, element in enumerate(row):
            if (random.random() < p):
                row[i] = BLOCKED
            else:
                row[i] = UNBLOCKED
    #make sure start and goal are free!
    grid[0][0] = UNBLOCKED
    grid[dimm-1][dimm-1] = UNBLOCKED
    return grid

def generateSolvableGrid(dimm, p, algorithm):
    grid = generateGrid(dimm, p)
    solved, _, _ = algorithm(grid, (0, 0), (dimm-1, dimm-1))
    while not solved:
        grid = generateGrid(dimm, p)
        solved, _, _ = algorithm(grid, (0, 0), (dimm-1, dimm-1))

    return grid

def generateFireGrid(dimm, p):
    """
    return a grid with fire in the top right corner
    """
    grid = generateGrid(dimm, p)
    #Note: we don't check here for diagonal accuracy. That is done in our driver code
    grid[0][dimm-1] = FIRE
    grid[dimm-1][0] = UNBLOCKED
    return grid

def grid_copy(grid):
    """
    retun a copy of a given grid
    """
    dimm = len(grid)
    newGrid = np.zeros((dimm, dimm))
    for i in range(dimm):
        for j in range(dimm):
            newGrid[i][j] = grid[i][j]
    return newGrid

def main():
    """Testing method"""
    print("Testing grid.py")
    grid = generateGrid(10, .5)
    print(grid)

if (__name__ == "__main__"): main()
