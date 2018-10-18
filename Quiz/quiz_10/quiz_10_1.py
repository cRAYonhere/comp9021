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
new_list=[]
def preferred_sequence(working_list=[]):
    '''
    This is the first implementation, it can be reduced greatly from this point onwards
    P.S Don't share the code with anyone, just be mindful of plagiarism. Good Luck !
    '''
    #input()
    #print('Working List:',working_list)
    #Everytime I get a pq I sort it
    sorted_list=sorted(working_list[1:len(pq)+1], reverse=True)
    #print('Sorted List:',sorted_list)
    #index postion in sorted list
    sorted_counter=0
    #A list to store the location of places I have vistited
    travelled_through=[]
    #where I start
    curr_loc = len(working_list)-1
    #first location I visited
    travelled_through.append(curr_loc)
    while True:

        #index position of the element I am looking for
        looking_for=working_list.index(sorted_list[sorted_counter])
        #print('Looking For: ', looking_for)
        #print('Current Loc: ', curr_loc)
        #If even, else odd
        if curr_loc % 2 == 1:
            if working_list[curr_loc] > working_list[curr_loc-1]:
                curr_loc=curr_loc//2
                travelled_through.append(curr_loc)
            else:
                #print(f'Failed {working_list[curr_loc]} !> {working_list[curr_loc-1]}')
                sorted_counter+=1
                del travelled_through[:]
                curr_loc = len(working_list)-1
                travelled_through.append(curr_loc)
        elif curr_loc % 2 ==0:
            if len(working_list)-1== curr_loc:
                curr_loc=curr_loc//2
                travelled_through.append(curr_loc)
            elif working_list[curr_loc] > working_list[curr_loc+1]:
                curr_loc=curr_loc//2
                travelled_through.append(curr_loc)
            else:
                sorted_counter+=1
                del travelled_through[:]
                curr_loc = len(working_list)-1
                travelled_through.append(curr_loc)
        if curr_loc == looking_for:
            break

    if curr_loc == looking_for:
        new_list.append(working_list[curr_loc])
        print('New List Reg:',new_list)
        #print('Travelled Through:', travelled_through)
        #Shifting the elements and deleting the last element
        for index in range(len(travelled_through)-1,0,-1):
            working_list[travelled_through[index]]=working_list[travelled_through[index-1]]
        del working_list[-1]
        print(working_list)
        #If working has only 1 element
        if len(working_list)-1==1:
            new_list.append(working_list[1])
            return
        preferred_sequence(working_list)


    #Replace pass above with your code (altogether, aim for around 24 lines of code)

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
print(pq._data[1 : len(pq) + 1])
from datetime import datetime
startTime = datetime.now()

preferred_sequence(pq._data[:len(pq)+1])

print(datetime.now() - startTime)
input()
#print(list(reversed(new_list)))
#print('The preferred ordering of data to generate this heap by successsive insertion is:')
#print(preferred_sequence())

