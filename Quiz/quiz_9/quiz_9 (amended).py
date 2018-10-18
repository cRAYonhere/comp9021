# Generates a binary tree T whose shape is random and whose nodes store
# random even positive integers, both random processes being directed by user input.
# With M being the maximum sum of the nodes along one of T's branches, minimally expands T
# to a tree T* such that:
# - every inner node in T* has two children, and
# - the sum of the nodes along all of T*'s branches is equal to M.
#
# Written by *** and Eric Martin for COMP9021


import sys
from random import seed, randrange

from binary_tree_adt import *


def create_tree(tree, for_growth, bound):
    if randrange(max(for_growth, 1)):
        tree.value = 2 * randrange(bound + 1)
        tree.left_node = BinaryTree()
        tree.right_node = BinaryTree()
        create_tree(tree.left_node, for_growth - 1, bound)
        create_tree(tree.right_node, for_growth - 1, bound)

def max_path(tree):

    if tree.value is None:
        return 0

    if tree.left_node.value is not None:
        val_left=max_path(tree.left_node)
    else:
        val_left=0

    if tree.right_node.value is not None:
        val_right=max_path(tree.right_node)
    else:
        val_right=0

    if val_left >= val_right:
        return tree.value + val_left
    return tree.value + val_right

def expand_tree(tree,max):
    if max ==0:
        return
    if tree.left_node.value is None and max-tree.value:
        tree.left_node = BinaryTree(max-tree.value)
    else:
        expand_tree(tree.left_node,max-tree.value)
    if tree.right_node.value is None and max-tree.value:
        tree.right_node = BinaryTree(max-tree.value)
    else:
        expand_tree(tree.right_node,max-tree.value)
    return
    # Replace pass above with your code
# Possibly define other functions

try:
    for_seed, for_growth, bound = [int(x) for x in input('Enter three positive integers: ').split()
                                   ]
    if for_seed < 0 or for_growth < 0 or bound < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
 
seed(for_seed)
tree = BinaryTree()
create_tree(tree, for_growth, bound)
print('Here is the tree that has been generated:')
tree.print_binary_tree()
print(max_path(tree))
expand_tree(tree,max_path(tree))
#print('Here is the expanded tree:')
#tree.print_binary_tree()



