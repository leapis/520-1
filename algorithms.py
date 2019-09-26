import numpy as np
import grid as gd
import heapq as heap
import heuristics as h
import math
import random

def DFS(grid, start, goal):
    """
    Runs a DFS search from start to goal on the given grid
    @params grid: selected grid, start: starting coordinates, goal: goal coordinates
    @return True/False if a path exists or not, order of nodes used to traverse path if one exists
    """
    frontier = [(start, None)] #acts as stack
    closedList = dict() #list of nodes already explored
    current = start #our curent node
    while (len(frontier) > 0):
        current, previous = frontier.pop(0)
        y, x = current
        closedList.update({current: previous})
        if (current == goal):
            return (True, makePath(start, goal, closedList))
        #scan surrounding elements and add them to the closed list
        for newCoord in ((y, x-1), (y-1, x), (y, x+1), (y+1, x)): #it's ordered in this way to make it nice and short in a lot of cases, but priority doesn't really matter for DFS
            newY, newX = newCoord
            if ((newY, newX) not in closedList and (newY, newX) not in [c for (c,_) in frontier] and scan(grid, (newY, newX))):
                frontier.insert(0,((newY, newX), current))
    return False, None

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

def aStar(grid, start, goal, heuristic, tieSort=False, fire=False, fireLimit=0, q=0, previousGrids={}):
    """
    Runs an A* search from start to goal on the given grid
    @params grid: selecte grid, start: starting coordinates, goal: goal coordinates
    @return True/False if a path exists or not, order of nodes used to traverse path if one exists,
    tuple containing output debug data (length closedList, list of explored nodes, frontier)
    """
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
            return (True, makePath(start, goal, closedList), (len(closedList), exploredNodes, frontier, previousGrids))
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
    if (grid[i][j] == gd.FIRE):
        return gd.FIRE
    if (grid[i][j] == gd.BLOCKED):
        return gd.BLOCKED
    value = grid[i][j]
    for i,j in [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]:
        if(scan(grid, (i,j))):
            value = value + (1 - value) * (1 - (1 - q)) * grid[i][j]
    return value

def fireEval(grid, path, q):

    evalGrid = gd.grid_copy(grid)
    for i in range(len(path)):
        current = path[i]
        y, x = current
        if (evalGrid[y][x] == gd.FIRE):
            #rerun A* looking for an alternative route
            dimm = len(evalGrid)
            solved, newPath, _ = aStar(evalGrid, path[i-1], (dimm - 1, dimm - 1), h.Manhattan, False, True, 0.7, q)
            if (solved):
                return fireEval(grid, newPath, q)
            else:
                return False, evalGrid 
        evalGrid = fireAdvance(evalGrid, q)
    return True, evalGrid

def fireAdvance(grid, q):
    nextGrid = gd.grid_copy(grid)
    for i in range(len(nextGrid)):
        for j in range(len(nextGrid)):
            if(nextGrid[i][j] != gd.FIRE and nextGrid[i][j] != gd.BLOCKED):
                surrounding = 0
                for y,x in [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]:
                    if ( scan(grid, (y,x)) and  grid[y][x] == gd.FIRE):
                        surrounding += 1
                if (random.random() < (1 - math.pow(1 - q, surrounding))):
                    nextGrid[i][j] = gd.FIRE
    return nextGrid
                
        
    
def testOne():
    print("Testing algorithms.py")
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

    print(fireEval(grid, solvedPath, 0.3))

def testFive():
    for q in np.arange(0, 1.04, 0.05):
        runs = 100
        success = 0
        tries = 0
        while (tries < runs):
            #thresh = 0.5
            start = (0,0)
            dimm = 30
            bottomLeft = (dimm - 1, 0)
            upperRight = (0, dimm - 1)
            p = 0.2
            goal = (dimm-1, dimm-1)
            heuristic = h.Manhattan
            grid = gd.generateFireGrid(dimm, p)
            #print(grid)
            previousFireGrids = dict()
            #solvedStrong, solvedPath, testingData = aStar(grid, start, goal, heuristic, False, True, thresh, q)
            solved, _ = BDBFS(grid, start, goal)
            fireHasPath, _ = BDBFS(grid, bottomLeft, upperRight)
            if (solved and fireHasPath):
                listings = [i for i in np.arange(0,1.05,0.05)]
                for i in listings:
                    _, solvedPath, testData = aStar(grid, start, goal, h.Manhattan, False, True, i, q, previousFireGrids)
                    if (solvedPath):
                        _, _, _, previousFireGrids = testData
                        #print(listings)
                        tries += 1
                        fireSolved, _ = fireEval(grid, solvedPath, q)
                        if (fireSolved): 
                            success += 1
                        break
                            #print(grid)
                            #print(solvedPath)
                
        print("for", q, ":", success/tries, " : ", success, "/", tries)

def testSix():
    runs = 10
    for heuristic in [h.Euc]:#[h.returnZero, h.Manhattan, h.Euc]:
        for p in np.arange(0, 0.41, 0.05):
            count = 0
            numSolved = 0
            while (numSolved < runs):
                dimm = 100
                start = (0,0)
                goal = (dimm-1,dimm-1)
                grid = gd.generateFireGrid(dimm, p)
                solved, _ = BDBFS(grid, start, goal)
                if(solved):
                    solved, solvedPath, testingData = aStar(grid, start, goal, heuristic, True)
                    numSolved += 1
                    closedLen, *_ = testingData
                    count += closedLen
            print(p, " : ", count/runs)
            


if (__name__ == "__main__"): testSix()
