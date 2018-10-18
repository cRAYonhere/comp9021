# Randomly fills a grid of size 10 x 10 with digits between 0
# and bound - 1, with bound provided by the user.
# Given a point P of coordinates (x, y) and an integer "target"
# also all provided by the user, finds a path starting from P,
# moving either horizontally or vertically, in either direction,
# so that the numbers in the visited cells add up to "target".
# The grid is explored in a depth-first manner, first trying to move north,
# always trying to keep the current direction,
# and if that does not work turning in a clockwise manner.
#
# Written by Eric Martin for COMP9021


import sys
from random import seed, randrange

from stack_adt import *

def display_grid(grid):
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))

def explore_depth_first(x, y, target,grid):

    stack = Stack()
    cost = grid[x][y]
    stack.push([[(x, y)], [(cost, 4)]])
    if cost == target:
        return [(x, y)]
    elif cost > target:
        return []
    else:
        while True:
            try:
                crazy_pop = stack.pop()
            except EmptyStackError:
                return []
            old_cost=crazy_pop[1][-1][0]
            if old_cost == target:
                return crazy_pop[0]

            for child in reversed(c_direction(crazy_pop[0][-1], grid, set(crazy_pop[0]),crazy_pop[1][-1])):
                x,y=child[0]
                new_cost = old_cost + grid[x][y]
                if new_cost > target:
                    continue
                else:
                    stack.push([list(crazy_pop[0]) + [(x, y)], list(crazy_pop[1]) + [[new_cost, child[2]]]])
    # Replace pass above with your code
'''
def c_direction(element, grid, chain, support_element):

    
    This is a code skeleton, I have removed parts of the code, I thought
    were not necessary to this code Review
    In case you feel the need to see the whole thing, please let me know.
    
    
    1=North
    2=South
    3=East
    4=West
    

    #{element} is a location on the grid
    #{chain} is all the locations previously seen [removed the iteration]
    #{value} gives the sum of the grid locations seen before arriving at
    #that point
    #{direction_flag} gives the direction in which the node was discovered.
    children = []
    direction_flag=support_element[1]
    if direction_flag == 1:
        val=element[0] - 1
        if element[0] > 0 and (val, element[1]) not in chain:
            children += [((val, element[1]), support_element[0], 1)]
        val=element[1] + 1
        if element[1] < 9 and (element[0], val) not in chain:
            children += [((element[0], val), support_element[0], 3)]
        val=element[1] - 1
        if element[1] > 0 and (element[0], val) not in chain:
            children += [((element[0], val), support_element[0], 4)]
        return children

    elif direction_flag == 2:
        val=element[0] + 1
        if element[0] < 9 and (val, element[1]) not in chain:
            children += [((val, element[1]), support_element[0], 2)]
        val=element[1] - 1
        if element[1] > 0 and (element[0], val) not in chain:
            children += [((element[0], val), support_element[0], 4)]
        val= element[1] + 1
        if element[1] < 9 and (element[0], val) not in chain:
            children += [((element[0], val), support_element[0], 3)]
        return children

    elif direction_flag == 3:
        val=element[1] + 1
        if element[1] < 9 and (element[0], val) not in chain:
            children += [((element[0], val), support_element[0], 3)]
        val=element[0] + 1
        if element[0] < 9 and (val, element[1]) not in chain:
            children += [((val, element[1]), support_element[0], 2)]
        val=element[0] - 1
        if element[0] > 0 and (val, element[1]) not in chain:
            children += [((val, element[1]), support_element[0], 1)]
        return children

    elif direction_flag == 4:
        val=element[1] - 1
        if element[1] > 0 and (element[0], val) not in chain:
            children += [((element[0], val), support_element[0], 4)]
        val=element[0] - 1
        if element[0] > 0 and (val, element[1]) not in chain:
            children += [((val, element[1]), support_element[0], 1)]
        val=element[0] + 1
        if element[0] < 9 and (val, element[1]) not in chain:
            children += [((val, element[1]), support_element[0], 2)]
        return children

    else:
        val = element[0] - 1
        if element[0] > 0 and (val, element[1]) not in chain:
            children += [((val, element[1]), support_element[0], 1)]
        val = element[1] + 1
        if element[1] < 9 and (element[0], val) not in chain:
            children += [((element[0], val), support_element[0], 3)]
        val = element[1] - 1
        if element[1] > 0 and (element[0], val) not in chain:
            children += [((element[0], val), support_element[0], 4)]
        val = element[0] + 1
        if element[0] < 9 and (val, element[1]) not in chain:
            children += [((val, element[1]), support_element[0], 2)]
        return children
'''
'''
def c_direction(element, grid, chain, support_element):
    GRID_SIZE = 10
    children = []

    OFFSET = [
        (-1, 0),  # north
        ( 0,+1),  # east
        (+1, 0),  # south
        ( 0,-1),  # west
    ]
    
    cost,c_direction=support_element
    x, y = element
    loop_counter=0

    while loop_counter<4:
        direction=c_direction % 4
        dx, dy = OFFSET[direction]
        cx, cy = dx + x, dy + y
        loop_counter += 1
        c_direction += 1
        if (cx, cy) in chain:
            continue
        if cx not in range(GRID_SIZE) or cy not in range(GRID_SIZE):
            continue
        children += [((cx, cy), cost, direction)]

    return children
'''

def c_direction(element, grid, chain, support_element):
    GRID_SIZE = 10
    children = []

    '''
    OFFSET = [
        (-1, 0, 0),  # north-0
        (0, +1, 1),  # east-1
        (+1, 0, 2),  # south-2
        (0, -1, 3),  # west-3
    ]

    
    dictionary= {
                  0:[OFFSET[0],OFFSET[1],OFFSET[3]],
                  1:[OFFSET[1],OFFSET[2],OFFSET[0]],
                  2:[OFFSET[2],OFFSET[3],OFFSET[1]],
                  3:[OFFSET[3],OFFSET[0],OFFSET[2]],
                  4:[OFFSET[0],OFFSET[1],OFFSET[2],OFFSET[3]]
             }
    '''
    dictionary= {
                  0: [(-1, 0, 0), (0, +1, 1), (0, -1, 3)],
                  1: [(0, +1, 1), (+1, 0, 2), (-1, 0, 0)],
                  2: [(+1, 0, 2), (0, -1, 3), (0, +1, 1)],
                  3: [(0, -1, 3), (-1, 0, 0), (+1, 0, 2)],
                  4: [(-1, 0, 0), (0, +1, 1), (+1, 0, 2), (0, -1, 3)]
                }

    x, y = element
    for dx,dy,new_direction in dictionary[support_element[1]]:
        cx, cy = dx + x, dy + y
        if cx not in range(GRID_SIZE) or cy not in range(GRID_SIZE):
            continue
        if (cx, cy) in chain:
            continue
        children += [((cx, cy), support_element[0], new_direction)]

    return children
#def quiz_8_runner():
def quiz_8_runner(for_seed, bound, x, y, target):
    try:
        #for_seed, bound, x, y, target = [int(x) for x in input('Enter five integers: ').split()]
        if bound < 1 or x not in range(10) or y not in range(10) or target < 0:
            raise ValueError
    except ValueError:
        print('Incorrect input, giving up.')
        sys.exit()
    seed(for_seed)
    #grid = [[randrange(bound) for _ in range(10)] for _ in range(10)]

    grid = [

        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 2, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    ]

    print('Here is the grid that has been generated:')
    display_grid(grid)
    path = explore_depth_first(x, y, target,grid)
    if not path:
        print(f'There is no way to get a sum of {target} starting from ({x}, {y})')
    else:
        print('With North as initial direction, and exploring the space clockwise,')
        print(f'the path yielding a sum of {target} starting from ({x}, {y}) is:')
        print(path)



import cProfile

#print('Chain Check')
cProfile.run('quiz_8_runner(0,1,5,5,5)')

#quiz_8_runner()

