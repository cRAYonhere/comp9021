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
        self.filename = str(args)
        self.lines = lines
        self.build_box_dictionary()
        self.primary_set = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.options_dict = {}
        self.preemptive_dict = {}
        self.copy_options_dict = dict()

        try:
            self.sudoku = [[int(character) for character in element] for element in self.lines]
        except ValueError:
            raise SudokuError('Incorrect input')

        if len(self.sudoku) < 9:
            raise SudokuError('Incorrect input')
        for row in self.sudoku:
            if len(row) < 9:
                raise SudokuError('Incorrect input')
        self.init_options_dict()

    def preassess(self, function_name=0):
        box_list = [[], [], [], [], [], [], [], [], []]
        column_list = [[], [], [], [], [], [], [], [], []]
        row_list = [[], [], [], [], [], [], [], [], []]
        primary_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        frequency = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0]]
        for row in range(9):
            for column in range(9):
                if self.sudoku[row][column] != 0:
                    frequency[self.sudoku[row][column] - 1][1] += 1
                # print(frequency)
                if self.sudoku[row][column] in primary_list:
                    box = self.location_to_box[(row, column)]
                    if self.sudoku[row][column] not in box_list[box]:
                        box_list[box].append(self.sudoku[row][column])
                    else:
                        print('There is clearly no solution.')
                        for row in self.sudoku:
                            print(row)
                        return False
                    if self.sudoku[row][column] not in row_list[row]:
                        row_list[row].append(self.sudoku[row][column])
                    else:
                        print('There is clearly no solution.')
                        for row in self.sudoku:
                            print(row)
                        return False
                    if self.sudoku[row][column] not in column_list[column]:
                        column_list[column].append(self.sudoku[row][column])
                    else:
                        print('There is clearly no solution.')
                        for row in self.sudoku:
                            print(row)
                        return False

        self.box_list = box_list
        self.row_list = row_list
        self.column_list = column_list
        if function_name == 0:
            print('There might be a solution.')
            for row in self.sudoku:
                print(row)
        if function_name == 1:
            self.frequency = frequency
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
            self.box_to_location = box_to_location
            self.location_to_box = location_to_box

    def bare_tex_output(self, function_name=0):
        if self.preassess(function_name=2):
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

            footer = r'''
\end{tabular}
\end{center}

\end{document}
'''
            function_name_dict = {0: '_bare.tex', 1: '_forced.tex', 2: '_marked.tex', 3: '_worked.tex'}
            element_dict = {1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [1, 1], 5: [2, 0], 6: [2, 1], 7: [3, 0], 8: [3, 1],
                            9: [3, 2]}
            printing = [[[['\cancel' for _ in range(3)] for _ in range(5)] for _ in range(9)] for _ in range(9)]

            filename = str(self.filename)[0:-4] + function_name_dict[function_name]

            if function_name == 3:
                for key, value in self.copy_options_dict.items():
                    value.sort()
                    for element in value:
                        printing[key[0]][key[1]][element_dict[element][0]][
                            element_dict[element][1]] += f'{{{str(element)}}}'

            if function_name == 2 or function_name == 3:
                for key, value in self.options_dict.items():
                    value.sort()
                    for element in value:
                        printing[key[0]][key[1]][element_dict[element][0]][element_dict[element][1]] = element

            with open(filename, 'a') as fstream:
                fstream.write(header)
                for line in range(9):
                    string = ''
                    if line > 0:
                        string += '\n'
                    string += '\n% Line ' + str(line + 1) + '\n'
                    for box in range(9):
                        if box > 0 and box % 3 != 0:
                            string += ' & '
                        elif box > 0:
                            string += ' &\n'
                        string += '\\N'
                        if self.sudoku[line][box] is not 0:
                            printing[line][box][4][0] = self.sudoku[line][box]
                        for element in range(5):
                            place_holder = ''
                            for ele in range(len(printing[line][box][element])):
                                if printing[line][box][element][ele] != '\cancel':
                                    if place_holder:
                                        place_holder = place_holder + ' ' + str(printing[line][box][element][ele])
                                    else:
                                        place_holder = str(printing[line][box][element][ele])
                            string += str(f'{{{place_holder}}}')
                    string += ' \\\ \hline'
                    if line % 3 == 2:
                        string += '\hline'
                    fstream.write(string)
                fstream.write(footer)

    def box_options_builder(self, x, y, ):
        for location in self.box_to_location[self.location_to_box[(x, y)]]:
            if self.sudoku[location[0]][location[1]] not in self.primary_set:
                temp_list = list(set(self.options_dict[location]) - set(self.box_list[self.location_to_box[location]]))
                if len(temp_list) == 1:
                    # print(f'Options Dict Added {temp_list[0]} at location ({location[0]},{location[1]})')
                    self.sudoku[location[0]][location[1]] = temp_list[0]
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
                temp_list = list(set(self.options_dict[(row, y)]) - set(self.column_list[y]))
                if len(temp_list) == 1:
                    # print(f'Options Dict Added {temp_list[0]} at location ({row},{y})')
                    self.sudoku[row][y] = temp_list[0]
                    del self.options_dict[(row, y)]
                    if self.preassess(function_name=1):
                        self.box_options_builder(row, y)
                        self.row_options_builder(row)
                        self.column_options_builder(y)
                else:
                    self.options_dict[(row, y)] = temp_list

    def row_options_builder(self, x):
        for column in range(9):
            if self.sudoku[x][column] not in self.primary_set:
                temp_list = list(set(self.options_dict[(x, column)]) - set(self.row_list[x]))
                if len(temp_list) == 1:
                    # print(f'Options Dict Added {temp_list[0]} at location ({x},{column})')
                    self.sudoku[x][column] = temp_list[0]
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
                self.box_options_builder(row, column)
                self.row_options_builder(row)
                self.column_options_builder(column)

    def forced_tex_output(self, function_name=0):
        if self.preassess(function_name=1):
            if function_name == 0:
                self.build_all_options()
            if function_name == 1:
                self.build_all_options()
            self.frequency.sort(key=lambda x: x[1], reverse=True)
            # print('Frequency:',self.frequency)
            worked_flag = 0

            flag = 1
            while flag == 1:
                flag = 0
                # print('length of options_dict: ', len(self.options_dict))
                for element in range(9):
                    # print(self.frequency[element][0])
                    if self.frequency[element][1] > 1:
                        for box in range(9):
                            counter = 0
                            for location in self.box_to_location[box]:
                                try:
                                    if self.frequency[element][0] in self.options_dict[location]:
                                        counter += 1
                                        final_location = location
                                except KeyError:
                                     continue
                            if counter == 1:
                                # print(f'Added {self.frequency[element][0]} at location ({final_location[0]},{final_location[1]})')
                                self.sudoku[final_location[0]][final_location[1]] = self.frequency[element][0]
                                del self.options_dict[final_location]
                                if self.preassess(function_name=1):
                                    self.box_options_builder(final_location[0], final_location[1])
                                    self.row_options_builder(final_location[0])
                                    self.column_options_builder(final_location[1])
                                flag = 1
                                worked_flag = 1
            if function_name != 0:
                if worked_flag == 1:
                    return True
                return False

            if function_name == 0:
                self.bare_tex_output(function_name=1)

    def preemptive_set_builder(self, function_name=0):
        preemptive_dict = dict()
        for key in self.options_dict:
            for location in self.box_to_location[self.location_to_box[key]]:
                try:
                    if set(self.options_dict[location]).issubset(set(self.options_dict[key])):
                        try:
                            preemptive_dict[(key[0], key[1], 'b')] = preemptive_dict[(key[0], key[1], 'b')] + [location]
                        except KeyError:
                            preemptive_dict[(key[0], key[1], 'b')] = [set(self.options_dict[key])] + [location]
                except KeyError:
                    pass
            try:
                if len(preemptive_dict[(key[0], key[1], 'b')][0]) != len(preemptive_dict[(key[0], key[1], 'b')]) - 1:
                    del preemptive_dict[(key[0], key[1], 'b')]
            except KeyError:
                pass

            # column
            for x in range(9):
                try:
                    if set(self.options_dict[(x, key[1])]).issubset(set(self.options_dict[key])):
                        try:
                            # print('column')
                            preemptive_dict[(key[0], key[1], 'c')] = preemptive_dict[(key[0], key[1], 'c')] + [
                                (x, key[1])]
                        except KeyError:
                            preemptive_dict[(key[0], key[1], 'c')] = [set(self.options_dict[key])] + [(x, key[1])]
                except KeyError:
                    pass
            try:
                if len(preemptive_dict[(key[0], key[1], 'c')][0]) != len(preemptive_dict[(key[0], key[1], 'c')]) - 1:
                    del preemptive_dict[(key[0], key[1], 'c')]
            except KeyError:
                pass

            # row
            for y in range(9):
                try:
                    if set(self.options_dict[(key[0], y)]).issubset(set(self.options_dict[key])):
                        try:
                            # print('row')
                            preemptive_dict[(key[0], key[1], 'r')] = preemptive_dict[(key[0], key[1], 'r')] + [
                                (key[0], y)]
                        except KeyError:
                            preemptive_dict[(key[0], key[1], 'r')] = [set(self.options_dict[key])] + [(key[0], y)]
                except KeyError:
                    pass
            try:
                if len(preemptive_dict[(key[0], key[1], 'r')][0]) != len(preemptive_dict[(key[0], key[1], 'r')]) - 1:
                    del preemptive_dict[(key[0], key[1], 'r')]
            except KeyError:
                pass

        self.preemptive_dict = preemptive_dict

    def marked_tex_output(self):
        if self.preassess(function_name=2):
            self.forced_tex_output(function_name=1)
            self.bare_tex_output(function_name=2)

    def worked_tex_output(self, function_name=0):
        if self.preassess(function_name=2):
            self.forced_tex_output(function_name=1)

            self.copy_options_dict = deepcopy(self.options_dict)
            flag = 1
            while flag == 1:
                flag = 0
                self.preemptive_set_builder()
                for key in self.preemptive_dict:
                    # print('Working on: ',key,self.preemptive_dict[key])
                    if key[2] == 'b':
                        for location in self.box_to_location[self.location_to_box[(key[0], key[1])]]:
                            if self.sudoku[location[0]][location[1]] not in self.primary_set and \
                                            location not in self.preemptive_dict[key][1:len(self.preemptive_dict[key])]:
                                for element in self.preemptive_dict[key][0]:
                                    if element in self.options_dict[location]:
                                        del self.options_dict[location][self.options_dict[location].index(element)]
                    elif key[2] == 'r':
                        for column in range(9):
                            if self.sudoku[key[0]][column] not in self.primary_set and (key[0], column) not in \
                                    self.preemptive_dict[key][1:len(self.preemptive_dict[key])]:
                                for set_element in self.preemptive_dict[key][0]:
                                    if set_element in self.options_dict[(key[0], column)]:
                                        del self.options_dict[(key[0], column)][
                                            self.options_dict[(key[0], column)].index(set_element)]
                                        # print(f'New option:({key[0]},{column})', self.options_dict[(key[0], column)])
                    elif key[2] == 'c':
                        for row in range(9):
                            if self.sudoku[row][key[1]] not in self.primary_set and (row, key[1]) not in \
                                    self.preemptive_dict[key][1:len(self.preemptive_dict[key])]:
                                for set_element in self.preemptive_dict[key][0]:
                                    if set_element in self.options_dict[(row, key[1])]:
                                        del self.options_dict[(row, key[1])][
                                            self.options_dict[(row, key[1])].index(set_element)]
                                        # print(f'New option:({row},{key[1]})', self.options_dict[(row,key[1])])
                    if self.update_sudoku():
                        flag = 1
            self.bare_tex_output(function_name=3)

    def update_sudoku(self):
        flag = 0
        delete_keys = []
        for key in self.options_dict:
            if len(self.options_dict[key]) == 1:
                # print(f'Adding {self.options_dict[key][0]} at location ({key[0]},{key[1]})')
                self.sudoku[key[0]][key[1]] = self.options_dict[key][0]
                # for row in self.sudoku:
                # print(row)
                delete_keys.append(key)

        for key in delete_keys:
            # print(f'Deleting {key}')
            del self.options_dict[key]
            flag_build_options = 1

        if self.preassess(function_name=1):
            for key in delete_keys:
                self.box_options_builder(key[0], key[1])
                self.row_options_builder(key[0])
                self.column_options_builder(key[1])
            flag = 1
        else:
            # print('Preasses Failed.')
            sys.exit()
        box_count = []
        row_count = []
        column_count = []
        return_flag = 0
        flag = 1
        while flag == 1:
            flag = 0

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
                    column_count[key[1]][item - 1][0], column_count[key[1]][item - 1][1] = key
                    column_count[key[1]][item - 1][2] += 1
                    # row
                    row_count[key[0]][item - 1][0], row_count[key[0]][item - 1][1] = key
                    row_count[key[0]][item - 1][2] += 1
                    # box
                    box_count[self.location_to_box[key]][item - 1][0], box_count[self.location_to_box[key]][item - 1][
                        1] = key
                    box_count[self.location_to_box[key]][item - 1][2] += 1

            for row in range(9):
                for column in range(9):
                    box_x, box_y, box_counter = box_count[row][column]
                    row_x, row_y, row_counter = row_count[row][column]
                    column_x, column_y, column_counter = column_count[row][column]
                    try:
                        if box_counter == 1 and self.options_dict[(box_x, box_y)]:
                            # print(f'Box Added {column+1} at ({box_x},{box_y})')
                            self.sudoku[box_x][box_y] = column + 1
                            # print(f'Box Deleting ({box_x},{box_y})')
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
                            # print(f'Row Added {column+1} at ({row_x},{row_y})')
                            self.sudoku[row_x][row_y] = column + 1
                            # print(f'Row Deleting ({row_x},{row_y})')
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
                            # print(f'Column Added {column+1} at ({column_x},{column_y})')
                            self.sudoku[column_x][column_y] = column + 1
                            # print(f'Column Deleting ({column_x},{column_y})')
                            del self.options_dict[(column_x, column_y)]
                            row_count[column_x][column] = column_count[column_y][column] = box_count[row][column] = [0,
                                                                                                                     0,
                                                                                                                     0]

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
        if return_flag == 1:
            return True
        return False