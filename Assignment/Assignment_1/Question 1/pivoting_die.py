#!/usr/bin/env python

'''
The code snipet for the spiral matrix is taken from stackoverflow
Link: https://stackoverflow.com/questions/36834505/creating-a-spiral-array-in-python
The original code was posted by J.F. Sebastian
The Spiral Matrix code snipet is licensed under cc by-sa 3.0 with attribution requirement
'''

from math import ceil, sqrt
NORTH, SOUTH, WEST, EAST = (0, -1), (0, 1), (-1, 0), (1, 0) # directions
turn_right = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH} # old -> new direction
front=0
top=1
right_side=2
dim=0
value_view=[2,3,1]
#value_view=[2,1,4]
def east():
    #print('Roll East')
    temp=value_view[top]
    value_view[top]=7-value_view[right_side]
    value_view[right_side]=temp
    #print(value_view)
    
def west():
    #print('Roll West')
    temp=value_view[1]
    value_view[1]=value_view[2]
    value_view[2]=7-temp
    #print(value_view)
    
def north():
    #print('Roll North')
    temp= value_view[1]
    value_view[1]=value_view[0]
    value_view[0]=7-temp
    #print(value_view)
    
def south():
    #print('Roll South')
    temp=value_view[front]
    value_view[front]=value_view[top]
    value_view[top]=7-temp
    #print(value_view)

def spiral(width, height):
    if width < 1 or height < 1:
        raise ValueError
    x, y = width // 2, height // 2 # start near the center
    dx, dy = NORTH # initial direction
    matrix = [[None] * width for _ in range(height)]
    count = 0
    
    #print('Starting Condition: ', end='')
    #print(value_view)
    #print(' F  T  S')
    while True:
        count += 1
        matrix[y][x] = count # visit
        # try to turn right
        new_dx, new_dy = turn_right[dx,dy]

        new_x, new_y = x + new_dx, y + new_dy
        if count < dim:
            if (0 <= new_x < width and 0 <= new_y < height and
                matrix[new_y][new_x] is None): # can turn right
                    #print(new_dx,new_dy)
                if new_dx == 0:
                    if new_dy == -1:
                        flag=1
                        north()
                    elif new_dy == 1:
                        flag=2
                        south()
                elif new_dx == -1:
                    flag=3
                    west()
                elif new_dx == 1:
                    flag=4
                    east()
                x, y = new_x, new_y
                dx, dy = new_dx, new_dy
            else: # try to move straight

                if flag ==1:
                    north()
                elif flag ==2:
                    south()
                elif flag ==3:
                    west()
                elif flag ==4:
                    east()
                x, y = x + dx, y + dy
                if not (0 <= x < width and 0 <= y < height):

                    return #matrix # nowhere to go
        else:
            return
while True:
    try:
        dim=int(input('Enter the desired goal cell number: '))
        if dim < 1:
            raise ValueError
        break
    except ValueError:
        print('Incorrect value, try again')
cell_size=ceil(sqrt(dim))+1
spiral(cell_size,cell_size)
print('On cell '+str(dim)+', '+str(value_view[top])+' is at the top, '+str(value_view[front])+' at the front, and '+str(value_view[right_side])+' on the right.')
