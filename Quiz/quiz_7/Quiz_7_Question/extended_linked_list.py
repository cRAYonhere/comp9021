# Written by **** for COMP9021

from linked_list_adt import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def rearrange(self):

        node = self.head
        another_LL=LinkedList()
        another_node=Node()

        another_LL.head=another_node
        while node.next_node:
            if node.value % 2==1:
                end_node=node
            node=node.next_node

        #print(end_node.value)
        #end_node= node
        checking_node =node
        working_node = self.head
        while working_node.value % 2 == 0:
            another_node.next_node = working_node
            working_node=working_node.next_node
            another_node=another_node.next_node
            another_node.next_node=None
        self.head=working_node

        while working_node.next_node.next_node and checking_node != working_node.next_node.next_node:

            if working_node.next_node.value % 2== 0:
                another_node.next_node=working_node.next_node
                working_node.next_node=working_node.next_node.next_node
                another_node = another_node.next_node
                another_node.next_node=None

                continue
            working_node=working_node.next_node
        end_node.next_node=another_LL.head
        self.print()