import sys
from collections import defaultdict

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
        self.build_box()
        self.primary_set=[1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.option_dict=defaultdict(list)
        self.preemptive_dict={}

        try:
            self.sudoku = [[int(character) for character in element] for element in self.lines]
        except ValueError:
            raise SudokuError('Incorrect Input.')

        if len(self.sudoku)<9:
            raise SudokuError('Incorrect Input.')
        for row in self.sudoku:
            if len(row)<9:
                raise SudokuError('Incorrect Input.')

    def preasses(self,function_name=0):
        box_list = [[], [], [], [], [], [], [], [], []]
        column_list = [[], [], [], [], [], [], [], [], []]
        row_list = [[], [], [], [], [], [], [], [], []]
        primary_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for row in range(9):
            for column in range(9):
                if self.sudoku[row][column] in primary_list:
                    box = self.location_to_box[(row, column)]
                    if self.sudoku[row][column] not in box_list[box]:
                        box_list[box].append(self.sudoku[row][column])
                    else:
                        print('There is clearly no solution.')
                        return False
                    if self.sudoku[row][column] not in row_list[row]:
                        row_list[row].append(self.sudoku[row][column])
                    else:
                        print('There is clearly no solution.')
                        return False
                    if self.sudoku[row][column] not in column_list[column]:
                        column_list[column].append(self.sudoku[row][column])
                    else:
                        print('There is clearly no solution.')
                        return False

        self.box_list=box_list
        self.row_list=row_list
        self.column_list=column_list

        if function_name==0:
            print('There might be a solution.')
        if function_name==1 or function_name==0:
            self.init_preemptive_dict()
        return True

    def init_preemptive_dict(self):
        flag = False
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] not in self.primary_set:
                    self.option_dict[(i, j)] = self.primary_set
                    flag = True
        return flag

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
                                for option in self.option_dict[(row, column)]:
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

    def build_box(self):
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

    def box_check(self, x, y):
        for location in self.box_to_location[self.location_to_box[(x, y)]]:
            if self.sudoku[location[0]][location[1]] not in self.primary_set:
                self.option_dict[location] = list(set(self.option_dict[location]) - set(self.box_list[self.location_to_box[location]]))
                if len(self.option_dict[location]) ==1:
                    #print(f'Dictionary Level Added {self.option_dict[location][0]} at ({location[0]},{location[1]})')
                    self.sudoku[location[0]][location[1]]= self.option_dict[location][0]
                    del self.option_dict[location]
                    self.preasses(function_name=2)

    def column_check(self, y):
        for row in range(9):
            if self.sudoku[row][y] not in self.primary_set:
                self.option_dict[(row, y)] = list(set(self.option_dict[(row, y)]) - set(self.column_list[y]))
                if len(self.option_dict[(row, y)]) ==1:
                    #print(f'Dictionary Level Added {self.option_dict[(row, y)][0]} at ({row},{y})')
                    self.sudoku[row][y]= self.option_dict[(row, y)][0]
                    del self.option_dict[(row, y)]
                    self.preasses(function_name=2)

    def row_check(self,x):
        for column in range(9):
            if self.sudoku[x][column] not in self.primary_set:
                self.option_dict[(x, column)] = list(set(self.option_dict[(x, column)]) - set(self.row_list[x]))
                if len(self.option_dict[(x, column)]) ==1:
                    #print(f'Dictionary Level Added {self.option_dict[(x, column)][0]} at ({x},{column})')
                    self.sudoku[x][column]= self.option_dict[(x, column)][0]
                    del self.option_dict[(x, column)]
                    self.preasses(function_name=2)
    def forced(self):
        flag=1
        while flag==1:
            flag = 0
            box_count = []
            row_count = []
            column_count = []

            for i in range(9):
                box_count.append(
                    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
                row_count.append(
                    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
                column_count.append(
                    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])

            for key in self.option_dict:
                for item in self.option_dict[key]:
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
            '''
            for box_nb in range(9):
                for number in range(9):
                    x, y, counter = box_count[box_nb][number]
                    if counter == 1:
                        try:
                            if row_count[x][number][2] == 1 or column_count[y][number][2] == 1 and self.option_dict[(x, y)]:
                                #print(f'Preemptive Level Added {number+1} at ({x},{y})')
                                self.sudoku[x][y] = number + 1
                                del self.option_dict[(x, y)]
                                row_count[x][number] = column_count[y][number] =box_count[box_nb][number] =[0, 0, 0]
                                self.preasses(function_name=2)
                                self.box_check(x, y)
                                self.column_check(y)
                                self.row_check(x)
                                flag=1
                        except KeyError:
                            continue
            '''
            for row in range(9):
                for column in range(9):
                    box_x, box_y, box_counter = box_count[row][column]
                    row_x, row_y, row_counter = row_count[row][column]
                    column_x, column_y, column_counter = column_count[row][column]
                    if box_counter == 1 and self.option_dict[(box_x, box_y)] != []:
                        #print(f'Preemptive Level Added {column+1} at ({box_x},{box_y})')
                        self.sudoku[box_x][box_y] = column + 1
                        del self.option_dict[(box_x, box_y)]
                        row_count[box_x][box_y] = column_count[box_y][column] = box_count[row][column] = [0, 0, 0]
                        self.preasses(function_name=2)
                        self.box_check(box_x, box_y)
                        self.column_check(box_y)
                        self.row_check(box_x)
                        flag = 1
                    elif row_counter == 1 and self.option_dict[(row_x, row_y)]!= []:
                        #print(f'Preemptive Level Added {column+1} at ({row_x},{row_y})')
                        self.sudoku[row_x][row_y] = column + 1
                        del self.option_dict[(row_x, row_y)]
                        row_count[row_x][column] = column_count[row_y][column] = box_count[row][column] = [0, 0, 0]
                        self.preasses(function_name=2)
                        self.box_check(row_x, row_y)
                        self.column_check(row_y)
                        self.row_check(row_x)
                        flag = 1
                    elif column_counter == 1 and self.option_dict[(column_x, column_y)]!= []:
                        #print(f'Preemptive Level Added {column+1} at ({column_x},{column_y})')
                        self.sudoku[column_x][column_y] = column + 1
                        del self.option_dict[(column_x, column_y)]
                        row_count[column_x][column] = column_count[column_y][column] = box_count[row][column] = [0, 0, 0]
                        self.preasses(function_name=2)
                        self.box_check(column_x, column_y)
                        self.column_check(column_y)
                        self.row_check(column_x)
                        flag = 1


    def forced_tex_output(self,function_name=0):
        if self.preasses(function_name=1):
            for row in range(9):
                for column in range(9):
                    self.box_check(row, column)
                    self.column_check(column)
                    self.row_check(row)
            self.forced()
            if function_name==0:
                self.bare_tex_output(function_name=1)

    def marked_tex_output(self,function_name=0):
        self.forced_tex_output(function_name=2)
        if function_name==0:
            #print('Here')
            #for row in self.sudoku:
                #print(row)
           self.bare_tex_output(function_name=2)

    def preemptive_set(self):
        preemptive_dict=dict()
        for key in self.option_dict:
            # box
            for location in self.box_to_location[self.location_to_box[key]]:
                try:
                    if set(self.option_dict[location]).issubset(set(self.option_dict[key])):
                        try:
                            # print('Box')
                            if location not in preemptive_dict[key]:
                                preemptive_dict[key] = preemptive_dict[key] + [location]
                        except KeyError:
                            preemptive_dict[key] = [set(self.option_dict[key])] + [location]
                except KeyError:
                    continue
            # column
            for x in range(9):
                try:
                    if set(self.option_dict[(x, key[1])]).issubset(set(self.option_dict[key])):
                        try:
                            # print('column')
                            if (x, key[1]) not in preemptive_dict[key]:
                                preemptive_dict[key] = preemptive_dict[key] + [(x, key[1])]
                        except KeyError:
                            preemptive_dict[key] = [set(self.option_dict[key])] + [(x, key[1])]
                except KeyError:
                    continue
            # row
            for y in range(9):
                try:
                    if set(self.option_dict[(key[0], y)]).issubset(set(self.option_dict[key])):
                        try:
                            # print('row')
                            if (key[0], y) not in preemptive_dict[key]:
                                preemptive_dict[key] = preemptive_dict[key] + [(key[0], y)]
                        except KeyError:
                            preemptive_dict[key] = [set(option_dict[key])] + [(key[0], y)]
                except KeyError:
                    continue
            if len(preemptive_dict[key]) != len(preemptive_dict[key][0]) + 1:
                del preemptive_dict[key]
        self.preemptive_dict=preemptive_dict

    def worked_tex_output(self):
        self.marked_tex_output(function_name=1)
        self.preemptive_set()


#Sudoku('sudoku_wrong_1.txt')
#Sudoku('sudoku_wrong_2.txt')
#Sudoku('sudoku_wrong_3.txt')
#sudoku = Sudoku('sudoku_1.txt')
#sudoku.preasses()
#sudoku = Sudoku('sudoku_2.txt')
#sudoku.preasses()
sudoku = Sudoku('sudoku_3.txt')
#sudoku.preasses()
#sudoku.bare_tex_output()
#sudoku.forced_tex_output()
sudoku.marked_tex_output()
#sudoku.worked_tex_output()
sudoku = Sudoku('sudoku_4.txt')
#sudoku.preasses()
#sudoku.bare_tex_output()
#sudoku.forced_tex_output()
sudoku.marked_tex_output()
sudoku = Sudoku('sudoku_5.txt')
#sudoku.preasses()
#sudoku.bare_tex_output()
#sudoku.forced_tex_output()
sudoku.marked_tex_output()
