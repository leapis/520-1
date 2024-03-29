import numpy
from matplotlib import pyplot
import minesweeper
import random
import time
import sys
import inference

# This is a very useful array to iterate over for neighbors
surroundings = [
    (-1, -1), (-1,  0), (-1,  1),
    ( 0, -1),           ( 0,  1),
    ( 1, -1), ( 1,  0), ( 1,  1)
]

def inspect_cell(grid, mines, clues, i, j):
    d = len(grid)
    info = False # Represents whether the puzzle has moved forward due to this inspection
    # We only have clues for revealed cells
    if mines[i][j] != 1:
        return

    mineNeighbors = 0
    safeNeighbors = 0
    unknownNeighbors = 8
    wallNeighbors = 0
    # Count the number of unknown, safe, and mine neighbors on the fly
    for offset in surroundings:
        oi, oj = offset
        if 0 <= i + oi < d and 0 <= j + oj < d:
            if mines[i + oi][j + oj] == -1:
                mineNeighbors += 1
                unknownNeighbors -= 1
            if mines[i + oi][j + oj] == 1:
                safeNeighbors += 1
                unknownNeighbors -= 1
        else:
            wallNeighbors += 1
    unknownNeighbors -= wallNeighbors

    # No point in inspecting this cell!
    if unknownNeighbors == 0:
        return False

    # Rule 1 of the basic agent, where it knows remaining neighbors are mines
    if clues[i][j] - mineNeighbors == unknownNeighbors:
        info = True
        for offset in surroundings:
            oi, oj = offset
            if 0 <= i + oi < d and 0 <= j + oj < d and mines[i + oi][j + oj] == 0:
                mines[i + oi][j + oj] = -1
    # Rule 2 of the basic agent, where it knows remaining neighbors are safe and should be revealed
    if 8 - wallNeighbors - clues[i][j] - safeNeighbors == unknownNeighbors:
        info = True
        for offset in surroundings:
            oi, oj = offset
            if 0 <= i + oi < len(mines) and 0 <= j + oj < len(mines) and mines[i + oi][j + oj] == 0:
                mines[i + oi][j + oj] = 1
                clues[i + oi][j + oj] = grid[i + oi][j + oj] # This access represents a reveal
                if grid[i + oi][j + oj] == -1:
                    print('You should not have revealed this mine!')

    return info
    
def isNewFact(knowledge_base, fact):
    for kFact in knowledge_base:
        if fact.is_equal_to(kFact):
            return False
    return True

def dumpSquare(mines, m, n):
    return ("""
    {v1} {v2} {v3}
    {v4} {v5} {v6}
    {v7} {v8} {v9}
    """.format(
        v1=mines[m-1][n-1],v2=mines[m-1,n],v3=mines[m-1,n+1],
        v4=mines[m][n-1],v5=mines[m,n],v6=mines[m,n+1],
        v7=mines[m+1][n-1],v8=mines[m+1,n],v9=mines[m+1,n+1],
        ))

def infer(grid, clues, mines):

    knowledge_base = []

    for m in range(len(grid)): #create knowledge base
        for n in range(len(grid[0])):
            if mines[m][n] == 1 and minesweeper.unsolved_in_neighborhood(mines, m, n) > 0: #if confirmed safe and there are unsolved
                assert (minesweeper.unsolved_in_neighborhood(mines, m, n) != 1), "UNSOLVED_IN_NEIGHBORHOOD ERROR" #if there is only one, we should have already caught it
                assert (minesweeper.unsolved_in_neighborhood(mines, m, n) >= 0), "UNSOLVED_IN_NEIGHBORHOOD SEVERE ERROR"
                unknowns = []
                minesFound = 0
                for offset in surroundings:
                    i, j = m + offset[0], n + offset[1]
                    if not minesweeper.is_valid(i, j, len(grid)): continue
                    if mines[i][j] == 0: #coveread
                        unknowns.append( (i,j) )
                    elif mines[i][j] == -1: #mine
                        minesFound += 1

                diffValue = int(clues[m][n]) - minesFound #mines we haven't found yet
                assert (int(clues[m][n]) > 0), "VALUES_AT_OR_UNDER_ZERO: " + str(int(clues[m][n])) + " - " + str(minesFound) + " = " + str(diffValue) + " :: " + dumpSquare(mines, m, n)
                knowledge_base.append(inference.Fact(diffValue, unknowns))

    updated = True
    while (updated): #iterate through facts to see if we can use modus ponens
        updated = False
        for fact in knowledge_base:
            assert (len(fact.unknowns) > 1), ("ATOMIC GOT THROUGH: " + str(fact.value) + " : " + str(fact.unknowns) + 
                "minestatus: " + str(mines[list(fact.unknowns)[0][0]][list(fact.unknowns)[0][1]]) + 
                "actual: " + str(grid[list(fact.unknowns)[0][0]][list(fact.unknowns)[0][0]]) +
                " :: " + dumpSquare(grid, list(fact.unknowns)[0][0], list(fact.unknowns)[0][1]))
            if ( len(fact.unknowns) == 2): continue #set of 2 cannot contain subset
            for otherFact in knowledge_base:
                foundFact, newFact = fact.merge_subset(otherFact)
                if foundFact and isNewFact(knowledge_base, newFact):
                    if newFact.is_solved_zero():
                        print(str(newFact.value), ":", str(newFact.unknowns))
                        for cell in newFact.unknowns:
                            a, b = cell
                            assert(mines[a][b] == 0), "DISCOVERED EXISTING FACT"
                            mines[a][b] = 1
                            assert(grid[a][b] != -1), "INCORRECT ASSIGNMENT (ZEROS)"
                            clues[a][b] = minesweeper.mines_in_neighborhood(grid, a, b)
                            print("SOLVED FOR" + str(a) + "," + str(b))
                        return True, clues, mines
                    if newFact.is_solved_atomic():
                        a, b = newFact.unknowns.pop()
                        assert (newFact.value == 1), str(newFact.value) + " GOT THROUGH newFact"
                        assert(mines[a][b] == 0), "ATOMIC DISCOVERED EXISTING FACT"
                        mines[a][b] = -1
                        assert (mines[a][b] == grid[a][b]), "INCORRECT ASSIGNMENT (ATOMIC)"
                        print("SOLVED FOR" + str(a) + "," + str(b))
                        return True, clues, mines
                    updated = True
                    knowledge_base.append(newFact)
    
    return False, clues, mines #we could not infer anything about the situation

def sweep_grid(grid):
    d = len(grid)
    explosions = 0
    clues = numpy.zeros((d, d))
    mines = numpy.zeros((d, d)) # 0 for covered, -1 for mine, 1 for safe

    while True:
        info = False # Whether any cell moved forward in the puzzle
        for i in range(0, d):
            for j in range(0, d):
                info = inspect_cell(grid, mines, clues, i, j) or info

        # This second for loop helps performance significantly, since it would otherwise be
        # very inefficient to try to follow clues toward the top-left
        for i in range(d-1, -1, -1):
            for j in range(d-1, -1, -1):
                info = inspect_cell(grid, mines, clues, i, j) or info

        if not info:
            print("Trying inference")
            discovered = False
            #now let's try to solve it with our logical inference engine:
            discovered, clues, mines = infer(grid, clues, mines)
            if (discovered): 
                print("Inference worked!")
                #assert(False), "WORKED!"

        # Rule 5 of the basic agent, there are no known ways forward, so take random guess
        if not info and not discovered:
            # But first we check if theres no ways forward because the puzzle is complete!
            done = True
            for i in range(0, d):
                for j in range(0, d):
                    if mines[i][j] == 0:
                        done = False
            if done:
                print("Explosions: ", explosions)
                return

            print("randoming")
            #pyplot.matshow(grid)
            #pyplot.matshow(mines)
            #pyplot.show()
            # Random unknown cell
            i = random.randint(0, d - 1)
            j = random.randint(0, d - 1)
            while mines[i][j] != 0:
                i = random.randint(0, d - 1)
                j = random.randint(0, d - 1)

            if grid[i][j] == -1:
                mines[i][j] = -1
                print('Boom!', flush = True)
                explosions += 1
            else:
                mines[i][j] = 1
                clues[i][j] = grid[i][j]
                print(grid[i][j])
        #pyplot.matshow(grid)
        #pyplot.matshow(mines)
        #pyplot.show()

if __name__ == '__main__':
    while(True):
        grid = minesweeper.generate_environment(40, 150)
        sweep_grid(grid)
