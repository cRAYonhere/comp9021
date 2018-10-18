# Creates a class to represent a permutation of 1, 2, ..., n for some n >= 0.
#
# An object is created by passing as argument to the class name:
# - either no argument, in which case the empty permutation is created, or
# - "length = n" for some n >= 0, in which case the identity over 1, ..., n is created, or
# - the numbers 1, 2, ..., n for some n >= 0, in some order, possibly together with "lengh = n".
#
# __len__(), __repr__() and __str__() are implemented, the latter providing the standard form
# decomposition of the permutation into cycles (see wikepedia page on permutations for details).
#
# Objects have:
# - nb_of_cycles as an attribute
# - inverse() as a method
#
# The * operator is implemented for permutation composition, for both infix and in-place uses.
#
# Written by *** and Eric Martin for COMP9021


class PermutationError(Exception):
    def __init__(self, message):
        self.message = message

class Permutation:
    def __init__(self, *args, length = None, internal_list=[]):

        if not internal_list:
            if args:
                if not all(isinstance(n, int) for n in args):

                    raise PermutationError('Cannot generate permutation from these arguments')
                if len(set(args))!= len(args):
                    raise PermutationError('Cannot generate permutation from these arguments')
                if length:
                    if length < 0 or len(args) != length:
                        raise PermutationError('Cannot generate permutation from these arguments')
                for i in args:
                    if i <= 0 or i>len(args):
                        raise PermutationError('Cannot generate permutation from these arguments')

            elif length:
                if length<0:

                    raise PermutationError('Cannot generate permutation from these arguments')
                args = tuple([i for i in range(1, length + 1)])

            self.user_perm=args
        else:
            self.user_perm = tuple(internal_list)

        if len(self.user_perm) > 0:
            self.cycle_string = ''
            self.calc_cycles()
        else:
            self.cycle_string = '()'
            self.nb_of_cycles = 0
        # Replace pass above with your code

    def __len__(self):
        counter=0
        for i in self.user_perm:
            counter+=1
        return counter
        # Replace pass above with your code

    def __repr__(self):
        return f'Permutation{self.user_perm}'
        # Replace pass above with your code

    def __str__(self):
        return str(self.cycle_string)
        # Replace pass above with your code

    def __mul__(self, permutation):
        if len(self.user_perm)== len(permutation.user_perm):
            temp_perm = [0 for _ in range(len(self.user_perm))]
            for i in range(len(self.user_perm)):
                temp_perm[i]=permutation.user_perm[self.user_perm[i]-1]
            return Permutation(internal_list=temp_perm)
        else:
            raise PermutationError('Cannot compose permutations of different lengths')
        # Replace pass above with your code

    def __imul__(self, permutation):
        if len(self.user_perm) == len(permutation.user_perm):
            temp_perm = [0 for _ in range(len(self.user_perm))]

            for i in range(len(self.user_perm)):
                temp_perm[i]=permutation.user_perm[(self.user_perm[i]-1)]

            return Permutation(internal_list=temp_perm)

        else:
            raise PermutationError('Cannot compose permutations of different lengths')
        # Replace pass above with your code

    def inverse(self):
        temp_perm=[0 for _ in range(len(self.user_perm))]

        for i in range(1,len(self.user_perm)+1):
            temp_perm[self.user_perm[i-1]-1]=i

        return Permutation(internal_list=temp_perm)
        # Replace pass above with your code
        
    # Insert your code for helper functions, if needed
    def calc_cycles(self):

        seen = set()
        cycle = []
        final_cycle = []
        working = list(self.user_perm)
        cycle_string = ''
        length_user_perm = len(self.user_perm)
        i = max(self.user_perm)
        cycle_string = ''
        cycle_nb = 0
        while len(seen) < length_user_perm:
            if i not in seen:
                seen.add(i)
                working.remove(i)
                cycle.append(i)
                i = self.user_perm[i - 1]
            else:
                final_cycle.append(tuple(cycle))
                del cycle[:]
                if working:
                    i = max(working)

        final_cycle.append(tuple(cycle))
        final_cycle.sort()

        for i in final_cycle:
            cycle_string += str(i).replace(',', '')

        self.cycle_string = cycle_string
        self.nb_of_cycles = len(final_cycle)


