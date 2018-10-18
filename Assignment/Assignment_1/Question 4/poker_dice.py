from random import seed,randint
from itertools import groupby
import sys
import doctest
import time

def simulate(size):
    
    dice_list=[]
    ofakind_list=[]
    randint_list=[]
    dice_set=set()
    
    counter_5=counter_4=counter_3=counter_2=counter_1=counter_straight=counter_full_house=counter_times=counter_bust=0

    straight_set10={0,1,2,3,4}
    straight_set9={1,2,3,4,5}
    start_time = time.time()
    while counter_times <size:          
        
        del dice_list[:]
        del randint_list[:]
        dice_set.clear()
        
        dice_list=[randint(0,5) for i in range(5)]
            
        dice_set=set(dice_list)
        dice_set_len=len(dice_set)
        
        if dice_set_len == 1:
            counter_5+=1
        elif straight_set10 == (straight_set10 & dice_set) or straight_set9 == (straight_set9 & dice_set):
            counter_straight+=1
        elif dice_set_len==2:
            for i in dice_set:
                ofakind_list.append(dice_list.count(i))
            if max(ofakind_list) == 4:
                counter_4+=1
            else:
                counter_full_house+=1
            del ofakind_list[:]
        elif dice_set_len ==3:
            for i in dice_set:
                ofakind_list.append(dice_list.count(i)) 
            if max(ofakind_list)==3:
                counter_3+=1
            else:
                counter_2+=1
            del ofakind_list[:]
        elif dice_set_len !=5:
            counter_1+=1

        counter_times+=1
        
    
    multiplier=100/size

    print("Five of a kind : " + str(f'{round(counter_5*multiplier,2):.2f}'+'%'))
    print("Four of a kind : " + str(f'{round(counter_4*multiplier,2):.2f}'+'%'))
    print("Full house     : " + str(f'{round(counter_full_house*multiplier,2):.2f}'+'%'))
    print("Straight       : " + str(f'{round(counter_straight*multiplier,2):.2f}'+'%'))
    print("Three of a kind: " + str(f'{round(counter_3*multiplier,2):.2f}'+'%'))
    print("Two pair       : " + str(f'{round(counter_2*multiplier,2):.2f}'+'%'))
    print("One pair       : " + str(f'{round(counter_1*multiplier,2):.2f}'+'%'))

def play():
    dice_set=set()
    dice_list=[]
    ops_list=[]
    ofakind_list=[]
    answer_list=[]
    randint_list=[]
    random_dict={5: '9', 4: '10', 3:'Jack', 2:'Queen',1:'King',0:'Ace'}
    char_dict={'Jack':11,'Queen':12,'King':13,'Ace':14, '10':10,'9':9}
    number_dict={'Jack':3,'Queen':2,'King':1,'Ace':0, '10':4,'9':5}
    dict_roll={2:'second',3:'third'}
    straight_set10={0,1,2,3,4}
    straight_set9={1,2,3,4,5}
    roll=1
    flag=0
    hold=0
    while roll <=3:

        del ops_list[:] 
        del ofakind_list[:]
        del randint_list[:]
        
        dice_set.clear()
        #print(dice_list)
        for i in range(5-hold):
            dice_list.append(randint(0,5))
        
        dice_list.sort()
        
        print(f'The roll is: {random_dict[dice_list[0]]} {random_dict[dice_list[1]]} {random_dict[dice_list[2]]} {random_dict[dice_list[3]]} {random_dict[dice_list[4]]}')
        
        dice_set=set(dice_list)
        dice_set_len=len(dice_set)
        
        
        #print('Dice List:',dice_list)
        #Five of a Kind
        if dice_set_len == 1:
            print('It is a Five of a kind.')
        #Straight
        elif straight_set10 == (straight_set10 & dice_set) or straight_set9 == (straight_set9 & dice_set):
            print('It is a Straight')
        elif dice_set_len==2:
            for i in dice_set:
                ofakind_list.append(dice_list.count(i))
            #Four of a Kind
            if max(ofakind_list) == 4:
                print('It is a Four of a kind')
            else:
            #Full House
                print('It is a Full house') 
        elif dice_set_len ==3:
            for i in dice_set:
                ofakind_list.append(dice_list.count(i))
            #print('Dice set:',dice_set)
            #print('Dice List:',dice_list)
            #print('ofakind_list:',ofakind_list)
            #Three of a Kind
            if max(ofakind_list)==3:
                print('It is a Three of a kind')
            #Two Pair
            else:
                print('It is a Two pair')
        #One Pair
        elif dice_set_len !=5:
            print('It is a One pair')
        #Bust
        elif dice_set_len == 5:
            print('It is a Bust')
            
        for i in range(len(dice_list)):
            dice_list[i]=random_dict[dice_list[i]]

        roll+=1
        while roll<=3:
            del answer_list[:] 
            answer_list=input(f'Which dice do you want to keep for the {dict_roll[roll]} roll? ').split()
            if not answer_list:
                flag=1
                del dice_list[:] 
                break
            elif answer_list[0] == 'All' or answer_list[0]=='all':
                print('Ok, done.')
                flag=0
                break
            elif len(answer_list) <5:
                not_possible=1
                for l in answer_list:
                    if l not in char_dict:
                        print('That is not possible, try again!')
                        not_possible=0
                        break
                if not_possible == 1:
                    if not all(True if answer_list.count(item) <= dice_list.count(item) else False for item in answer_list):
                        print('That is not possible, try again!')
                    else:
                        flag=1
                        #print('deleted')
                        del dice_list[:]
                        for i in answer_list: 
                            dice_list.append(number_dict[i])
                        hold=len(dice_list)
                        break
            elif len(answer_list) == 5:
                if not all(True if answer_list.count(item) <= dice_list.count(item) else False for item in answer_list):
                    print('That is not possible, try again!')
                else:
                    flag=0
                    print('Ok, done.')
                    break
            else:
                print(answer_list)
                print('That is not possible, try again!')

        if flag==1:
            continue
        else:
            break
