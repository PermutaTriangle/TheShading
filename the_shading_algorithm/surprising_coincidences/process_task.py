import sys
import os

name = sys.argv[1]
depth = int(sys.argv[2])

done = False
for d in range(1, depth+1):
    path = os.path.join(name, 'depth_%02d.txt' % d)
    if not os.path.exists(path): continue
    with open(path, 'r') as f:
        st = f.readline()
        if st.strip() not in {'FAIL','ERROR'}:
            done = True
            break

if done:
    sys.exit(0)

sys.stderr.write("Running %s to depth %d\n" % (name, depth))

sys.path.append('../')
from permuta import *
import imp
from tsa2_clean import TSA, TSAResult

taskpath = os.path.join(name, '__init__.py')
task = imp.load_source(name, taskpath)

outfile = os.path.join(name, 'depth_%02d.txt' % depth)

try:
    tsa = TSA(task.mp1, task.mp2, depth)
    res = tsa.run()

    with open(outfile, 'w') as f:
        if res.res == TSAResult.CONTRADICTION:
            f.write('SUCCESS\n')
            f.write('p =\n%s\n' % task.mp1)
            f.write('q =\n%s\n' % task.mp2)
            f.write('%s\n' % str(res))
        else:
            f.write('FAIL\n')
except:
    with open(outfile, 'w') as f:
        f.write('ERROR\n')
        import traceback
        f.write('%s\n' % traceback.format_exc())

# print task.mp1
# print task.mp2

