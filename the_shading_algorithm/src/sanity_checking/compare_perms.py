import sys
from permuta import *
from permuta.misc import ProgressBar, factorial

cpatt = Perm(map(int, sys.argv[1].split()))
mpatt1 = MeshPatt.unrank(cpatt, int(sys.argv[2]))
mpatt2 = MeshPatt.unrank(cpatt, int(sys.argv[3]))
length = 9

if len(sys.argv) > 4:
    length = int(sys.argv[4])

for l in range(len(cpatt), length + 1):
    sys.stderr.write("Length {}\n".format(l))
    ProgressBar.create(factorial(l))
    for perm in PermSet(l):
        ProgressBar.progress()
        if perm.avoids(mpatt1) != perm.avoids(mpatt2):
            print(perm.avoids(mpatt1))
            print(perm.avoids(mpatt2))
            print("Avoidance of permutation {} differs.".format(perm))
            sys.exit(0)
    ProgressBar.finish()
