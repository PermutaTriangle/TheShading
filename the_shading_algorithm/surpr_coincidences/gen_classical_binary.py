from permuta import *
from permuta.misc import *
from misc import *
import sys
from itertools import chain

def gen_classical_binary(basis, n):
    perm_set = PermSet.avoiding(basis)
    permlen = 2 * max(map(len, basis))
    patts = list(chain.from_iterable(PermSet(l + 1) for l in range(n)))
    for length in range(permlen + 1):
        sys.stderr.write("Permutations of length {}\n".format(length))
        ProgressBar.create(factorial(length))
        for perm in perm_set.of_length(length):
            ProgressBar.progress()
            patts = list(filter(lambda x: x.count_occurrences_in(perm) < 2, patts))
        ProgressBar.finish()

    return patts

B = [Perm((0,1,2,3)), Perm((0,1,3,2)), Perm((0,2,1,3)), Perm((0,2,3,1)), Perm((0,3,1,2)), Perm((1,0,2,3)), Perm((1,2,0,3)), Perm((1,2,3,0)), Perm((2,0,1,3)), Perm((3,0,1,2))]

print(gen_classical_binary(B, 3))
