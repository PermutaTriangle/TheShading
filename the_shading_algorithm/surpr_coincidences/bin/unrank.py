import sys
from permuta import *
cpatt = Perm(map(int, sys.argv[1].split()))
for rank in  map(int, sys.argv[2:]):
    print(MeshPatt.unrank(cpatt, rank))
    print()
