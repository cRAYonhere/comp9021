from collections import defaultdict
import sys

mother_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
forced_dict = {1:0, 2:0, 3:0 , 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
empty_column_org=[[],[],[],[],[],[],[],[],[]]
empty_row_org=[[],[],[],[],[],[],[],[],[]]
empty_box_org=[[],[],[],[],[],[],[],[],[]]

'''
#Very Easy 
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
'''
'''
sudoku =[
        [0, 0, 1, 9, 0, 0, 0, 0, 8],
        [6, 0, 0, 0, 8, 5, 0, 3, 0],
        [0, 0, 7, 0, 6, 0, 1, 0, 0],
        [0, 3, 4, 0, 9, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 4, 2, 0],
        [0, 0, 5, 0, 7, 0, 9, 0, 0],
        [0, 1, 0, 8, 4, 0, 0, 0, 7],
        [7, 0, 0, 0, 0, 9, 2, 0, 0]
        ]
'''
sudoku =[
        [0, 3, 9, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 0, 0, 0, 7, 0],
        [0, 0, 0, 0, 1, 0, 9, 0, 4],
        [1, 0, 0, 4, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 8, 6, 0],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 1, 0, 0, 9, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 1, 0, 0, 8]
        ]
preemptive_dict=defaultdict(list)

box_list=[[],[],[],[],[],[],[],[],[]]
start_x=start_y=0
end_x=3
end_y=3

for box in range(0,9):
    for row in range(start_x,end_x):
        for column in range(start_y,end_y):
            box_list[box].append((row%9,column%9))
    start_y+=3
    end_y+=3
    if start_y%9==0:
        start_x+=3
        end_x+=3

def box_check():
    empty_box=list(empty_box_org)
    del_set=set()
    counter=0
    for box in box_list:
        for i in box:
            if sudoku[i[0]][i[1]] !=0 :
                del_set.add(sudoku[i[0]][i[1]])
        #print('the box has ',del_set)
        for cell in box:
            if sudoku[cell[0]][cell[1]] == 0:
                empty_box[counter].append((row, column))
                preemptive_dict[(cell[0],cell[1])] = mother_set-del_set
        del_set.clear()
        counter += 1
    '''
    print('Box Check')
    for key in preemptive_dict:
        print(key,preemptive_dict[key])
    '''
    return empty_box

def column_check():
    empty_column=list(empty_column_org)
    del_set = set()
    counter=0
    for column in range(9):
        for i in range(9):
            if sudoku[i][column]!=0:
                del_set.add(sudoku[i][column])
        for row in range(9):
            if sudoku[row][column]==0:
                empty_column[counter].append((row, column))
                preemptive_dict[(row,column)]=set(preemptive_dict[(row,column)])-del_set
        del_set.clear()
        counter+=1
    '''
    print('Column Check')
    for key in preemptive_dict:
        print(key,preemptive_dict[key])
    '''
    return empty_column


def row_check():
    empty_row=list(empty_row_org)
    del_set = set()
    counter=0
    for row in range(9):
        for i in range(9):
            if sudoku[row][i]!=0:
                del_set.add(sudoku[row][i])
        for column in range(9):
            if sudoku[row][column]==0:
                empty_row[counter].append((row,column))
                preemptive_dict[(row,column)]=set(preemptive_dict[(row,column)])-del_set
        del_set.clear()
        counter+=1
    return empty_row

def forced(empty_box, empty_row, empty_column):
    flag=1
    while flag==1:
        #column
        flag=0
        for element in mother_set:
            for column_number in empty_column:
                counter = 0
                for location in column_number:
                    if element in preemptive_dict[location]:
                        counter+=1
                        element_location=location
                if counter==1:
                    flag=1
                    print(f'Column Forced {element} in {element_location}')
                    sudoku[element_location[0]][element_location[1]]=element
                    del preemptive_dict[element_location]
                    Equalizer()
        #row
        for element in mother_set:
            for row_number in empty_row:
                counter = 0
                for location in row_number:
                    if location[0]==1 and element==9:
                        print(f'{element} in {location}={preemptive_dict[location]}')
                    if element in preemptive_dict[location]:
                        counter += 1
                        element_location = location
                if counter == 1:
                    flag = 1
                    print(f'Row Forced {element} in {element_location}')
                    sudoku[element_location[0]][element_location[1]] = element
                    del preemptive_dict[element_location]
                    Equalizer()
        #box
        for element in mother_set:
            for box in empty_box:
                counter = 0
                for location in box:
                    #print(f'{element} in {preemptive_dict[location]}')
                    if element in preemptive_dict[location]:
                        counter += 1
                        element_location = location
                if counter == 1:
                    flag = 1
                    print(f'Box Forced {element} in {element_location}')
                    sudoku[element_location[0]][element_location[1]] = element
                    del preemptive_dict[element_location]
                    Equalizer()


def Equalizer():
    counter=0
    flag=1
    while flag !=0:
        flag=0
        print('Sudoku: ')
        counter += 1
        for i in sudoku:
            print(i)
        empty_box=box_check()
        empty_row=row_check()
        empty_column=column_check()
        for key in preemptive_dict:
            if len(preemptive_dict[key])==1:
                print(f'Inserting {preemptive_dict[key]} in {key}')
                sudoku[key[0]][key[1]]=preemptive_dict[key].pop()
                del preemptive_dict[key]
                flag=1
                for key in preemptive_dict:
                    print(key, preemptive_dict[key])
    forced(empty_box,empty_row,empty_column)

Equalizer()


