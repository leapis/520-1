import math

def returnZero(start, end):
    """
    h(x) = 0
    """
    return 0

def Euc(start, end):
    """
    h(x) = Euclidean distance
    """
    y1, x1 = start
    y2, x2 = end
    return math.sqrt( math.pow(y1 - y2, 2) + math.pow(x1 - x2, 2) )

def Manhattan(start, end):
    """
    h(x) = Manhattan distance
    """
    y1, x1 = start
    y2, x2 = end
    return abs(y1 - y2) + abs(x1 - x2)