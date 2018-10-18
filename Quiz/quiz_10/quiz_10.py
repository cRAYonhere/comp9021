# Randomly generates N distinct integers with N provided by the user,
# inserts all these elements into a priority queue, and outputs a list
# L consisting of all those N integers, determined in such a way that:
# - inserting the members of L from those of smallest index of those of
#   largest index results in the same priority queue;
# - L is preferred in the sense that the last element inserted is as large as
#   possible, and then the penultimate element inserted is as large as possible, etc.
#
# Written by *** and Eric Martin for COMP9021



import sys
from random import seed, sample

from priority_queue_adt import *


# Possibly define some functions
def preferred_sequence(working_list = [], new_list = [], sorted_list=[]):

    if len(working_list) - 1 == 1:
        new_list.append(working_list[1])
        return new_list

    sorted_counter = 0
    travelled_through = []
    curr_loc = len(working_list) - 1
    travelled_through.append(curr_loc)

    while True:

        looking_for = working_list.index(sorted_list[sorted_counter])
        flag = 0

        if curr_loc % 2 == 1 and curr_loc > looking_for:
            if working_list[curr_loc] > working_list[curr_loc - 1]:
                curr_loc = curr_loc // 2
                flag = 1
        elif curr_loc > looking_for:
            if len(working_list) - 1 == curr_loc or working_list[curr_loc] > working_list[curr_loc + 1]:
                curr_loc = curr_loc // 2
                flag = 1

        if flag == 0:
            sorted_counter += 1
            del travelled_through[:]
            curr_loc = len(working_list) - 1
        travelled_through.append(curr_loc)

        if curr_loc == looking_for:
            new_list.append(working_list[curr_loc])
            del sorted_list[sorted_list.index(working_list[curr_loc])]
            for index in range(len(travelled_through) - 1, 0, -1):
                working_list[travelled_through[index]] = working_list[travelled_through[index - 1]]
            working_list.pop()
            return preferred_sequence(working_list,new_list,sorted_list)
    # Replace pass above with your code (altogether, aim for around 24 lines of code)


try:
    for_seed, length = [int(x) for x in input('Enter 2 nonnegative integers, the second one '
                                                                             'no greater than 100: '
                                             ).split()
                       ]
    if for_seed < 0 or length > 100:
        raise ValueError
except ValueError:
    print('Incorrect input (not all integers), giving up.')
    sys.exit()
seed(for_seed)
L = sample(list(range(length * 10)), length)
pq = PriorityQueue()
for e in L:
    pq.insert(e)
print('The heap that has been generated is: ')
print(pq._data[ : len(pq) + 1])
print('The preferred ordering of data to generate this heap by successsive insertion is:')
if len(pq._data[ : len(pq) + 1])>1:
    from datetime import datetime
    startTime = datetime.now()
    temp=preferred_sequence(pq._data[:len(pq) + 1], sorted_list=sorted(pq._data[1:len(pq) + 1], reverse=True))
    print(datetime.now() - startTime)

    print(print(list(reversed(temp))))
else:
    print(pq._data[ : len(pq) + 1])
