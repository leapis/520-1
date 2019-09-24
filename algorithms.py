import grid as gd
import heapq as heap
import math

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
    while (len(frontier) > 0):
        f, (current, previous) = frontier.pop(0)
        y, x = current
        closedList.update({current: previous})
        if (current == goal):
            return (True, makePath(start, goal, closedList))
        #scan surrounding elements and add them to closed list
        currentG = gVals.get(current) + 1
        for newCoord in ((y, x-1), (y-1, x), (y, x+1), (y+1, x)):
            newY, newX = newCoord
            if(scan(grid, (newY, newX))):
                if (newCoord in [k for _, (k, _) in frontier]): #if discovered node is already in open list
                    if(gVals.get(newCoord) > currentG):
                        oldIndex = [z for _, (z, _) in frontier].index(newCoord)
                        frontier[oldIndex] = (currentG + heuristic(newCoord, goal), (newCoord, current))
                        heap.heapify(frontier)
                        gVals.update({newCoord: currentG})
                elif (newCoord in closedList):
                    if(gVals.get(newCoord) > currentG):
                        closedList.pop(newCoord)
                        heap.heappush(frontier,(currentG + heuristic(newCoord, goal),(newCoord, current)))
                        gVals.update({newCoord: currentG})
                else:
                    heap.heappush(frontier,(currentG + heuristic(newCoord, goal),(newCoord, current)))
                    gVals.update({newCoord: currentG})
    return False, None
            



def Euc (start, end):
    y1, x1 = start
    y2, x2 = end
    return math.sqrt(math.pow(y1+y2,2) + math.pow(x1+x2,2))

def Zer (start, end):
    return 0


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
    solvedN = 0
    for q in range(0, 100):
        dimm = 50
        start = (0,0)
        goal = (dimm-1,dimm-1)
        grid = gd.generateGrid(dimm, .2)
        solved, solvedPath = DFS(grid, start, goal)
        solved, solvedPath2 = BFS(grid, start, goal)
        solved, solvedPath3 = aStar(grid, start, goal, Euc)
        #print(grid)
        if (solved): 
            solvedN += 1
            assert(len(solvedPath2) == len(solvedPath3))
            #print("DFS: ", solvedPath)
            #print("BFS: ", solvedPath2)
            #print("ASR: ",solvedPath3)
        else: None#print("Unsolvable!")
    print(solvedN)

        

if (__name__ == "__main__"): main()