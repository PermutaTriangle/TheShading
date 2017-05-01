import sys
from permuta.misc import UnionFind
f = open(sys.argv[1], 'r')

def hamming(x):
    cnt = 0
    while x > 0:
        cnt += 1
        x = x & (x-1)
    return cnt

def get(expect=None):
    line = f.readline()
    if not line:
        if expect is not None:
            assert False
        return None, None
    key, val = line.strip().split(' ', 1)
    if expect is not None:
        assert expect == key
        return val
    return key, val


perm = get('perm')
n = len(perm)
length = int(get('length'))
uf = UnionFind(2**((n+1)**2))
surprising = []
params = []

while True:
    key,val = get()
    if not key:
        break
    if key == 'params':
        surprising = []
        params.append([eval(val), 0])
    elif key == 'unite':
        params[-1][1] += 1
        a,b = map(int,val.split())
        uf.unite(a,b)
    elif key == 'surprising':
        lst = map(int,val.split())
        surprising.append(lst)
    else:
        assert False

f.close()


coinc = []
pat = '\\pattern{scale=0.75}{%d}{%s}' % (len(perm), ','.join([ '%d/%s' % (i+1,v) for i,v in enumerate(perm) ]))

for lst in surprising:
    co = []
    for p in sorted(lst):
        # XXX: make this faster, if needed
        here = [ i for i in range(2**((n+1)**2)) if uf.find(i) == uf.find(p) ]
        best = -1
        for x in here:
            if best == -1 or hamming(best) < hamming(x):
                best = x
        co.append(best)

    s = '\\begin{center}\n'
    s += 'Coincidence %d\n' % (len(coinc)+1)

    print co

    for x in co:
        s += pat + '{' + ','.join( '%d/%d' % (i//(n+1),i%(n+1)) for i in range((n+1)**2) if (x & (1<<i)) != 0 ) + '}\n'

    s += '\\end{center}\n'
    coinc.append(s)

coinc = '\n'.join(coinc)
ptable = '\\begin{longtable}{ccccc} \n'
ptable += 'depth & multbox & q\\_{}check & forcelen & \\#united \\\\ \n'
for p in params:
    ptable += ' & '.join(map(str,list(p[0]) + [p[1]])) + ' \\\\ \n'
ptable += '\\end{longtable}'
template = open('pdf/template.tex', 'r').read()
res = (template.replace('PERMUTATION', perm)
               .replace('LENGTH', str(length))
               # .replace('PARAMS', '\n'.join( '\\item ' + repr(p[0]) + ', united ' + str(p[1]) for p in params ))
               .replace('PARAMS', ptable)
               .replace('COINCIDENCES', coinc))

with open('pdf/surprising_%s_%d.tex' % (perm, length), 'w') as of:
    of.write(res)

