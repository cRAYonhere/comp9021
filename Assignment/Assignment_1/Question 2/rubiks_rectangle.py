from collections import deque

# Insert your code here
from copy import deepcopy
import sys 
from collections import defaultdict
import re

def f1(ops_list):
    #print('f1')
    ops_list[0].reverse() 
    ops_list[1]+=1
    return ops_list

def f2(ops_list):
    #print('f2')
    temp=ops_list[0].pop(3)
    ops_list[0].insert(0,temp)
    temp=ops_list[0].pop(4)
    ops_list[0].insert(7,temp)
    ops_list[1]+=1

    return ops_list

def f3(ops_list):
    #print('f3')
    temp1=ops_list[0][1]
    temp2=ops_list[0][2]
    temp5=ops_list[0][5]
    temp6=ops_list[0][6]
    ops_list[0][6]=temp5
    ops_list[0][2]=temp1
    ops_list[0][1]=temp6
    ops_list[0][5]=temp2
    ops_list[1]+=1
    
    return ops_list
def f():
    d = deque()
    seen_before_list = defaultdict(list)
    new_list= []
    start_list=[[1, 2, 3, 4, 5, 6, 7, 8],0]
    
    #user_list=[1, 2, 3, 4, 5, 6, 7, 8] #0 steps-0.0 seconds
    #user_list=[2, 6, 8, 4, 5, 7, 3, 1] #7 steps-0.01200723648071289 seconds
    #user_list=[7, 2, 1, 5, 4, 3, 6, 8] #16 steps-0.8640754222869873 seconds
    #user_list=[1, 5, 3, 2, 4, 6, 7, 8]  #18 Steps-1.9593160152435303 seconds
    #user_list=[2, 8, 1, 3, 6, 5, 7, 4] #18 Steps-2.1534345149993896 seconds
    
    letters_string = input('Input final configuration: ')
    letters_string=letters_string.replace(" ","")
    user_list=[]
    if not re.match("^[1-8]{8}$", letters_string):
        print('Incorrect configuration, giving up...')
        sys.exit()
    for i in letters_string:
        user_list.append(int(i))
    depth=0
    seen_before_list[tuple(start_list[0])].append(list(start_list[0]))
    d.append(deepcopy(start_list))
    checkmate=0
    
    if user_list == start_list[0]:
        print('0 step is needed to reach the final configuration.')
           
    else:
        while checkmate ==0:

            current_list=list(d.popleft())

            new_list=f1(deepcopy(current_list))
            if user_list == new_list[0]:
                if new_list[1] <=1:
                    print(str(new_list[1])+' step is needed to reach the final configuration.')
                else:
                    print(str(new_list[1])+' steps are needed to reach the final configuration.')
                checkmate=1
                break
            if tuple(new_list[0]) not in seen_before_list:
                seen_before_list[tuple(new_list[0])].append(list(new_list[0]))
                d.append(list(new_list))

            new_list=f2(deepcopy(current_list))
            if user_list == new_list[0]:
                if new_list[1] <=1:
                    print(str(new_list[1])+' step is needed to reach the final configuration.')
                else:
                    print(str(new_list[1])+' steps are needed to reach the final configuration.')
                checkmate=1
                break

            if tuple(new_list[0]) not in seen_before_list:
                seen_before_list[tuple(new_list[0])].append(list(new_list[0]))
                d.append(list(new_list))
            new_list=f3(deepcopy(current_list))
            if user_list == new_list[0]:
                if new_list[1] <=1:
                    print(str(new_list[1])+' step is needed to reach the final configuration.')
                else:
                    print(str(new_list[1])+' steps are needed to reach the final configuration.')
                checkmate=1
                break

            if tuple(new_list[0]) not in seen_before_list:
                seen_before_list[tuple(new_list[0])].append(list(new_list[0]))
                d.append(list(new_list))

f()



