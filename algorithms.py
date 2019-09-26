import numpy as np
import grid as gd
from matplotlib import pyplot
import random
import math

def hardestDFSMaze(dimm):
    """
    Attempts to find the maze that causes DFS to have the largest fringe
    @params dimm: the dimension of the desired maze
    @return The hardest maze
    """
    bestFringe = 0
    bestMaze = []
    for i in range(8): #Random restart loop. We will take the best maximum out of every restart
        print(i, flush=True)
        maze = gd.generateSolvableGrid(dimm, .3, DFS)
        largestFringe = 0
        hardestMaze = maze
        time = 1
        while time < 20000: #This is our search loop, we have this many iterations to find a local maximum
            _, path, fringeSize = DFS(maze, (0, 0), (dimm-1, dimm-1))
            #This if represents taking a step into a new state in our local search
            #We always step forward if its better, or with the simulated annealing probability function discussed in class
            if fringeSize >= largestFringe or random.random() < math.exp(-abs(fringeSize - largestFringe) * time / 200):
                largestFringe = fringeSize
                hardestMaze = maze

            maze = mutateMaze(maze, DFS, path)
            time += 1

        #This tracks the best local maximum we've found so far
        if largestFringe > bestFringe:
            bestFringe = largestFringe
            bestMaze = hardestMaze

    return hardestMaze

def mutateMaze(maze, algorithm, path):
    """
    Changes the given maze by changing either a space to a wall or a wall to a space
    @params maze: given maze to be mutate, algorithm: which algorithm to use to check solvability,
        path: current path (to be used to influence mutation)
    @return the new maze
    """
    dimm = len(maze)-1
    #This loop keeps us from creating an unsolvable maze, it returns once it finds a solvable one
    while True:
        newMaze = maze.copy()
        x = 0
        y = 0
        #This loop attempts to find a random place in the maze to mutate that won't violate any rules
        while x == 0 and y == 0 or x == dimm and y == dimm or x < 0 or y < 0 or x > dimm or y > dimm:
            if random.random() < 0.8: #Take a purely random location
                x = random.randint(0, dimm)
                y = random.randint(0, dimm)
            else: #Take a location near the current path, since a mutation there is more likely to increase maze difficulty
                deviation = [(0, 0), (0, 1), (1, 0), (-1, 0), (0, -1)]
                x, y = tuple(sum(x) for x in zip(random.choice(path), random.choice(deviation)))
        newMaze[y][x] = -1 if newMaze[y][x] == 0 else 0
        solved, _, _ = algorithm(newMaze, (0, 0), (dimm, dimm))
        if solved: #As long as the maze is solvable, we're good to return
            return newMaze


def DFS(grid, start, goal):
    """
    Runs a DFS search from start to goal on the given grid
    @params grid: selected grid, start: starting coordinates, goal: goal coordinates
    @return True/False if a path exists or not, order of nodes used to traverse path if one exists
    """
    frontier = [(start, None)] #acts as stack
    closedList = dict() #list of nodes already explored
    current = start #our curent node
    largestFringe = 0
    while (len(frontier) > 0):
        largestFringe = max(largestFringe, len(frontier))
        #print(frontier)
        current, previous = frontier.pop(0)
        y, x = current
        closedList.update({current: previous})
        if (current == goal):
            return (True, makePath(start, goal, closedList), largestFringe)
        #scan surrounding elements and add them to the closed list
        for newCoord in ((y, x-1), (y-1, x), (y, x+1), (y+1, x)): #it's ordered in this way to make it nice and short in a lot of cases, but priority doesn't really matter for DFS
            newY, newX = newCoord
            if ((newY, newX) not in closedList and (newY, newX) not in [c for (c,_) in frontier] and scan(grid, (newY, newX))):
                frontier.insert(0,((newY, newX), current))
    return False, None, largestFringe

def BFS(grid, start, goal):
    """
    Runs a BFS search from start to goal on the given grid
    This is the exact same code as DFS, except we use a queue system instead of a stack
    @params grid: selected grid, start: starting coordinates, goal: goal coordinates
    @return True/False if a path exists or not, order of nodes used to traverse path if one exists
    """
    frontier = [(start, None)] #acts as queue
    closedList = dict() #list of nodes already explored
    current = start #our curent node
    while (len(frontier) > 0):
        #print(frontier)
        current, previous = frontier.pop(0)
        y, x = current
        closedList.update({current: previous})
        if (current == goal):
            return (True, makePath(start, goal, closedList))
        #scan surrounding elements and add them to the closed list
        for newCoord in ((y, x-1), (y-1, x), (y, x+1), (y+1, x)): #it's ordered in this way to make it nice and short in a lot of cases, but priority doesn't really matter for DFS
            newY, newX = newCoord
            if ((newY, newX) not in closedList and (newY, newX) not in [c for (c,_) in frontier] and scan(grid, (newY, newX))):
                frontier.append(((newY, newX), current))
    return False, None

def BDBFS(grid, start, goal):
    """
    Runs a Bi-direction BFS search from start to goal on the given grid
    @params grid: selected grid, start: starting coordinates, goal: goal coordinates
    @return True/False if a path exists or not, order of nodes used to traverse path if one exists
    """
    startFrontier = [(start, None)]
    goalFrontier = [(goal, None)]
    startClosedList = dict()
    goalClosedList = dict()
    currentStart = start
    currentGoal = goal

    while(len(startFrontier) > 0 and len(goalFrontier) > 0):
        current, previous = startFrontier.pop(0)
        y, x = current
        startClosedList.update({current: previous})
        if (current in goalClosedList):
            goalPath = makePath(goal, current, goalClosedList)
            return (True, list(map(tuple, np.concatenate((makePath(start, current, startClosedList), goalPath[len(goalPath)-2::-1])))))
        #scan surrounding elements and add them to the closed list
        for newCoord in ((y, x-1), (y-1, x), (y, x+1), (y+1, x)): #it's ordered in this way to make it nice and short in a lot of cases, but priority doesn't really matter for DFS
            newY, newX = newCoord
            if ((newY, newX) not in startClosedList and (newY, newX) not in [c for (c,_) in startFrontier] and scan(grid, (newY, newX))):
                startFrontier.append(((newY, newX), current))

        current, previous = goalFrontier.pop(0)
        y, x = current
        goalClosedList.update({current: previous})
        if (current in startClosedList):
            goalPath = makePath(goal, current, goalClosedList)
            return (True, list(map(tuple, np.concatenate((makePath(start, current, startClosedList), goalPath[len(goalPath)-2::-1])))))
        #scan surrounding elements and add them to the closed list
        for newCoord in ((y, x-1), (y-1, x), (y, x+1), (y+1, x)): #it's ordered in this way to make it nice and short in a lot of cases, but priority doesn't really matter for DFS
            newY, newX = newCoord
            if ((newY, newX) not in goalClosedList and (newY, newX) not in [c for (c,_) in goalFrontier] and scan(grid, (newY, newX))):
                goalFrontier.append(((newY, newX), current))
    return False, None

def scan(grid, coords):
    """
    Performs safety checks on nodes before they're added to the frontier
    @params grid: selected grid, coords: coordinates of point to be scanned
    @return True if safe, False if unsafe
    """
    maxHeight = len(grid) -1
    y, x = coords
    if (y < 0 or x < 0):
        return False
    if (y > maxHeight or x > maxHeight):
        return False
    if (int(grid[y][x]) == gd.BLOCKED): #if node is blocked
        return False
    return True

def makePath(start, goal, closedList):
    """
    Using the closed list and start and goal endpoints, traces a path from the goal to the start and then reverses it
    @param start: grid's start coords, goal: goal coords, closedList: search algorithm's closed list
    @return path: array of coords from start to goal
    """
    path = [goal]
    while (goal != start):
        goal = closedList.get(goal)
        path.append(goal)
    path.reverse()
    return path

def main():
    print("Testing algorithms.py")

    hardestMaze = hardestDFSMaze(50)
    _, path, fringeSize = DFS(hardestMaze, (0, 0), (49, 49))
    for y, x in path:
        hardestMaze[y][x] = 3
    pyplot.matshow(hardestMaze)
    pyplot.title(fringeSize)
    pyplot.show()
    for y, x in path:
        hardestMaze[y][x] = 0


    dimm = 10
    start = (0,0)
    goal = (dimm-1,dimm-1)
    grid = gd.generateGrid(dimm, .2)
    print(grid)

    solved, solvedPath, _ = DFS(grid, start, goal)
    if (solved):
        print("DFS: \t", solvedPath)

    solved, solvedPath2 = BFS(grid, start, goal)
    if (solved):
        print("BFS: \t", solvedPath2)

    solved, solvedPath3 = BDBFS(grid, start, goal)
    if (solved):
        print("BDBFS: \t", solvedPath3)
    else: print("Unsolvable!")

    if (solved): #assertions
        assert ( len(solvedPath2) == len(solvedPath3) ), (
            "BFS and BDBFS are not consistent!")
        assert ( len(solvedPath) >= len(solvedPath2) ), (
            "DFS found shorter route than BFS!")

if (__name__ == "__main__"): main()
