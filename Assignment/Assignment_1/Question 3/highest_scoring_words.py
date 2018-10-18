# Insert your code here
import re
import sys
from collections import Counter 
from bisect import insort_left

def issubset(X, Y):
    '''
    checks if x is a subset of y
    '''
    return all(v <= Y[k] for k, v in X.items())

def f():
    list1=[]   
    list2=[]
    final_list=[]
    value_dict={'a': 2,'b': 5, 'c': 4, 'd': 4, 'e': 1,'f': 6,'g': 5,'h': 5,'i': 1,'j': 7,'k': 6,'l': 3,'m': 5,'n': 2,'o': 3,'p': 5,'q': 7,'r': 2,'s': 1,'t': 2,'u': 4,'v': 6,'w': 6,'x': 7,'y': 5,'z' :7}

    letters_string = input('Enter between 3 and 10 lowercase letters: ')
    letters_string=letters_string.replace(" ","")
    if not re.match("^[a-z]{3,10}$", letters_string):
        print('Incorrect input, giving up...')
        sys.exit()
    main_string=Counter(letters_string)
    newDict = {}
    with open('wordsEn.txt', 'r') as f:
        for line in f:
            newDict[line.rstrip()]=line.rstrip()
    set2=set()
    large=0
    for key, value in newDict.items():
        temp=Counter(key)
        val=0
        if issubset(temp, main_string):
            for i in value:
                val=val+value_dict[i]
            if val > large:
                large=val
            insort_left(list2, (val,value), lo=0, hi=len(list2))
    for j in list2:
        if j[0]==large:
            final_list.append(j[1])
    if final_list:
        print('The highest score is '+str(large)+'.')
        if len(final_list) == 1:
            print('The highest scoring word is',final_list[0])
        else:
            print('The highest scoring words are, in alphabetical order:')
            for j in final_list:
                    print('   ',j)
    else:
        print('No word is built from some of those letters.')

f()

