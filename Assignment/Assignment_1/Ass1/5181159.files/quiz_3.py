# Randomly generates a grid with 0s and 1s, whose dimension is controlled by user input,
# as well as the density of 1s in the grid, and finds out, for given step_number >= 1
# and step_size >= 2, the number of stairs of step_number many steps,
# with all steps of size step_size.
#
# A stair of 1 step of size 2 is of the form
# 1 1
#   1 1
#
# A stair of 2 steps of size 2 is of the form
# 1 1
#   1 1
#     1 1
#
# A stair of 1 step of size 3 is of the form
# 1 1 1
#     1
#     1 1 1
#
# A stair of 2 steps of size 3 is of the form
# 1 1 1
#     1
#     1 1 1
#         1
#         1 1 1
#
# The output lists the number of stairs from smallest step sizes to largest step sizes,
# and for a given step size, from stairs with the smallest number of steps to stairs
# with the largest number of stairs.
#
# Written by *** and Eric Martin for COMP9021


from random import seed, randint
import sys
from collections import defaultdict
from math import ceil


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))

def step_calc(row, column, step_size, dim, grid):
    new_grid=list(grid)
    steps=0
    val1=val2=0
    counter=0
    horizontal=vertical=0
    #print('row:'+str(row)+'\t column: '+str(column))
    #print(step_size,dim)
    while row+step_size <= dim or column+step_size <= dim:
        if column+step_size <= dim:
            counter=0
            for horizontal_movement in range(0,step_size): #Horizontal Shift
                val1=column+horizontal_movement
                #print('Column= column: '+str(column)+' horizontal_movement: '+str(horizontal_movement))
                #print('Horizontal Movement Coordinates: '+str(row)+' '+str(val1))
                if new_grid[row][val1] == 0:
                    return steps
                else:
                    continue
            horizontal+=1 #Horizontal
            column=column+horizontal_movement
                #print('Column:'+str(column))
        else:
            counter+=1
        if horizontal == 2 and vertical == 1:
            steps+=1
            horizontal=1
            vertical=0
        if row+step_size <= dim: 
            counter=0
            for vertical_movement in range(0, step_size): #vertical Shift
                val2=row+vertical_movement
                #print('Row= row: '+str(row)+' vertical_movement: '+str(vertical_movement))
                #print('Vertical Movement Coordinates: '+str(val2)+' '+str(column))
                if new_grid[val2][column] ==0:
                    return steps
                else:
                    continue
                
            vertical+=1 #Vertical
            row=row+vertical_movement
            #print('inside row: '+str(row)+'vertical_movement: '+str(vertical_movement))
            #print('Row:'+str(row))
        else:
            counter+=1
        if horizontal == 2 and vertical == 1:
            steps+=1
            horizontal=1
            vertical=0
        if counter >=2:
            break
    return steps      

def size_calc(dim,grid):
    #dictionary= {}
    element=0
    step_size= int(round(ceil(dim/2)))
    final_list = [[0,0,0]]
    #print(final_list)
    for step_size in range(2,step_size+1):
        for i in range(0, dim):
            for j in range(0, dim):
                steps=step_calc(i,j,step_size,dim,grid)
                if steps > 0:
                    find=0
                    for k in final_list:
                        if k[0] == step_size and k[1]== steps:
                            k[2]+=1
                            find=1
                    if find == 0:
                        final_list.append([step_size,steps,1])

    final_list.sort()
    del final_list[0]
    #[[2, 1, 12], [2, 2, 8], [2, 3, 3], [2, 4, 2], [3, 1, 9], [4, 1, 2]]
    for i in range(len(final_list)-1):
        if final_list[i][0]== final_list[i+1][0]:
            final_list[i][2]=final_list[i][2]-final_list[i+1][2]
    #print(final_list)
    del_flag=0
    while True:
        for i in range(len(final_list)):
            del_flag=0
            if final_list[i][2]==0:
                del final_list[i]
                del_flag=1
                break
        
        if del_flag==0:
            break

    #print(final_list)
    dictionary= defaultdict(list) 
    for i in range(len(final_list)):
        dictionary[final_list[i][0]].append(list((final_list[i][1],final_list[i][2])))
       

    #print(final_list)
    #print(dictionary)
            #Dictionary Key=step_size
            #Value Pair(number_of_steps, number_of_stairs_with_that_number_of_steps_of_that_step_size)   
    return dictionary

try:
    arg_for_seed, density, dim = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, density, dim = int(arg_for_seed), int(density), int(dim)
    if arg_for_seed < 0 or density < 0 or dim < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()
# A dictionary whose keys are step sizes, and whose values are pairs of the form
# (number_of_steps, number_of_stairs_with_that_number_of_steps_of_that_step_size),
# ordered from smallest to largest number_of_steps.
stairs = size_calc(dim, grid)
#print(stairs)
for step_size in sorted(stairs):
    print(f'\nFor steps of size {step_size}, we have:')
    for (nb_of_steps, nb_of_stairs) in stairs[step_size]:
        stair_or_stairs = 'stair' if nb_of_stairs == 1 else 'stairs'
        step_or_steps = 'step' if nb_of_steps == 1 else 'steps'
        print(f'     {nb_of_stairs} {stair_or_stairs} with {nb_of_steps} {step_or_steps}')
