from permuta import *
from permuta.misc import ProgressBar
import sys

# cpatt = Perm((0,1))
cpatt = Perm(map(int, sys.argv[1]))
# patts = [MeshPatt.unrank(cpatt, int(p)) for p in sys.stdin.readline().strip("[]\n").split(",")]
patts = [MeshPatt.unrank(cpatt, int(p)) for p in sys.stdin.readlines()]
# patts = [MeshPatt.unrank(cpatt, p) for p in [0, 23, 55, 151, 263, 269, 278, 284, 295, 301, 310, 316, 391, 397, 406, 412]]

sys.stderr.write("Comparing {} patterns with each other.\n".format(len(patts)))
ProgressBar.create(len(patts))

maximal = []
for i in range(len(patts)-1,-1,-1):
    ProgressBar.progress()
    ismax = True
    for j in range(len(patts)-1,-1,-1):
        if i == j:
            continue

        if patts[i].shading <= patts[j].shading:
            ismax = False
            break

    if ismax:
        maximal.append(patts[i])

ProgressBar.finish()

for p in maximal:
    print(p)
    print()
