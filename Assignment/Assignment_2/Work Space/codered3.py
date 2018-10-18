from copy import deepcopy
import sys

option_dict=dict()
preemptive_dict=dict()
primary_list=[1, 2, 3, 4, 5, 6, 7, 8, 9]

box_list=[[],[],[],[],[],[],[],[],[]]
column_list=[[],[],[],[],[],[],[],[],[]]
row_list=[[],[],[],[],[],[],[],[],[]]
#'''
#Shortz301
sudoku =[
        [None,     3,    9,    5, None, None, None, None, None],
        [None,  None, None,    8, None, None, None,    7, None],
        [None,  None, None, None,    1, None,    9, None,    4],
        [   1,  None, None,    4, None, None, None, None,    3],
        [None,  None, None, None, None, None, None, None, None],
        [None,  None,    7, None, None, None,    8,    6, None],
        [None,  None,    6,    7, None,    8,    2, None, None],
        [None,     1, None, None,    9, None, None, None,    5],
        [None,  None, None, None, None,    1, None, None,    8]
        ]
#'''
'''
#Very Easy
sudoku =[
        [   2, None,    7,    6, None, None,    1, None,    5],
        [None, None, None,    8,    1,    5,    4,    7, None],
        [   5,    8,    1,    2, None, None,    6, None, None],
        [   1,    5,    9, None,    8, None, None, None,    4],
        [None, None, None, None,    2,    9,    8,    5,    1],
        [None,    2,    4,    7,    5, None, None, None, None],
        [None,    1, None,    5,    7,    2, None, None,    3],
        [   7, None,    2, None, None, None,    5,    1,    8],
        [   3,    9, None, None,    6,    8, None,    4, None]
        ]
'''
def init_preemptive_dict():
    flag=False
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == None:
                option_dict[(i,j)]=primary_list
                flag=True
    return flag

#For Box
box_to_location= dict()
location_to_box= dict()
start_x = start_y = 0
end_x = 3
end_y = 3
for box in range(0, 9):
    for row in range(start_x, end_x):
        for column in range(start_y, end_y):
            try:
                box_to_location[box]=box_to_location[box]+[(row % 9, column % 9)]
            except KeyError:
                box_to_location[box]=[(row % 9, column % 9)]
            except AttributeError:
                box_to_location[box] = [(row % 9, column % 9)]
            location_to_box[(row % 9, column % 9)]=box
    start_y += 3
    end_y += 3
    if start_y % 9 == 0:
        start_x += 3
        end_x += 3

def preasses_builder(row,column):
    try:
        if sudoku[row][column] in primary_list:
            box=location_to_box[(row,column)]
            if sudoku[row][column] not in box_list[box]:
                box_list[box].append(sudoku[row][column])
            else:
                print(f'Duplication in box number {box} detected.')
                sys.exit()
            if sudoku[row][column] not in row_list[row]:
                row_list[row].append(sudoku[row][column])
            else:
                print(f'Duplication in row number {row} detected')
                sys.exit()
            if sudoku[row][column] not in column_list[column]:
                column_list[column].append(sudoku[row][column])
            else:
                print(f'Duplication in column number {column} detected')
                sys.exit()
    except IndexError:
        print(f'({row},{column}) doesn\'t exist.')

def box_check(x,y,box_list):
    for location in box_to_location[location_to_box[(x,y)]]:
        if sudoku[location[0]][location[1]] is None:
            option_dict[location]=list(set(option_dict[location])-set(box_list[location_to_box[location]]))

def column_check(y,column_list):
    for row in range(9):
        if sudoku[row][y] is None:
            option_dict[(row,y)]=list(set(option_dict[(row,y)])-set(column_list[y]))

def row_check(x,row_list):
    for column in range(9):
        if sudoku[x][column] is None:
            option_dict[(x,column)]=list(set(option_dict[(x,column)])-set(row_list[x]))

def forced_asses(x=-1,y=-1):
    if len(option_dict) > 0:
        if x==-1 or y==-1:
            for row in range(9):
                for column in range(9):
                    preasses_builder(row, column)
            for row in range(9):
                for column in range(9):
                    box_check(row,column,box_list)
                    column_check(column,column_list)
                    row_check(row,row_list)
        else:
            row = x
            column = y
            preasses_builder(row, column)
            box_check(row, column, box_list)
            column_check(column, column_list)
            row_check(row, row_list)
        forced()




def print_sudoku():
    print('Sudoku')
    for row in sudoku:
        for i in row:
            if i == None:
                print('0 ',end='')
            else:
                print(f'{i} ',end='')
        print()

def forced():
    box_count = []
    row_count = []
    column_count = []

    for i in range(9):
        box_count.append([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        row_count.append([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        column_count.append([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])

    for key in option_dict:
        for item in option_dict[key]:
            #delete_me +=1
        #column
            column_count[key[1]][item - 1][0] = key[0]
            column_count[key[1]][item - 1][1] = key[1]
            column_count[key[1]][item - 1][2] += 1
        #row
            row_count[key[0]][item - 1][0] = key[0]
            row_count[key[0]][item - 1][1] = key[1]
            row_count[key[0]][item - 1][2] += 1
        #box
            box_count[location_to_box[key]][item - 1][0] = key[0]
            box_count[location_to_box[key]][item - 1][1] = key[1]
            box_count[location_to_box[key]][item - 1][2] += 1

    for box_nb in range(9):
        for number in range(9):
            x,y,counter=box_count[box_nb][number]
            if counter==1:
                flag = 0
                if row_count[x][number][2]==1:
                    #print(f'Row Added {number+1} at ({x},{y})')
                    sudoku[x][y] = number + 1
                    try:
                        del option_dict[(x,y)]
                    except KeyError:
                        return
                    flag=1
                elif column_count[y][number][2]==1:
                    #print(f'Column Added {number+1} at ({x},{y})')
                    sudoku[x][y]=number+1
                    try:
                        del option_dict[(x, y)]
                    except KeyError:
                        return
                    flag=1
                if flag ==1:
                    row_count[x][number]=[0,0,0]
                    column_count[y][number]=[0,0,0]
                    box_count[box_nb][number]=[0,0,0]
                    forced_asses(x,y)

def preemptive_asses(x=-1,y=-1):

    pass
def preemptive_set():
    for key in option_dict:
        #box
        for location in box_to_location[location_to_box[key]]:
            try:
                if set(option_dict[location]).issubset(set(option_dict[key])):
                    try:
                        #print('Box')
                        if location not in preemptive_dict[key]:
                            preemptive_dict[key]=preemptive_dict[key]+[location]
                    except KeyError:
                        preemptive_dict[key] =[set(option_dict[key])]+[location]
            except KeyError:
                continue
        #column
        for x in range(9):
            try:
                if set(option_dict[(x,key[1])]).issubset(set(option_dict[key])):
                    try:
                        #print('column')
                        if (x, key[1]) not in preemptive_dict[key]:
                            preemptive_dict[key]=preemptive_dict[key]+[(x,key[1])]
                    except KeyError:
                        preemptive_dict[key] =[set(option_dict[key])]+[(x,key[1])]
            except KeyError:
                continue
        #row
        for y in range(9):
            try:
                if set(option_dict[(key[0],y)]).issubset(set(option_dict[key])):
                    try:
                        #print('row')
                        if (key[0], y) not in preemptive_dict[key]:
                            preemptive_dict[key]=preemptive_dict[key]+[(key[0],y)]
                    except KeyError:
                        preemptive_dict[key] =[set(option_dict[key])]+[(key[0],y)]
            except KeyError:
                continue
        if len(preemptive_dict[key]) != len(preemptive_dict[key][0])+1:
            del preemptive_dict[key]
        for key in preemptive_dict:
            print(key, preemptive_dict[key])
        #input()

init_preemptive_dict()
print_sudoku()
forced_asses()
#print(option_dict)
preemptive_set()
#print_sudoku()
#preemptive_asses()
#print(preemptive_dict)
#print(option_dict)

