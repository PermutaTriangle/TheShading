
import sys
from permuta import *
from classify import parse_classes, ExpClasses
from tsa5_knowledge import tsa5_two as tsa5

inputfile = open(sys.argv[1])
expclasses = ExpClasses(list(parse_classes(inputfile)))
# expclasses = None
depth = 2

cpatt = Perm((0,1,2))
mpatt1 = 1144
mpatt2 = 3192

run = tsa5(MeshPatt.unrank(cpatt, mpatt1), MeshPatt.unrank(cpatt, mpatt2), depth=depth, multbox=True, q_check=False, force_len=None, knowledge=expclasses)

for r in run:
    print(r)
