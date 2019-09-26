import algorithms as algo
import heuristics as h
import grid as gd
import math
import random as rand
import sys
import numpy as np

def main():
    graphDimVsSolv()

def graphDimVsSolv():
    runs = 10000
    p = 0.05
    upper = 50
    min = 2 #const
    solveCount = [0 for _ in range(upper - min + 1)]
    print(len(solveCount))
    for i in range(min, upper + 1):
        solveCount[i-min] = {}
        f = open(sys.argv[1], "a+")
        f.write(str(i) + "\t")
        for p in np.arange(0, 0.5, 0.05):
            solveCount[i-min][p] = 0
            for _ in range(runs):
                dimm = i
                start = (0,0)
                goal = (dimm-1,dimm-1)
                grid = gd.generateGrid(dimm, p)
                solved, *rest = algo.DFS(grid, start, goal) #, h.Manhattan)
                if(solved):
                    solveCount[i-min][p] += 1
            print("Finished", i, "with a rate of", solveCount[i-min][p]/runs)
            f.write(str(solveCount[i-min][p]/runs) + "\t")
        f.write("\n")


if(__name__ == "__main__"): main()