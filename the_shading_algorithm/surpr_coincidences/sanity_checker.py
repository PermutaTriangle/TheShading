
import sys
from permuta import *
from permuta.misc import ProgressBar, factorial
from classify import parse_classes, ExpClasses
from tsa5_knowledge import tsa5_two as tsa5

maxlength = int(sys.argv[1])
cpatt = Perm(map(int, sys.argv[2].split()))
mpatts = [MeshPatt.unrank(cpatt, m) for m in map(int, sys.argv[3:])]

for l in range(len(cpatt), maxlength + 1):
    sys.stderr.write("Length {} permutations\n".format(l))
    # ProgressBar.create(factorial(l))
    for p in PermSet(l):
        # ProgressBar.progress()
        if len(set([p.avoids(mpatt) for mpatt in mpatts])) != 1:
            print("Found permutation")
            print(cpatt)
            print(mpatts)
            print([p.avoids(mpatt) for mpatt in mpatts])
            sys.exit(0)
    # ProgressBar.finish()
