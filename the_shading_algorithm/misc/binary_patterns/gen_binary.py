# For all permutations:
#   find all occurrences of cpatt
#   find the maximal pattern in each occurrence
#   for every pair of maximal pattern:
#       the intersection is non-binary
#       every subset of the intersection is non-binary
#       collect only the maximal intersections
# wal through the pattern poset from the top to collect the final patterns

from permuta import *
from permuta.misc import *
from misc import *
import sys

cpatt = Perm(map(int, list(sys.argv[1])))
avoidance = []

if len(sys.argv) > 2:
    avoidance = [ Perm(map(int, p)) for p in map(list, sys.argv[2:]) ]

perm_set = PermSet.avoiding(avoidance)
permlen = len(cpatt) * 2
maxexclude = set()

for length in range(permlen + 1):
    sys.stderr.write("Permutations of length {}\n".format(length))
    ProgressBar.create(factorial(length))
    for perm in perm_set.of_length(length):
        ProgressBar.progress()
        poss = []
        # loop over the occurrences of the underlying pattern exactly once
        for res in cpatt.occurrences_in(perm):
            con = set(perm[i] for i in res)
            colcnt = 0
            col = [-1]*len(perm)
            for v in perm:
                if v in con:
                    colcnt += 1
                else:
                    col[v] = colcnt
            rowcnt = 0
            row = [-1]*len(perm)
            for v in range(len(perm)):
                if v in con:
                    rowcnt += 1
                else:
                    row[v] = rowcnt
            # bad is the set of boxes that contain points and can not be shaded
            bad = set( (u,v) for u,v in zip(col,row) if u != -1 )
            # cur is the set of boxes that can be shaded
            cur = set( (u,v) for u in range(len(cpatt)+1) for v in range(len(cpatt)+1) if (u,v) not in bad )
            poss.append(shad_to_binary(cur, len(cpatt) + 1))

        for i in range(len(poss)):
            for j in range(i + 1, len(poss)):
                maxexclude.add(poss[i] & poss[j])

        maxexclude = set(filter(lambda x:  all(not is_subset(x, y) or x == y for y in maxexclude), maxexclude))
    ProgressBar.finish()

# print("Max exclude {}".format(maxexclude))
binarypatterns = set()

def bt(i, cur):
    if any(is_subset(cur, x) for x in maxexclude):
        return
    if cur not in binarypatterns:
        binarypatterns.add(cur)
    if i >= 2**((len(cpatt) + 1)**2):
        return
    if cur & i:
        bt(i * 2, cur ^ i)
    bt(i * 2, cur)
bt(1, 2**((len(cpatt) + 1)**2) - 1)

for p in sorted(binarypatterns):
    print(p)
