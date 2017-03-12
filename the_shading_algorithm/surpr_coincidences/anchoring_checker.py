import sys
from permuta import *

cpatt = Perm(map(int, sys.stdin.readline().split()))
mpatts = map(int, sys.stdin.readline().split())
for p in mpatts:
    patt = MeshPatt.unrank(cpatt, p)
    if not any(patt.has_anchored_point()):
        print(patt)
        print()
