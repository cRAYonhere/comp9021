preemptive_dict=dict()
primary_set={1, 2, 3, 4, 5, 6, 7, 8, 9}

sudoku =[
        [2, 0, 7, 6, 0, 0, 1, 0, 5],
        [0, 0, 0, 8, 1, 5, 4, 7, 0],
        [5, 8, 1, 2, 0, 0, 6, 0, 0],
        [1, 5, 9, 0, 8, 0, 0, 0, 4],
        [0, 0, 0, 0, 2, 9, 8, 5, 1],
        [0, 2, 4, 7, 5, 0, 0, 9, 0],
        [0, 1, 0, 5, 7, 2, 0, 0, 3],
        [7, 0, 2, 0, 0, 0, 5, 1, 8],
        [3, 9, 0, 0, 6, 8, 0, 4, 0]
        ]

for i in range(0,9):
    for j in range(0,9):
        if sudoku[i][j]==0:
            preemptive_dict[(i,j)]=primary_set
        else:
            preemptive_dict[(i,j)]=set(sudoku[i][j])

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
                box_to_location[box]=box_to_location[box].append((row % 9, column % 9))
            except KeyError:
                box_to_location[box]=[(row % 9, column % 9)]
            location_to_box[(row % 9, column % 9)]=box
    start_y += 3
    end_y += 3
    if start_y % 9 == 0:
        start_x += 3
        end_x += 3

def box_check(x,y):
    del_set=set()
    box_nb=location_to_box[(x,y)]
    for location in box_to_location[box_nb]:
        del_set.add(sudoku[location[0]][location[1]])
    temp_set = preemptive_dict[(x, y)] - del_set
    if len(temp_set) != len(preemptive_dict[(x, y)]):
        preemptive_dict[(x, y)] = temp_set
        return 1
    return 0

def column_check(x,y):
    del_set = set()
    for row in range(0,9):
        if sudoku[row][y] != 0:
            del_set.add(sudoku[row][y])
    temp_set=preemptive_dict[(x,y)]-del_set
    if len(temp_set) != len(preemptive_dict[(x,y)]):
        preemptive_dict[(x,y)]=temp_set
        return 1
    return 0

def row_check(x,y):
    del_set = set()
    for column in range(0,9):
        if sudoku[x][column] != 0:
            del_set.add(sudoku[x][column])
    temp_set=preemptive_dict[(x,y)]-del_set
    if len(temp_set) != len(preemptive_dict[(x,y)]):
        preemptive_dict[(x,y)]=temp_set
        return 1
    return 0

def refactor_preemptive_set(x,y):
    value=1
    while value:
        value=0
        value += row_check()
        value += column_check()
        value += box_check()

def create_preemptive_set():
    for x in range(0,9):
        for y in range(0,9):
            refactor_preemptive_set(x,y)

def refactor_sudoku():
    for key in preemptive_dict:
        if len(preemptive_dict[key])==1:
            sudoku[key[0]][key[1]]=preemptive_dict[key]
            refactor_preemptive_set()

def print_sudoku():
    for row in sudoku:
        print(row)

create_preemptive_set()
refactor_sudoku()