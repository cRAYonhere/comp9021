import sys
from copy import deepcopy

class SudokuError(Exception):
    def __init__(self, message):
        self.message = message

class Sudoku:
    def __init__(self, args):

        with open(args) as f_in:
            lines = (line.rstrip() for line in f_in)
            lines = list(line.replace(' ', '') for line in lines if line)  # Non-blank lines in a list
        self.filename=str(args)
        self.lines=lines
        self.build_box_dictionary()
        self.primary_set=[1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.options_dict={}
        self.preemptive_dict={}
        self.copy_options_dict=dict()

        try:
            self.sudoku = [[int(character) for character in element] for element in self.lines]
        except ValueError:
            raise SudokuError('Incorrect input')

        if len(self.sudoku)<9:
            raise SudokuError('Incorrect input')
        for row in self.sudoku:
            if len(row)<9:
                raise SudokuError('Incorrect input')
        self.init_options_dict()

    def preassess(self,function_name=0):
        box_list = [[], [], [], [], [], [], [], [], []]
        column_list = [[], [], [], [], [], [], [], [], []]
        row_list = [[], [], [], [], [], [], [], [], []]
        primary_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        frequency = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0]]
        for row in range(9):
            for column in range(9):
                if self.sudoku[row][column] !=0:
                    frequency[self.sudoku[row][column]-1][1]+=1
                #print(frequency)
                if self.sudoku[row][column] in primary_list:
                    box = self.location_to_box[(row, column)]
                    if self.sudoku[row][column] not in box_list[box]:
                        box_list[box].append(self.sudoku[row][column])
                    else:
                        print('There is clearly no solution.')
                        sys.exit()
                        return False
                    if self.sudoku[row][column] not in row_list[row]:
                        row_list[row].append(self.sudoku[row][column])
                    else:
                        print('There is clearly no solution.')
                        sys.exit()
                        return False
                    if self.sudoku[row][column] not in column_list[column]:
                        column_list[column].append(self.sudoku[row][column])
                    else:
                        print('There is clearly no solution.')
                        sys.exit()
                        return False

        self.box_list=box_list
        self.row_list=row_list
        self.column_list=column_list
        if function_name==0:
            print('There might be a solution.')
        if function_name==1:
            self.frequency=frequency
        return True

    def init_options_dict(self):
        flag = False
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] not in self.primary_set:
                    self.options_dict[(i, j)] = self.primary_set
                    flag = True
        return flag
    def build_box_dictionary(self):
        box_to_location = dict()
        location_to_box = dict()
        start_x = start_y = 0
        end_x = 3
        end_y = 3
        for box in range(0, 9):
            for row in range(start_x, end_x):
                for column in range(start_y, end_y):
                    try:
                        box_to_location[box] = box_to_location[box] + [(row % 9, column % 9)]
                    except KeyError:
                        box_to_location[box] = [(row % 9, column % 9)]
                    except AttributeError:
                        box_to_location[box] = [(row % 9, column % 9)]
                    location_to_box[(row % 9, column % 9)] = box
            start_y += 3
            end_y += 3
            if start_y % 9 == 0:
                start_x += 3
                end_x += 3
            self.box_to_location=box_to_location
            self.location_to_box=location_to_box

    def bare_tex_output(self,function_name=0):

        header = r'''\documentclass[10pt]{article}
        \usepackage[left=0pt,right=0pt]{geometry}
        \usepackage{tikz}
        \usetikzlibrary{positioning}
        \usepackage{cancel}
        \pagestyle{empty}

        \newcommand{\N}[5]{\tikz{\node[label=above left:{\tiny #1},
                                       label=above right:{\tiny #2},
                                       label=below left:{\tiny #3},
                                       label=below right:{\tiny #4}]{#5};}}

        \begin{document}

        \tikzset{every node/.style={minimum size=.5cm}}

        \begin{center}
        \begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline'''

        footer = r'''\end{tabular}
        \end{center}

        \end{document}
        '''
        cancel_header = '\cancel{'
        cancel_footer = '}'

        if function_name==0:
            filename = str(self.filename)[0:-4] + '_bare_temp' + '.tex'
        elif function_name==1:
            filename = str(self.filename)[0:-4] + '_forced_temp' + '.tex'
        elif function_name==2:
            filename = str(self.filename)[0:-4] + '_marked_temp' + '.tex'
        with open(filename, 'a') as fstream:
            fstream.write(header)
            for row in range(9):
                row_list = ['', '', '', '', '', '', '', '', '']
                markup = [['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', ''],
                          ['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', ''],
                          ['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', ''],
                          ['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', ''],
                          ['', '', '', '', '', '', '', '', '']]

                for column in range(9):
                    if self.sudoku[row][column] in self.primary_set:
                        row_list[column] = self.sudoku[row][column]

                    else:
                        if function_name==2:
                            try:
                                # temp_list=preemptive_dict[(row,column)][0]
                                for option in self.options_dict[(row, column)]:
                                    if option < 0:
                                        markup[column][option - 1] = cancel_header + str(abs(option)) + cancel_footer
                                    else:
                                        markup[column][option - 1] = abs(option)
                            except KeyError:
                                continue
                ending = ''
                if (row + 1) % 3 == 0:
                    ending = '\hline'
                fstream.write(
                    f'% Line {row} \n\\N {{{markup[0][0]} {markup[0][1]}}}{{{markup[0][2]} {markup[0][3]}}}{{{markup[0][4]} {markup[0][5]}}}{{{markup[0][6]} {markup[0][7]} {markup[0][8]}}}{{{row_list[0]}}} & \\N {{{markup[1][0]} {markup[1][1]}}}{{{markup[1][2]} {markup[1][3]}}}{{{markup[1][4]} {markup[1][5]}}}{{{markup[1][6]} {markup[1][7]} {markup[1][8]}}}{{{row_list[1]}}} & \\N {{{markup[2][0]} {markup[2][1]}}}{{{markup[2][2]} {markup[2][3]}}}{{{markup[2][4]} {markup[2][5]}}}{{{markup[2][6]} {markup[2][7]} {markup[2][8]}}}{{{row_list[2]}}} &\n\\N {{{markup[3][0]} {markup[3][1]}}}{{{markup[3][2]} {markup[3][3]}}}{{{markup[3][4]} {markup[3][5]}}}{{{markup[3][6]} {markup[3][7]} {markup[3][8]}}}{{{row_list[3]}}} & \\N {{{markup[4][0]} {markup[4][1]}}}{{ {markup[4][2]} {markup[4][3]} }}{{ {markup[4][4]} {markup[4][5]} }}{{ {markup[4][6]} {markup[4][7]} {markup[4][8]} }}{{{row_list[4]}}} & \\N {{{markup[5][0]} {markup[5][1]}}}{{{markup[5][2]} {markup[5][3]}}}{{{markup[5][4]} {markup[5][5]}}}{{{markup[5][6]} {markup[5][7]} {markup[5][8]}}}{{{row_list[5]}}} &\n\\N {{{markup[6][0]} {markup[6][1]}}}{{{markup[6][2]} {markup[6][3]}}}{{{markup[6][4]} {markup[6][5]}}}{{{markup[6][6]} {markup[6][7]} {markup[6][8]}}}{{{row_list[6]}}} & \\N {{{markup[7][0]} {markup[7][1]}}}{{{markup[7][2]} {markup[7][3]}}}{{{markup[7][4]} {markup[7][5]}}}{{{markup[7][6]} {markup[7][7]} {markup[7][8]}}}{{{row_list[7]}}} & \\N {{{markup[8][0]} {markup[8][1]}}}{{{markup[8][2]} {markup[8][3]}}}{{{markup[8][4]} {markup[8][5]}}}{{{markup[8][6]} {markup[8][7]} {markup[8][8]}}}{{{row_list[8]}}} \\\ \hline{ending}')
            fstream.write(footer)
            print('Tex File Created.')

    def box_options_builder(self, x, y, ):
        for location in self.box_to_location[self.location_to_box[(x, y)]]:
            if self.sudoku[location[0]][location[1]] not in self.primary_set:
                temp_list=list(set(self.options_dict[location]) - set(self.box_list[self.location_to_box[location]]))
                if len(temp_list)==1:
                    #print(f'Options Dict Added {temp_list[0]} at location ({location[0]},{location[1]})')
                    self.sudoku[location[0]][location[1]]= temp_list[0]
                    self.copy_options_dict[location] = [i * -1 for i in self.options_dict[location]]
                    del self.options_dict[location]
                    if self.preassess(function_name=1):
                        self.box_options_builder(location[0], location[1])
                        self.row_options_builder(location[0])
                        self.column_options_builder(location[1])
                else:
                    self.options_dict[location] = temp_list
    def column_options_builder(self, y):
        for row in range(9):
            if self.sudoku[row][y] not in self.primary_set:
                temp_list=list(set(self.options_dict[(row, y)]) - set(self.column_list[y]))
                if len(temp_list) ==1:
                    #print(f'Options Dict Added {temp_list[0]} at location ({row},{y})')
                    self.sudoku[row][y]=temp_list[0]
                    self.copy_options_dict[(row, y)] = [i * -1 for i in self.options_dict[(row, y)]]
                    del self.options_dict[(row, y)]
                    if self.preassess(function_name=1):
                        self.box_options_builder(row, y)
                        self.row_options_builder(row)
                        self.column_options_builder(y)
                else:
                    self.options_dict[(row, y)] = temp_list

    def row_options_builder(self,x):
        for column in range(9):
            if self.sudoku[x][column] not in self.primary_set:
                temp_list=list(set(self.options_dict[(x, column)]) - set(self.row_list[x]))
                if len(temp_list)==1:
                    #print(f'Options Dict Added {temp_list[0]} at location ({x},{column})')
                    self.sudoku[x][column]=temp_list[0]
                    self.copy_options_dict[(x, column)] = [i * -1 for i in self.options_dict[(x, column)]]
                    del self.options_dict[(x, column)]
                    if self.preassess(function_name=1):
                        self.box_options_builder(x, column)
                        self.row_options_builder(x)
                        self.column_options_builder(column)
                else:
                    self.options_dict[(x, column)] = list(set(self.options_dict[(x, column)]) - set(self.row_list[x]))

    def build_all_options(self):
        for row in range(9):
            for column in range(9):
                self.box_options_builder(row,column)
                self.row_options_builder(row)
                self.column_options_builder(column)

    def forced_tex_output(self, function_name=0):
        self.preassess(function_name=1)
        if function_name==0:
            self.build_all_options()
        if function_name==1:
            self.build_all_options()
        self.frequency.sort(key= lambda x:x[1],reverse=True)
        #print('Frequency:',self.frequency)
        worked_flag=0
        '''
        for key in self.options_dict:
            print(key,self.options_dict[key])
        '''
        flag=1
        while flag==1:
            flag=0
            #print('length of options_dict: ', len(self.options_dict))
            for element in range(9):
                #print(self.frequency[element][0])
                if self.frequency[element][1]>1:
                    for box in range(9):
                        counter=0
                        for location in self.box_to_location[box]:
                            try:
                                if self.frequency[element][0] in self.options_dict[location]:
                                    counter+=1
                                    final_location=location
                            except KeyError:
                                continue
                        if counter==1:
                            #print(f'Added {self.frequency[element][0]} at location ({final_location[0]},{final_location[1]})')
                            self.sudoku[final_location[0]][final_location[1]]=self.frequency[element][0]
                            del self.options_dict[final_location]
                            if self.preassess(function_name=1):
                                self.box_options_builder(final_location[0], final_location[1])
                                self.row_options_builder(final_location[0])
                                self.column_options_builder(final_location[1])
                            flag=1
                            worked_flag=1
        if function_name !=0:
            if worked_flag==1:
                return True
            return False
        '''
        for row in self.sudoku:
            print(row)
        '''
        if function_name==0:
            self.bare_tex_output(function_name=1)

    def preemptive_set_builder(self, function_name=0):
        preemptive_dict = dict()
        for key in self.options_dict:
            for location in self.box_to_location[self.location_to_box[key]]:
                try:
                    if set(self.options_dict[location]).issubset(set(self.options_dict[key])):
                        try:
                            preemptive_dict[(key[0],key[1],'b')] = preemptive_dict[(key[0],key[1],'b')] + [location]
                        except KeyError:
                            preemptive_dict[(key[0],key[1],'b')] = [set(self.options_dict[key])] + [location]
                except KeyError:
                    pass
            try:
                if len(preemptive_dict[(key[0],key[1],'b')][0]) != len(preemptive_dict[(key[0],key[1],'b')])-1:
                    del preemptive_dict[(key[0],key[1],'b')]
            except KeyError:
                pass

            # column
            for x in range(9):
                try:
                    if set(self.options_dict[(x, key[1])]).issubset(set(self.options_dict[key])):
                        try:
                            # print('column')
                            preemptive_dict[(key[0],key[1],'c')] = preemptive_dict[(key[0],key[1],'c')] + [(x, key[1])]
                        except KeyError:
                            preemptive_dict[(key[0],key[1],'c')] = [set(self.options_dict[key])] + [(x, key[1])]
                except KeyError:
                    pass
            try:
                if len(preemptive_dict[(key[0],key[1],'c')][0]) != len(preemptive_dict[(key[0],key[1],'c')])-1:
                    del preemptive_dict[(key[0],key[1],'c')]
            except KeyError:
                pass

            # row
            for y in range(9):
                try:
                    if set(self.options_dict[(key[0], y)]).issubset(set(self.options_dict[key])):
                        try:
                            # print('row')
                            preemptive_dict[(key[0],key[1],'r')] = preemptive_dict[(key[0],key[1],'r')] + [(key[0], y)]
                        except KeyError:
                            preemptive_dict[(key[0],key[1],'r')] = [set(self.options_dict[key])] + [(key[0], y)]
                except KeyError:
                    pass
            try:
                if len(preemptive_dict[(key[0],key[1],'r')][0]) != len(preemptive_dict[(key[0],key[1],'r')])-1:
                    del preemptive_dict[(key[0],key[1],'r')]
            except KeyError:
                pass
        #for key in preemptive_dict:
            #print(key, preemptive_dict[key])
        self.preemptive_dict=preemptive_dict
        #for key in self.preemptive_dict:
            #print(key,self.preemptive_dict[key])

    def marked_tex_output(self):

        self.forced_tex_output(function_name=1)
        self.bare_tex_output(function_name=2)

    def worked_tex_output(self, function_name=0):

        self.forced_tex_output(function_name=1)
        #for key in self.options_dict:
            #print(key,self.options_dict[key])
        self.copy_options_dict = deepcopy(self.options_dict)
        flag = 1
        while flag == 1:
            flag = 0
            self.preemptive_set_builder()
            for key in self.preemptive_dict:
                #print('Working on: ',key,self.preemptive_dict[key])
                if key[2]=='b':
                    for location in self.box_to_location[self.location_to_box[(key[0],key[1])]]:
                        if self.sudoku[location[0]][location[1]] not in self.primary_set and \
                                        location not in self.preemptive_dict[key][1:len(self.preemptive_dict[key])]:
                            for element in self.preemptive_dict[key][0]:
                                if element in self.options_dict[location]:
                                    self.copy_options_dict[location][self.copy_options_dict[location].index(element)] *= (-1)
                                    del self.options_dict[location][self.options_dict[location].index(element)]
                elif key[2]=='r':
                    for column in range(9):
                        if self.sudoku[key[0]][column] not in self.primary_set and (key[0], column) not in \
                                self.preemptive_dict[key][1:len(self.preemptive_dict[key])]:
                            for set_element in self.preemptive_dict[key][0]:
                                if set_element in self.options_dict[(key[0], column)]:
                                    self.copy_options_dict[(key[0], column)][self.copy_options_dict[(key[0], column)].index(set_element)] *= (-1)
                                    del self.options_dict[(key[0], column)][self.options_dict[(key[0], column)].index(set_element)]
                            #print(f'New option:({key[0]},{column})', self.options_dict[(key[0], column)])
                elif key[2]=='c':
                    for row in range(9):
                        if self.sudoku[row][key[1]] not in self.primary_set and (row,key[1]) not in self.preemptive_dict[key][1:len(self.preemptive_dict[key])]:
                            for set_element in self.preemptive_dict[key][0]:
                                if set_element in self.options_dict[(row,key[1])]:
                                    self.copy_options_dict[(row,key[1])][self.copy_options_dict[(row,key[1])].index(set_element)]*=(-1)
                                    del self.options_dict[(row,key[1])][self.options_dict[(row,key[1])].index(set_element)]
                            #print(f'New option:({row},{key[1]})', self.options_dict[(row,key[1])])
                if self.update_sudoku():
                    flag=1
        for row in self.sudoku:
            print(row)
        for key in self.copy_options_dict:
            print(key,self.copy_options_dict[key])
    def update_sudoku(self):
        flag=0
        delete_keys=[]
        for key in self.options_dict:
            if len(self.options_dict[key]) == 1:
                #print(f'Adding {self.options_dict[key][0]} at location ({key[0]},{key[1]})')
                self.sudoku[key[0]][key[1]] = self.options_dict[key][0]
                #for row in self.sudoku:
                    #print(row)
                delete_keys.append(key)

        for key in delete_keys:
            #print(f'Deleting {key}')
            self.copy_options_dict[key] = [i * -1 for i in self.options_dict[key]]
            del self.options_dict[key]
            flag_build_options=1

        if self.preassess(function_name=1):
            for key in delete_keys:
                self.box_options_builder(key[0], key[1])
                self.row_options_builder(key[0])
                self.column_options_builder(key[1])
            flag=1
        else:
            #print('Preasses Failed.')
            sys.exit()
        box_count = []
        row_count = []
        column_count = []
        return_flag=0
        flag=1
        while flag==1:
            flag=0

            for i in range(9):
                box_count.append(
                    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
                row_count.append(
                    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
                column_count.append(
                    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])

            for key in self.options_dict:
                for item in self.options_dict[key]:
                    # column
                    column_count[key[1]][item - 1][0] = key[0]
                    column_count[key[1]][item - 1][1] = key[1]
                    column_count[key[1]][item - 1][2] += 1
                    # row
                    row_count[key[0]][item - 1][0] = key[0]
                    row_count[key[0]][item - 1][1] = key[1]
                    row_count[key[0]][item - 1][2] += 1
                    # box
                    box_count[self.location_to_box[key]][item - 1][0] = key[0]
                    box_count[self.location_to_box[key]][item - 1][1] = key[1]
                    box_count[self.location_to_box[key]][item - 1][2] += 1
            #for row in box_count:
                #print(row)
            for row in range(9):
                for column in range(9):
                    box_x, box_y, box_counter = box_count[row][column]
                    row_x, row_y, row_counter = row_count[row][column]
                    column_x, column_y, column_counter = column_count[row][column]
                    try:
                        if box_counter == 1 and self.options_dict[(box_x, box_y)]:
                            #print(f'Box Added {column+1} at ({box_x},{box_y})')
                            self.sudoku[box_x][box_y] = column + 1
                            #print(f'Box Deleting ({box_x},{box_y})')
                            self.copy_options_dict[(box_x, box_y)] = [i * -1 for i in
                                                                   self.options_dict[(box_x, box_y)]]
                            del self.options_dict[(box_x, box_y)]
                            row_count[box_x][box_y] = column_count[box_y][column] = box_count[row][column] = [0, 0, 0]
                            if self.preassess(function_name=1):
                                self.box_options_builder(box_x, box_y)
                                self.column_options_builder(box_y)
                                self.row_options_builder(box_x)
                            flag = 1
                            return_flag = 1
                    except KeyError:
                        pass
                    try:
                        if row_counter == 1 and self.options_dict[(row_x, row_y)]:
                            #print(f'Row Added {column+1} at ({row_x},{row_y})')
                            self.sudoku[row_x][row_y] = column + 1
                            #print(f'Row Deleting ({row_x},{row_y})')
                            options_temp=copy_options_dict[(row_x, row_y)]
                            self.copy_options_dict[(row_x, row_y)] = [i * -1 for i in options_temp]
                            del self.options_dict[(row_x, row_y)]
                            row_count[row_x][column] = column_count[row_y][column] = box_count[row][column] = [0, 0, 0]
                            if self.preassess(function_name=1):
                                self.box_options_builder(row_x, row_y)
                                self.column_options_builder(row_y)
                                self.row_options_builder(row_x)
                            flag = 1
                            return_flag = 1
                    except KeyError:
                        pass

                    try:
                        if column_counter == 1 and self.options_dict[(column_x, column_y)]:
                            #print(f'Column Added {column+1} at ({column_x},{column_y})')
                            self.sudoku[column_x][column_y] = column + 1
                            #print(f'Column Deleting ({column_x},{column_y})')
                            options_temp=copy_options_dict[(column_x, column_y)]
                            self.copy_options_dict[(column_x, column_y)] = [i * -1 for i in options_temp]
                            del self.options_dict[(column_x, column_y)]
                            row_count[column_x][column] = column_count[column_y][column] = box_count[row][column] = [0, 0, 0]
                            if self.preassess(function_name=1):
                                self.box_options_builder(column_x, column_y)
                                self.column_options_builder(column_y)
                                self.row_options_builder(column_x)
                            flag = 1
                            return_flag = 1
                    except KeyError:
                        pass
            del box_count[:]
            del row_count[:]
            del column_count[:]
            #for key in self.options_dict:
                #print(key,self.options_dict[key])
            #print()
        if return_flag==1:
            return True
        return False


#Sudoku('sudoku_wrong_1.txt')
#Sudoku('sudoku_wrong_2.txt')
#Sudoku('sudoku_wrong_3.txt')
#sudoku = Sudoku('sudoku_1.txt')
#sudoku.preasses()
#sudoku = Sudoku('sudoku_2.txt')
#sudoku.preasses()
#sudoku = Sudoku('sudoku_3.txt')
#sudoku.preasses()
#sudoku.bare_tex_output()
#sudoku.forced_tex_output()
#sudoku.marked_tex_output()
#sudoku.worked_tex_output()
print('Sudoku 4')
sudoku = Sudoku('sudoku_4.txt')
#sudoku.preasses()
#sudoku.bare_tex_output()
#sudoku.forced_tex_output()
#sudoku.marked_tex_output()
sudoku.worked_tex_output()

#print('Sudoku 5')
#sudoku = Sudoku('sudoku_5.txt')
#sudoku.preasses()
#sudoku.bare_tex_output()
#sudoku.forced_tex_output()
#sudoku.marked_tex_output()
#sudoku.worked_tex_output()