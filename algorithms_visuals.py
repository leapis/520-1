import algorithms as algos
import heuristics as h
import grid as gd
from matplotlib import pyplot


def plotSearchAlgorithms(dim, p):
    start = (0, 0)
    goal = (dim-1, dim-1)
    grid = gd.generateGrid(dim, p)

    solved = [False for _ in range(5)]

    solved[0], DFSPath = algos.DFS(grid, start, goal)
    solved[1], BFSPath, _ = algos.BFS(grid, start, goal)
    solved[2], BDBFSPath = algos.BDBFS(grid, start, goal)
    solved[3], AStarPathEuclidean, _ = algos.aStar(grid, start, goal, h.Euc)
    solved[4], AStarPathManhattan, _ = algos.aStar(grid, start, goal, h.Manhattan)

    paths = {
        "DFS": DFSPath, "BFS": BFSPath, "BDBFS": BDBFSPath,
        "A* Euclidean": AStarPathEuclidean, "A* Manhattan": AStarPathManhattan
    }

    # if solvable, then all search algorithms should work, and so plot all of them one at a time
    if all(solved):
        print("Close window after each search algorithm to see next one")
        for i, path in enumerate(paths):
            print(path)
            for y, x in paths.get(path):
                grid[y][x] = 3
            pyplot.matshow(grid)
            pyplot.title(path)
            pyplot.show()
            for y, x in paths.get(path):
                grid[y][x] = 0
    # otherwise just show the unsolvable grid
    else:
        pyplot.matshow(grid)
        pyplot.title("Unsolvable")
        pyplot.show()


if __name__ == "__main__":
    plotSearchAlgorithms(100, 0.2)
