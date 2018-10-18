# It is a text file you can copy paste
list_vvip = []

def preferred_sequence(L=[]):
    new_L = L[1:]
    new_L.sort(reverse=True)
    list_to_keep_track_of_lookingfor = new_L
    #print(list_to_keep_track_of_lookingfor)
    yet_another_list=[]
    for value in list_to_keep_track_of_lookingfor:
        if L:
            index_of_the_last_guy = len(L) - 1
            yet_another_list.append(index_of_the_last_guy)
            print(f'Index of the last guy:', index_of_the_last_guy)
            starting_child = index_of_the_last_guy
            restart = True
            while restart:
                print(f'Looking for {value}')
                value_looking_for = value
                index_of_value = L.index(value_looking_for)

                if index_of_the_last_guy % 2 == 0:
                    print('index id even')
                    if index_of_the_last_guy == starting_child:
                        index_of_the_last_guy = index_of_the_last_guy // 2
                        yet_another_list.append(index_of_the_last_guy)

                    elif L[index_of_the_last_guy] > L[index_of_the_last_guy + 1]:
                        index_of_the_last_guy = index_of_the_last_guy // 2
                        yet_another_list.append(index_of_the_last_guy)

                    elif index_of_the_last_guy != index_of_value:
                        print('going to next element in looking_for')
                        del yet_another_list[:]
                        break

                elif index_of_the_last_guy % 2 == 1:
                    print('index is odd')
                    if L[index_of_the_last_guy] > L[index_of_the_last_guy - 1]:
                        index_of_the_last_guy = index_of_the_last_guy // 2
                        yet_another_list.append(index_of_the_last_guy)
                    elif index_of_the_last_guy != index_of_value:
                        print('going to next element in looking_for')
                        del yet_another_list[:]
                        break

                if index_of_the_last_guy == index_of_value:
                    print('Amrut\'s Path List:',yet_another_list)

                    list_vvip.append(value_looking_for)
                    print('list_vvip', list_vvip)
                    for index in range(len(yet_another_list)- 1, 0, -1):
                        L[yet_another_list[index]]=L[yet_another_list[index-1]]
                    L.pop()
                    print('path:', yet_another_list)
                    print('Master Que:', L)
                    list_to_keep_track_of_lookingfor.remove(value_looking_for)

                    if len(list_to_keep_track_of_lookingfor) == 1:
                        list_vvip.extend(list_to_keep_track_of_lookingfor)
                        print('list_vvip',list_vvip)
                        list_to_keep_track_of_lookingfor.clear()
                        L.clear()
                        return list_vvip
                    else:
                        preferred_sequence(L)
                        return list_vvip

            if len(list_vvip) == len_init_list:
                print(f'The Other Final List: {list_vvip}')
                print(f'pq',pq)
                return list_vvip


#pq=[None,97,61,65,49,51,53,62,5,38,33]
#pq=[None,27,12,24]
#pq = [None , 65 , 53 , 62 , 33 , 49 , 5 , 51 ]
pq=[None , 149 , 130 , 129 , 107 , 122 , 124 , 103 , 66 , 77 , 91 , 98 , 10 , 55 , 35 , 72 ]
len_init_list=len(pq)-1
print(f'Final List: ',list(reversed(preferred_sequence(pq))))