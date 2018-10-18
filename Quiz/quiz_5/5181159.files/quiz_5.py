from random import randint, seed
'''Randomly fills a grid of size height and width whose values are input by the user, with nonnegative integers 
randomly generated up to an upper bound N also input the user, and computes, for each n≤N, the number of paths 
consisting of all integers from 1 up to n that cannot be extended to n+1.

Outputs the number of such paths, when at least one exists.'''
list1=[]
answer=[]


def display_grid():
    for i in range(len(L)):
        print('   ', ' '.join(str(L[i][j]) for j in range(len(L[0]))))

def get_paths(i,j,answer_list=None):
    if answer_list==None:
        answer_list=[]

    flag=0
    #south
    if i<len(L)-1 and L[i][j]+1==L[i+1][j] and L[i+1][j] > 0:
        flag=1
        val=get_paths(i+1,j)
        answer_list=answer_list+val

    #east
    if j<len(L[0])-1 and L[i][j]+1==L[i][j+1] and L[i][j+1] > 0:
        flag=1
        val=get_paths(i,j+1)
        answer_list=answer_list+val

    #west
    if j and L[i][j]+1==L[i][j-1] and L[i][j-1] > 0:
        flag=1
        val=get_paths(i,j-1)
        answer_list=answer_list+val

    #north
    if L[i][j]+1==L[i-1][j] and L[i-1][j] > 0 and i:
        flag=1
        val=get_paths(i-1,j)
        answer_list=answer_list+val

    if flag==0:
        answer_list.append(L[i][j])          
    return answer_list

answer_set=set()
answer_list=[]
final_list=[]
temp_list=[]

try:
    for_seed, max_length, height, width = [int(i) for i in
                                                  input('Enter four nonnegative integers: ').split()
                                       ]
    if for_seed < 0 or max_length < 0 or height < 0 or width < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
L = [[randint(0, max_length) for _ in range(width)] for _ in range(height)]
print('Here is the grid that has been generated:')
display_grid()

for first in range(len(L)):
    for second in range(len(L[0])):
        if L[first][second] ==1:
            temp_list=get_paths(first,second,answer_list)
            final_list+=temp_list
            del temp_list[:]
count_list=[]

d=set(final_list)
for i in d:
    count_list.append([i,final_list.count(i)])
count_list.sort()

for i in count_list:
    print(f'The number of paths from 1 to {i[0]} is: {i[1]}')
