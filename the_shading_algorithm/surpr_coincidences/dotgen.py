import graphviz
import os
import sys
from permuta import *
from classify import ExpClass, parse_classes

infile=sys.argv[1]
with open(infile) as f:
    for (i, clas) in enumerate(parse_classes(f)):
        print(clas)
        # clas.graphviz().save(os.path.join(os.path.dirname(infile), "expclass_{}_dot")
        # clas.graphviz().render(os.path.join(os.path.dirname(infile), "expclass_{}_dot.pdf"))
        clas.graphviz().render(filename="expclass_{}_dot".format(clas.pattrank[0]), directory=os.path.join(os.path.dirname(infile), os.path.basename(infile).rsplit('.', 1)[0]))
