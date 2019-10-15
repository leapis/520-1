import numpy
import random


def is_valid(x, y, d):
    """ Determines whether x,y are valid grid (d x d) coordinates """
    return 0 <= x < d and 0 <= y < d


def mines_in_neighborhood(array, i, j):
    """ Return the total number of mines in the 8 squares surrounding
    spot array[i][j] """
    number_of_mines = 0
    offset = 0
    surroundings = [
        (-1, -1), (-1,  0), (-1,  1),
        ( 0, -1),           ( 0,  1),
        ( 1, -1), ( 1,  0), ( 1,  1)
    ]
    while offset < len(surroundings):
        a, b = i + surroundings[offset][0], j + surroundings[offset][1]
        if is_valid(a, b, len(array)):
            if array[a][b] == -1:
                number_of_mines += 1
        offset += 1
    return number_of_mines

def unsolved_in_neighborhood(matrix, m, n):
    """ Return the total number of unsolved cells in the 8 cells surrounding spot matrix[m][n]
    """
    unsolvedCount = 0
    surroundings = [
        (-1, -1), (-1,  0), (-1,  1),
        ( 0, -1),           ( 0,  1),
        ( 1, -1), ( 1,  0), ( 1,  1)
    ]
    for offset in surroundings:
        a, b = m + offset[0], n + offset[1]
        if is_valid(a, b, len(matrix)):
            if matrix[a][b] == 0:
                unsolvedCount += 1
    return unsolvedCount


def generate_environment(d, n):
    """ Return a d x d grid with n mines assigned at random, where each
    spot dim(i, j) contains either -1 for a mine or the number of mines
    bordering the spot.

    :param d: dimension, the grid size
    :param n: number of mines
    :return: array representing state space
    """
    assert (n <= d*d), "Grid not big enough for number of mines"

    array = numpy.zeros((d, d))
    # place mines randomly
    while n > 0:
        x, y = random.randint(0, d - 1), random.randint(0, d - 1)
        if array[x][y] != -1:
            array[x][y] = -1
            n -= 1

    # create numbers mines next to each spot
    for i in range(d):
        for j in range(d):
            if array[i][j] != -1:
                array[i][j] = mines_in_neighborhood(array, i, j)
    return array


if __name__ == '__main__':
    # 5x5 grid, 5 mines total
    generate_environment(5, 5)
