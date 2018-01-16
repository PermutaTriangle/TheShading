import os, sys
from permuta import *
from permuta.misc import ProgressBar, factorial
from classify import parse_classes, ExpClasses
from tsa5_knowledge import tsa5_two as tsa5

maxlength = int(sys.argv[1])
cpatt = Perm(map(int, sys.argv[2].split()))
mpatts = [MeshPatt.unrank(cpatt, m) for m in map(int, sys.argv[3:])]
sys.stderr.write(str([mpatt.rank() for mpatt in mpatts]))
sys.stderr.write("\n")

for l in range(len(cpatt), maxlength + 1):
    sys.stderr.write("Length {} permutations\n".format(l))
    sys.stderr.flush()
    cnt = 0
    last = (-1,)
    for p in PermSet(l):
        cnt += 1
        if len(set([p.avoids(mpatt) for mpatt in mpatts])) != 1:
            print("Found permutation")
            print(p)
            print(mpatts)
            print([p.avoids(mpatt) for mpatt in mpatts])
            sys.exit(0)
        if last[0] != p[0]:
            sys.stderr.write("   Permutations starting with {}\n".format(p[0]))
            sys.stderr.flush()
        last = p
