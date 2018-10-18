# Written by **** for COMP9021

from linked_list_adt import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def rearrange(self):
        odd = LinkedList()
        even = LinkedList()
        node = self.head
        odd_node = Node()
        even_node = Node()
        while node:
            if node.value % 2 == 0:
                if even.head == None:
                    even.head = node
                    even_node = even.head
                else:
                    even_node.next_node = node
                    even_node = even_node.next_node
            else:
                if odd.head == None:
                    odd.head = node
                    odd_node = odd.head
                else:
                    odd_node.next_node = node
                    odd_node = odd_node.next_node

            node = node.next_node
            odd_node.next_node = None
            even_node.next_node = None

        if odd.head != None:
            odd_node.next_node = even.head
            self.head = odd.head
        else:
            self.head = even.head
