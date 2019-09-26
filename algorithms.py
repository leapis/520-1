import numpy as np
import grid as gd
import heapq as heap
import heuristics as h
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
    exploredNodes = []
    while (len(frontier) > 0):
        current, previous = frontier.pop(0)
        exploredNodes.append(current)
        y, x = current
        closedList.update({current: previous})
        if (current == goal):
            return (True, makePath(start, goal, closedList), (len(closedList), exploredNodes, frontier))
        #scan surrounding elements and add them to the closed list
        for newCoord in ((y, x-1), (y-1, x), (y, x+1), (y+1, x)): #it's ordered in this way to make it nice and short in a lot of cases, but priority doesn't really matter for DFS
            newY, newX = newCoord
            if ((newY, newX) not in closedList and (newY, newX) not in [c for (c,_) in frontier] and scan(grid, (newY, newX))):
                frontier.append(((newY, newX), current))
    return False, None, ()

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

def aStar(grid, start, goal, heuristic, tieSort=False, fire=False, fireLimit=0, q=0):
    """
    Runs an A* search from start to goal on the given grid
    @params grid: selecte grid, start: starting coordinates, goal: goal coordinates
    @return True/False if a path exists or not, order of nodes used to traverse path if one exists,
    tuple containing output debug data (length closedList, list of explored nodes, frontier)
    """
    previousGrids = {}
    tieSort = tieSort
    frontier = []
    heap.heappush(frontier,(0,(start, None)))
    closedList = dict()
    gVals = dict()
    gVals.update({start: 0})
    current = start
    exploredNodes = []
    while (len(frontier) > 0):
        candidates = [heap.heappop(frontier)]
        value, _ = candidates[0]
        top = candidates[0]

        if( tieSort and len(frontier) > 0):
            nextOnFrontierValue, _ = frontier[0]
            i = 0
            while (len(frontier) > 0 and value == nextOnFrontierValue and i < goal[0]):
                candidates.append(heap.heappop(frontier))
                i+= 1
            top = max(candidates, key= lambda x: gVals.get(x[1][0]))
            candidates.remove(top)
            while(len(candidates) > 0):
                heap.heappush(frontier, candidates[-1])
                del candidates[-1]

        _, (current, previous) = top
        exploredNodes.append(current)
        y, x = current
        closedList.update({current: previous})
        if (current == goal):
            return (True, makePath(start, goal, closedList), (len(closedList), exploredNodes, frontier))
        #scan surrounding elements and add them to closed list
        currentG = gVals.get(current) + 1
        for newCoord in ( (y, x-1), (y-1, x), (y, x+1), (y+1, x) ):
            newY, newX = newCoord
            allowedMove = scan(grid, (newY, newX))
            if (fire):
                allowedMove = scan(grid, (newY, newX), True, previousGrids, fireLimit, currentG, q)
                #print(allowedMove, previousGrids.get(currentG)[y][x], fireLimit)
            if(allowedMove):
                if (newCoord in [k for _, (k, _) in frontier]): #if discovered node is already in open list
                    if(gVals.get(newCoord) > currentG): #in case of admissible but not consistent heuristic
                        oldIndex = [z for _, (z, _) in frontier].index(newCoord)
                        frontier[oldIndex] = (currentG + heuristic(newCoord, goal), (newCoord, current))
                        heap.heapify(frontier)
                        gVals.update({newCoord: currentG})
                elif (newCoord in closedList): #in case of admissible but not consistent heuristic
                    if(gVals.get(newCoord) > currentG):
                        closedList.pop(newCoord)
                        heap.heappush(frontier,(currentG + heuristic(newCoord, goal),(newCoord, current)))
                        gVals.update({newCoord: currentG})
                else:
                    heap.heappush(frontier,(currentG + heuristic(newCoord, goal),(newCoord, current)))
                    gVals.update({newCoord: currentG})
    return False, None, (closedList)

def scan(grid, coords, fire=False, previousGrids={}, fireLimit=0, g=-1, q=0):
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
    if (fire):
        if(generateFireGrids(previousGrids, grid, g, q)[y][x] > fireLimit):
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

def generateFireGrids(previousGrids, grid, g, q):
    if(g == 0):
        previousGrids[g] = grid
        return grid
    fireGrid = []
    if(g in previousGrids):
        return previousGrids[g]
    if (g-1 not in previousGrids):
        fireGrid = generateFireGrids(previousGrids, grid, g-1, q)
    fireGrid = gd.grid_copy(previousGrids[g-1])
    for i in range(len(fireGrid)):
        for j in range(len(fireGrid)):
            fireGrid[i][j] = fireScan(previousGrids[g-1], (i, j), q)
    previousGrids[g] = fireGrid
    return fireGrid

def fireScan(grid, coords, q):
    i, j = coords
    value = grid[i][j]
    for i,j in [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]:
        if(scan(grid, (i,j))):
            value = value + (1 - value) * (1 - (1 - q)) * grid[i][j]
    return value

def testOne():
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
    heuristic = h.Manhattan
    runs = 1
    printOn = True
    if (runs > 5): printOn = False #5 is a magic number
    BFSCount = 0
    aStarCount = 0

    for _ in range(runs):
        p = 0.3
        dimm = 10
        start = (0,0)
        goal = (dimm-1,dimm-1)
        grid = gd.generateGrid(dimm, p)
        if (printOn): print(grid)

        solved, solvedPathDFS = DFS(grid, start, goal)
        solved, solvedPathBFS, TestingDataBFS = BFS(grid, start, goal)
        solved, solvedPathBDBFS = BDBFS(grid, start, goal)
        solved, solvedPathaStar, testingDataaStar = aStar(grid, start, goal, heuristic)

        exploredBFS = frontierBFS = exploredaStar = 0
        if (solved):
            if(printOn):
                print("DFS: \t" + str(solvedPathDFS))
                print("BFS: \t" + str(solvedPathBFS))
                print("BDBFS: \t", solvedPathBDBFS)
                print("aStar: \t", solvedPathaStar)

            lenaStar,exploredBFS, frontierBFS = TestingDataBFS
            lenBFS,exploredaStar, frontieraStar = testingDataaStar
            exploredBFS = set(exploredBFS)
            frontierBFS = [v for v,_ in frontierBFS]
            frontierBFS = set(frontierBFS)
            exploredaStar = set(exploredaStar)
            frontieraStar = [v for _,(v,_) in frontieraStar]
            frontieraStar = set(frontieraStar)
        else:
            if (printOn): print("Unsolvable!")

        if (solved):
            BFSCount += len(exploredBFS)#len(exploredBFS.union(frontierBFS))
            aStarCount += len(exploredaStar)#len(exploredaStar.union(frontieraStar))

        if (solved): #assertions
            assert ( len(solvedPathBFS) == len(solvedPathBDBFS) ), (
                "BFS and BDBFS are not consistent!")
            assert ( len(solvedPathDFS) >= len(solvedPathBFS) ), (
                "DFS found shorter route than BFS!")
            assert ( len(solvedPathaStar) == len(solvedPathBFS) ) , (
                "aStar or BFS not optimal!"
            )
            #determines, when using no heuristic, whether aStar is equal to BFS
            assert (
                not (heuristic == h.returnZero) or
                exploredaStar.difference( exploredBFS.union(frontierBFS) ) == set()
                #we have to include the frontier of BFS due to queue differences
                ), (
                "aStar with heuristic of h(x) = 0 not identical to BFS! \n"+
                "aStar: " + str(lenaStar) + ", BFS: " + str(lenBFS) + "\n" +
                str(exploredaStar) + "\n" + str(exploredBFS) + "\n" +
                str(frontierBFS) + "\n" + str(grid)
            )
    print(BFSCount)
    print(aStarCount)

def testTwo():
    heuristic = h.Manhattan
    p = 0.3
    dimm = 50
    start = (0,0)
    goal = (dimm-1,dimm-1)
    grid = gd.generateFireGrid(dimm, p)
    solved1, solvedPathaStar1, testingDataaStar1 = aStar(grid, start, goal, heuristic, tieSort=False)
    solved2, solvedPathaStar2, testingDataaStar2 = aStar(grid, start, goal, heuristic, tieSort=True)
    assert (solved1 == solved2)
    if(solved1):
        (_,t1,_) = testingDataaStar1
        (_,t2,_) = testingDataaStar2
        print(len(t1), " : " ,len(t2))
    else:
        print(len(testingDataaStar1), ":", len(testingDataaStar2))
        print("unsolved")
    print(str(grid))

def testThree():
    p = 0.3
    dimm = 10
    grid = gd.generateFireGrid(dimm, 0)
    previousFireGrids = dict()
    print(generateFireGrids(previousFireGrids, grid, 1, 0.3))

def testFour():
    start = (0,0)
    p = 0.3
    dimm = 5
    goal = (dimm-1, dimm-1)
    heuristic = h.Manhattan
    grid = gd.generateFireGrid(dimm, 0)
    previousFireGrids = dict()
    solved, solvedPath, testingData = aStar(grid, start, goal, heuristic, True, True, 0.5, 0.3)
    print(generateFireGrids(previousFireGrids, grid, len(solvedPath) - 1, 0.3))
    print(solvedPath)

if (__name__ == "__main__"): testFour()
