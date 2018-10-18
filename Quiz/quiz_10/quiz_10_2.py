# Written by Eric Martin for COMP9021


'''
A priority queue abstract data type.
'''


class EmptyPriorityQueueError(Exception):
    def __init__(self, message):
        self.message = message


class PriorityQueue():
    min_capacity = 10

    def __init__(self, capacity=min_capacity):
        self.min_capacity = capacity
        self._data = [None] * capacity
        self._length = 0

    def __len__(self):
        '''
        >>> len(PriorityQueue(100))
        0
        '''
        return self._length

    def is_empty(self):
        return self._length == 0

    def insert(self, element):
        '''
        >>> pq = PriorityQueue(4)
        >>> L = [13, 13, 4, 15, 9, 4, 5, 14, 4, 11, 15, 2, 17, 8, 14, 12, 9, 5, 6, 16]
        >>> for e in L: pq.insert(e); print(f'{pq._data[: len(pq) + 1]}    {len(pq._data)}')
        [None, 13]    4
        [None, 13, 13]    4
        [None, 13, 13, 4]    4
        [None, 15, 13, 4, 13]    8
        [None, 15, 13, 4, 13, 9]    8
        [None, 15, 13, 4, 13, 9, 4]    8
        [None, 15, 13, 5, 13, 9, 4, 4]    8
        [None, 15, 14, 5, 13, 9, 4, 4, 13]    16
        [None, 15, 14, 5, 13, 9, 4, 4, 13, 4]    16
        [None, 15, 14, 5, 13, 11, 4, 4, 13, 4, 9]    16
        [None, 15, 15, 5, 13, 14, 4, 4, 13, 4, 9, 11]    16
        [None, 15, 15, 5, 13, 14, 4, 4, 13, 4, 9, 11, 2]    16
        [None, 17, 15, 15, 13, 14, 5, 4, 13, 4, 9, 11, 2, 4]    16
        [None, 17, 15, 15, 13, 14, 5, 8, 13, 4, 9, 11, 2, 4, 4]    16
        [None, 17, 15, 15, 13, 14, 5, 14, 13, 4, 9, 11, 2, 4, 4, 8]    16
        [None, 17, 15, 15, 13, 14, 5, 14, 13, 4, 9, 11, 2, 4, 4, 8, 12]    32
        [None, 17, 15, 15, 13, 14, 5, 14, 13, 4, 9, 11, 2, 4, 4, 8, 12, 9]    32
        [None, 17, 15, 15, 13, 14, 5, 14, 13, 5, 9, 11, 2, 4, 4, 8, 12, 9, 4]    32
        [None, 17, 15, 15, 13, 14, 5, 14, 13, 6, 9, 11, 2, 4, 4, 8, 12, 9, 4, 5]    32
        [None, 17, 16, 15, 13, 15, 5, 14, 13, 6, 14, 11, 2, 4, 4, 8, 12, 9, 4, 5, 9]    32
        '''
        if self._length + 1 == len(self._data):
            self._resize(2 * len(self._data))
        self._length += 1
        self._data[self._length] = element
        self._bubble_up(self._length)

    def delete(self):
        '''
        >>> pq = PriorityQueue(4)
        >>> L = [13, 13, 4, 15, 9, 4, 5, 14, 4, 11, 15, 2, 17, 8, 14, 12, 9, 5, 6, 16]
        >>> for e in L: pq.insert(e)
        >>> for _ in range(len(L)):
        ...     print(f'{pq.delete():2d} {pq._data[: len(pq) + 1]}    {len(pq._data)}')
        17 [None, 16, 15, 15, 13, 14, 5, 14, 13, 6, 9, 11, 2, 4, 4, 8, 12, 9, 4, 5]    32
        16 [None, 15, 14, 15, 13, 11, 5, 14, 13, 6, 9, 5, 2, 4, 4, 8, 12, 9, 4]    32
        15 [None, 15, 14, 14, 13, 11, 5, 8, 13, 6, 9, 5, 2, 4, 4, 4, 12, 9]    32
        15 [None, 14, 13, 14, 13, 11, 5, 8, 12, 6, 9, 5, 2, 4, 4, 4, 9]    32
        14 [None, 14, 13, 9, 13, 11, 5, 8, 12, 6, 9, 5, 2, 4, 4, 4]    32
        14 [None, 13, 13, 9, 12, 11, 5, 8, 4, 6, 9, 5, 2, 4, 4]    32
        13 [None, 13, 12, 9, 6, 11, 5, 8, 4, 4, 9, 5, 2, 4]    32
        13 [None, 12, 11, 9, 6, 9, 5, 8, 4, 4, 4, 5, 2]    32
        12 [None, 11, 9, 9, 6, 5, 5, 8, 4, 4, 4, 2]    32
        11 [None, 9, 6, 9, 4, 5, 5, 8, 2, 4, 4]    32
         9 [None, 9, 6, 8, 4, 5, 5, 4, 2, 4]    32
         9 [None, 8, 6, 5, 4, 5, 4, 4, 2]    16
         8 [None, 6, 5, 5, 4, 2, 4, 4]    16
         6 [None, 5, 4, 5, 4, 2, 4]    16
         5 [None, 5, 4, 4, 4, 2]    16
         5 [None, 4, 4, 4, 2]    8
         4 [None, 4, 2, 4]    8
         4 [None, 4, 2]    4
         4 [None, 2]    4
         2 [None]    4
        >>> pq.delete()
        Traceback (most recent call last):
        ...
        EmptyPriorityQueueError: Cannot delete element from empty priority queue
        '''
        if self.is_empty():
            raise EmptyPriorityQueueError('Cannot delete element from empty priority queue')
        max_element = self._data[1]
        self._data[1], self._data[self._length] = self._data[self._length], self._data[1]
        self._length -= 1
        # When the priority queue is one quarter full, we reduce its size to make it half full,
        # provided that it would not reduce its capacity to less than the minimum required.
        if self.min_capacity // 2 <= self._length <= len(self._data) // 4:
            self._resize(len(self._data) // 2)
        self._bubble_down(1)
        return max_element

    def _bubble_up(self, i):
        if i > 1 and self._data[i] > self._data[i // 2]:
            self._data[i // 2], self._data[i] = self._data[i], self._data[i // 2]
            self._bubble_up(i // 2)

    def _bubble_down(self, i):
        child = 2 * i
        if child < self._length and self._data[child + 1] > self._data[child]:
            child += 1
        if child <= self._length and self._data[i] < self._data[child]:
            self._data[child], self._data[i] = self._data[i], self._data[child]
            self._bubble_down(child)

    def _resize(self, new_size):
        self._data = list(self._data[: self._length + 1]) + [None] * (new_size - self._length - 1)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

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

# Possibly define some functions
new_list = []


def preferred_sequence(working_list=[]):
    if len(working_list) - 1 == 1:
        new_list.append(working_list[1])
        return new_list

    sorted_list = sorted(working_list[1:len(pq) + 1], reverse=True)
    sorted_counter = 0
    travelled_through = []
    curr_loc = len(working_list) - 1
    travelled_through.append(curr_loc)

    while True:

        looking_for = working_list.index(sorted_list[sorted_counter])
        flag = 0

        if curr_loc % 2 == 1:
            if working_list[curr_loc] > working_list[curr_loc - 1]:
                curr_loc = curr_loc // 2
                flag = 1
        else:
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
            for index in range(len(travelled_through) - 1, 0, -1):
                working_list[travelled_through[index]] = working_list[travelled_through[index - 1]]
            del working_list[-1]
            preferred_sequence(working_list)
            return new_list

    return new_list

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
if len(pq._data) >0:
    print('The heap that has been generated is: ')
    print(pq._data[1 : len(pq) + 1])

    preferred_sequence(pq._data[:len(pq)+1])
print(list(reversed(new_list)))
#print('The preferred ordering of data to generate this heap by successsive insertion is:')
#print(preferred_sequence())

