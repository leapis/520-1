import numpy as np
import grid as gd
import heapq as heap
import heuristics as h

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

def aStar(grid, start, goal, heuristic):
    """
    Runs an A* search from start to goal on the given grid
    @params grid: selecte grid, start: starting coordinates, goal: goal coordinates
    @return True/False if a path exists or not, order of nodes used to traverse path if one exists
    """
    frontier = []
    heap.heappush(frontier,(0,(start, None)))
    closedList = dict()
    gVals = dict()
    gVals.update({start: 0})
    current = start
    exploredNodes = []
    while (len(frontier) > 0):
        f, (current, previous) = heap.heappop(frontier)
        exploredNodes.append(current)
        y, x = current
        closedList.update({current: previous})
        if (current == goal):
            return (True, makePath(start, goal, closedList), (len(closedList), exploredNodes, frontier))
        #scan surrounding elements and add them to closed list
        currentG = gVals.get(current) + 1
        for newCoord in ( (y, x-1), (y-1, x), (y, x+1), (y+1, x) ):
            newY, newX = newCoord
            if(scan(grid, (newY, newX))):
                if (newCoord in [k for _, (k, _) in frontier]): #if discovered node is already in open list
                    if(gVals.get(newCoord) > currentG): print (currentG, "OVERWRITE OL!")
                    if(gVals.get(newCoord) > currentG):
                        oldIndex = [z for _, (z, _) in frontier].index(newCoord)
                        frontier[oldIndex] = (currentG + heuristic(newCoord, goal), (newCoord, current))
                        heap.heapify(frontier)
                        gVals.update({newCoord: currentG})
                elif (newCoord in closedList):
                    if(gVals.get(newCoord) > currentG):
                        print("OVERWROTE CLOSEDLIST")
                        closedList.pop(newCoord)
                        heap.heappush(frontier,(currentG + heuristic(newCoord, goal),(newCoord, current)))
                        gVals.update({newCoord: currentG})
                else:
                    heap.heappush(frontier,(currentG + heuristic(newCoord, goal),(newCoord, current)))
                    gVals.update({newCoord: currentG})
    return False, None, ()
            
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
    heuristic = h.Manhattan
    runs = 100
    printOn = True
    if (runs > 5): printOn = False #5 is a magic number
    BFSCount = 0
    aStarCount = 0
    
    for _ in range(runs):
        p = 0.3
        dimm = 30
        start = (0,0)
        goal = (dimm-1,dimm-1)
        grid = gd.generateGrid(dimm, p)
        if (printOn): print(grid)

        solved, solvedPathDFS = DFS(grid, start, goal)
        solved, solvedPathBFS, TestingDataBFS = BFS(grid, start, goal)
        solved, solvedPathBDBFS = BDBFS(grid, start, goal)
        solved, solvedPathaStar, testingDataaStar = aStar(grid, start, goal, heuristic)

        exploredBFS = frontierBFS = exploredaStar = 0
        printOn = False
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

if (__name__ == "__main__"): main()
