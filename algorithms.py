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
    tieSort = tieSort #tieSort=True means that in the case of multiple nodes on the frontier with the same f value, we will sort and pick the most optimal
    frontier = [] #open list
    heap.heappush(frontier,(0,(start, None)))
    closedList = dict()
    gVals = dict() #list of g values (distance from start) for each node
    gVals.update({start: 0})
    current = start
    exploredNodes = [] #list of node's we've added to closed list. This is different than the closed list because it keeps order, only for debugging purposes
    while (len(frontier) > 0): #while open list has elements
        candidates = [heap.heappop(frontier)] #candidates is part of our tieSort
        value, _ = candidates[0]
        top = candidates[0]

        if( tieSort and len(frontier) > 0): #if tieSort=True, and open list isn't empty
            nextOnFrontierValue, _ = frontier[0]
            i = 0
            while (len(frontier) > 0 and value == nextOnFrontierValue and i < goal[0]): #load all elements on frontier with f equal to the first into candidates
                candidates.append(heap.heappop(frontier))
                i+= 1
            top = max(candidates, key= lambda x: gVals.get(x[1][0])) 
            #^ this is our sorting algorithm: we weight g more heavily than h, so pick the max g. This will help us pick a path and stick too it for Manhattan distance, resulting in less expands, so long as f(x) doesn't change
            candidates.remove(top)
            while(len(candidates) > 0): #put the rest of the candidates back into the open list
                heap.heappush(frontier, candidates[-1])
                del candidates[-1]

        _, (current, previous) = top 
        exploredNodes.append(current)
        y, x = current
        closedList.update({current: previous}) #add our selected node to the closed list
        if (current == goal): #we've found the goal! return
            return (True, makePath(start, goal, closedList), (len(closedList), exploredNodes, frontier, previousGrids))
        #scan surrounding elements and add them to closed list
        currentG = gVals.get(current) + 1 # this will be the g value for surrounding nodes

        for newCoord in ( (y, x-1), (y-1, x), (y, x+1), (y+1, x) ): #scan up down left right
            newY, newX = newCoord 
            allowedMove = scan(grid, (newY, newX))
            if (fire): #if we're operating with fire, we have to scan and use our special fire rules (defined in part 4 of answer document)
                allowedMove = scan(grid, (newY, newX), True, previousGrids, fireLimit, currentG, q)
            if(allowedMove): #if the move is safe
                if (newCoord in [k for _, (k, _) in frontier]): #if discovered node is already in open list
                    if(gVals.get(newCoord) > currentG): #in case of admissible but not consistent heuristic, if node's g is greater than other's g
                        oldIndex = [z for _, (z, _) in frontier].index(newCoord) 
                        frontier[oldIndex] = (currentG + heuristic(newCoord, goal), (newCoord, current))
                        heap.heapify(frontier)
                        gVals.update({newCoord: currentG})
                elif (newCoord in closedList): #in case of admissible but not consistent heuristic, if node is already in closed list
                    if(gVals.get(newCoord) > currentG): #if node's g is greater than other's g
                        closedList.pop(newCoord)
                        heap.heappush(frontier,(currentG + heuristic(newCoord, goal),(newCoord, current)))
                        gVals.update({newCoord: currentG})
                else: #if undiscovered thus far
                    heap.heappush(frontier,(currentG + heuristic(newCoord, goal),(newCoord, current)))
                    gVals.update({newCoord: currentG})
    return False, None, (closedList) #this will be reached if frontier list runs out of elements
            
def scan(grid, coords, fire=False, previousGrids={}, fireLimit=0, g=-1, q=0):
    """
    Performs safety checks on nodes before they're added to the frontier
    @params grid: selected grid, coords: coordinates of point to be scanned
    @return True if safe, False if unsafe
    """
    maxHeight = len(grid) -1
    y, x = coords
    if (y < 0 or x < 0): #if node is out of bounds
        return False
    if (y > maxHeight or x > maxHeight): #if node is out of bounds
        return False
    if (int(grid[y][x]) == gd.BLOCKED): #if node is blocked
        return False
    if (fire):
        if(generateFireGrids(previousGrids, grid, g, q)[y][x] > fireLimit): #if node's probabilty of being on fire is greater than our threshold
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
    """
    Using the grid and a q value, generates the grid's probability state at point q
    @param previousGrids: set of previously generated grids, grid: starting grid, g: g steps, q
    @return fireGrid, a grid that shows the probability likelihood for each cell to be on fire at step g
    """
    if(g == 0): #base case
        previousGrids[g] = grid
        return grid
    fireGrid = []
    if(g in previousGrids): #if it's already been generated, we don't need to re-generate it
        return previousGrids[g]
    if (g-1 not in previousGrids):
        fireGrid = generateFireGrids(previousGrids, grid, g-1, q)
    fireGrid = gd.grid_copy(previousGrids[g-1])
    for i in range(len(fireGrid)):
        for j in range(len(fireGrid)):
            fireGrid[i][j] = fireScan(previousGrids[g-1], (i, j), q) #get and set the value of the current node from fireScan
    previousGrids[g] = fireGrid
    return fireGrid

def fireScan(grid, coords, q):
    """
    Using the grid, a coordinate, and a q value, generates the probability of this node being on fire
    @param grid: current grid, coords: coordinates of point, q
    @return value, the probability that the given coordinates will be on fire in the next timestep
    """
    i, j = coords
    if (grid[i][j] == gd.FIRE): #if it's on fire (ie 1), it will always be 1
        return gd.FIRE
    if (grid[i][j] == gd.BLOCKED): #blocked nodes can't catch on
        return gd.BLOCKED
    value = grid[i][j]
    for i,j in [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]: #for each surrounding node
        if(scan(grid, (i,j))): #if node is not blocked or out of bounds
            value = value + (1 - value) * (1 - (1 - q)) * grid[i][j] 
            #chance a node is on fire is the chance that it was already on fire + chance that it wasn't * likelihood that the node next to it is * chance it catches on fire if the node next to it is
    return value

def fireEval(grid, path, q):
    """
    This is the function we use to run A* through the fire grid
    @params grid: starting grid, path: the path our initial A* gave us, q
    @return True/False, whether our runner survived or not, the last grid it was in (for testing purposes)
    """
    evalGrid = gd.grid_copy(grid)
    for i in range(len(path)): #for every node in path
        current = path[i]
        y, x = current
        if (evalGrid[y][x] == gd.FIRE): #if node is on fire
            #rerun A* from last safe node looking for an alternative route
            dimm = len(evalGrid)
            solved, newPath, _ = aStar(evalGrid, path[i-1], (dimm - 1, dimm - 1), h.Manhattan, False, True, 0.9, q)
            if (solved):
                return fireEval(grid, newPath, q) #if A* finds a new path, take it
            else:
                return False, evalGrid #no path was found, A* can't help you
        evalGrid = fireAdvance(evalGrid, q) #advance grid to next state
    return True, evalGrid

def fireAdvance(grid, q):
    """
    This is our fire grid "engine". Seperate from the probability measure, this gives us the current state of the grid on fire
    @params grid: given grid, q
    @return grid at next timestep
    """
    nextGrid = gd.grid_copy(grid)
    for i in range(len(nextGrid)):
        for j in range(len(nextGrid)):
            if(nextGrid[i][j] != gd.FIRE and nextGrid[i][j] != gd.BLOCKED): #if cell isn't already on fire or blocked
                surrounding = 0
                for y,x in [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]: #for each surrounding node
                    if ( scan(grid, (y,x)) and  grid[y][x] == gd.FIRE): #if surrounding node is on fire
                        surrounding += 1
                if (random.random() < (1 - math.pow(1 - q, surrounding))): #if chance of catching fire is higher than random.random() (0,1)
                    nextGrid[i][j] = gd.FIRE #put node on fire
    return nextGrid
                
"""
Please note:
Everything below here is testing/data generation data.
It may contain examples of how to run our functions, but it is just driver code- 
nothing below this point is important for the implementation of our algorithms.
As such, it is not commented extensively. Feel free to ignore.
"""
    
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
    for p in np.arange(0, 0.41, 0.05):
        count = {}
        count[h.returnZero.__name__] = 0
        count[h.Manhattan.__name__] = 0
        count[h.Euc.__name__] = 0
        numSolved = 0
        while (numSolved < 3 * runs):
            dimm = 100
            start = (0,0)
            goal = (dimm-1,dimm-1)
            grid = gd.generateFireGrid(dimm, p)
            solved, _ = BDBFS(grid, start, goal)
            for heuristic in [h.returnZero, h.Manhattan, h.Euc]:
                if(solved):
                    solved, solvedPath, testingData = aStar(grid, start, goal, heuristic, True)
                    if (heuristic == h.returnZero):
                        solved, solvedPath, testingData = BFS(grid, start, goal)
                    numSolved += 1
                    closedLen, *_ = testingData
                    count[heuristic.__name__] += closedLen
        print(math.ceil(p * 100) / 100, " : ", math.floor(count[h.returnZero.__name__]/runs), math.floor(count[h.Manhattan.__name__]/runs), math.floor(count[h.Euc.__name__]/runs))
            


if (__name__ == "__main__"): testSix()
