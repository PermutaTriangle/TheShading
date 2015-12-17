from permuta import *
from permuta.misc import *
import time
import sys

pairs = {
'123_1': (
MeshPattern(Permutation([1, 2, 3]), set([(3, 3), (1, 0), (0, 3), (2, 1), (2, 2)])),
MeshPattern(Permutation([1, 2, 3]), set([(0, 0), (3, 3), (2, 2), (1, 0), (0, 3), (2, 1)]))
),

'123_2': (
MeshPattern(Permutation([1, 2, 3]), set([(2, 3), (3, 3), (2, 2), (1, 0), (0, 3), (2, 1)])),
MeshPattern(Permutation([1, 2, 3]), set([(0, 0), (2, 3), (3, 3), (2, 2), (1, 0), (0, 3), (2, 1)]))
),

'123_3': (
MeshPattern(Permutation([1, 2, 3]), set([(0, 3), (1, 0), (2, 1), (3, 3)])),
MeshPattern(Permutation([1, 2, 3]), set([(0, 3), (0, 0), (1, 0), (2, 1), (3, 3)]))
),

'123_4': (
MeshPattern(Permutation([1, 2, 3]), set([(0, 3), (1, 0), (2, 1), (2, 2)])),
MeshPattern(Permutation([1, 2, 3]), set([(0, 3), (0, 0), (1, 0), (2, 1), (2, 2)]))
),

'123_5': (
MeshPattern(Permutation([1, 2, 3]), set([(0, 3), (1, 0), (2, 1)])),
MeshPattern(Permutation([1, 2, 3]), set([(0, 3), (0, 0), (1, 0), (2, 1)]))
),


'132_1': (
MeshPattern(Permutation([1, 3, 2]), set([(1, 3), (2, 3), (1, 0), (0, 2), (2, 1), (1, 1)])),
MeshPattern(Permutation([1, 3, 2]), set([(1, 3), (2, 3), (2, 2), (1, 0), (0, 2), (2, 1), (1, 1)]))
),

'132_3': (
MeshPattern(Permutation([1, 3, 2]), set([(1, 0), (1, 3), (2, 3), (0, 2), (1, 1)])),
MeshPattern(Permutation([1, 3, 2]), set([(1, 3), (2, 3), (2, 2), (1, 0), (1, 1), (0, 2)]))
),

'132_10': (
MeshPattern(Permutation([1, 3, 2]), set([(1, 2), (0, 3), (3, 1), (2, 2)])),
MeshPattern(Permutation([1, 3, 2]), set([(1, 2), (0, 3), (3, 1), (1, 1), (2, 2)]))
)
}

def get_missing(a,sub,b):
    assert len(sub) == len(b)
    asub = a.sub_mesh(sub)
    assert asub.perm == b.perm

    res = []
    hs = [0]+sorted([ a.perm[x-1] for x in sub ])+[len(a)+1]
    ws = [0]+sub+[len(a)+1]
    for (x,y) in b.mesh - asub.mesh:
        for i in range(ws[x], ws[x+1]):
            for j in range(hs[y],hs[y+1]):
                if (i,j) not in a.mesh:
                    res.append((i,j))
    return res

# print p
# print get_missing(MeshPattern(Permutation([2,1,5,3,4,6]), []), [2,3,5], MeshPattern(Permutation([1,3,2]),[]))

def clear_screen():
    sys.stdout.write("\x1b[2J\x1b[H")

def header(p,q):
    clear_screen()
    print ''
    print splice('',splice(str(p),str(q),4),3)
    print ''

def splice(a, b, w=2):
    a = a.rstrip().split('\n')
    b = b.rstrip().split('\n')
    indent = max([ len(s) for s in a ]) + w
    res = [ (a[i] if i < len(a) else '').ljust(indent) + (b[i] if i < len(b) else '') for i in range(max(len(a), len(b))) ]
    return '\n'.join(res)

def tostr(p,stars):
    n = len(p)
    p = [ list(l) for l in str(p).split('\n') ]
    for (i,j) in stars:
        p[2*(n-j)][2*i] = 'X'
    return '\n'.join([ ''.join(l) for l in p ])

# slow = True
slow = len(sys.argv) >= 3 and sys.argv[2] == 'slow'

def doit(p,q,cur,first=False):
    if first:
        sub = range(1,len(p)+1)
    else:
        header(p,q)
        print splice('',str(cur),3)
        print '   ' + ''.join([ ''.join(str(n).rjust(2)[-2:]) for n in range(1,len(cur)+1) ])
        print ''
        inv = { cur.perm[i]:i+1 for i in range(len(cur)) }
        # sub = [ inv[x] for x in map(int,raw_input('Choose points: ').split()) ]
        sub = map(int, raw_input('Choose subsequence: ').split())
        print ''
        if slow:
            time.sleep(1)
    add = get_missing(cur,sub,q)
    header(p,q)
    print splice('',tostr(cur, add),3)
    print ''
    print 'Missing:', add
    print ''
    if len(add) > 1:
        x,y = map(int,raw_input('Which point to continue with: ').split())
        assert (x,y) in add
        for (x2,y2) in add:
            if (x,y) == (x2,y2): continue
            cur = cur.shade((x2,y2))
        add = [(x,y)]

    for (x,y) in add:
        ans = {'n':DIR_NORTH,'w':DIR_WEST,
               's':DIR_SOUTH,'e':DIR_EAST}[raw_input('Dir for (%d,%d) [nwse]: ' % (x,y))]
        nxt = cur.add_point((x,y),ans)
        if slow:
            time.sleep(1)
        doit(p,q,nxt)

p,q = pairs[sys.argv[1]]
doit(p,q,p,True)

