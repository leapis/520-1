import numpy as np
import grid as gd

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
        last = current
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
        last = current
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
    dimm = 5
    start = (0,0)
    goal = (dimm-1,dimm-1)
    grid = gd.generateGrid(dimm, .3)
    print(grid)

    solved, solvedPath = DFS(grid, start, goal)
    if (solved):
        print("DFS: ", solvedPath)

    solved, solvedPath2 = BFS(grid, start, goal)
    if (solved):
        print("BFS: ", solvedPath2)

    solved, solvedPath3 = BDBFS(grid, start, goal)
    if (solved):
        print("BDBFS: ", solvedPath3)
    else: print("Unsolvable!")

if (__name__ == "__main__"): main()
