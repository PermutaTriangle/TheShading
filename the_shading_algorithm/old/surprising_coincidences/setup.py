import os
from permuta import *

def parse(line):
    parts = line.split()
    perm = [ i+1 for i in eval(parts[4].rstrip(',')) ]
    mesh = eval(parts[8].rstrip('}'))
    return MeshPattern(Permutation(perm), mesh)

surprises = []
CNT = {}
def pop(cur):
    perm = cur[0].perm
    perms = ''.join(map(str, perm))
    no = CNT.get(perms, 0) + 1

    at = 1
    for i in range(len(cur)):
        for j in range(i+1, len(cur)):
            surprises.append(('C%03d_%s_%d' % (no, perms, at), cur[i], cur[j]))
            at += 1

    CNT[perms] = no

with open('data.txt', 'r') as f:
    cur = []
    for line in f.read().split('\n'):
        if line.startswith('MP'):
            cur.append(parse(line))
        elif cur:
            pop(cur)
            cur = []
    if cur:
        pop(cur)

for (id,a,b) in surprises:
    os.mkdir(id)
    with open(os.path.join(id, '__init__.py'), 'w') as f:
        f.write('from permuta import *\n')
        f.write('mp1 = %s\n' % repr(a))
        f.write('mp2 = %s\n' % repr(b))

with open('tasks.txt', 'w') as f:
    for d in range(1, 7+1):
        for (id,_,_) in surprises:
            f.write('%s %d\n' % (id, d))

