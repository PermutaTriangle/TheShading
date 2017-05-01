import sys
from permuta import Permutation, MeshPattern
from permuta.misc import UnionFind
import datetime

sys.path.append('..')
from tsa5_eq import tsa5_coincident

global outfile

def log(msg):
    print '[%s]\t%s' % (datetime.datetime.now(), msg)

def hamming(a,b):
    cnt = 0
    while a > 0 or b > 0:
        if (a&1) != (b&1):
            cnt += 1
        a >>= 1
        b >>= 1
    return cnt

def classify(classes, perm, mp_cnt, uf, depth, multbox, q_check, force_len):
    log('Running TSA with depth=%d, multbox=%s, q_check=%s, force_len=%s' % (depth, str(multbox), str(q_check), force_len))
    outfile.write('params %s\n' % repr((depth, multbox, q_check, force_len)))

    nclasses = []
    subclasses = 0
    if depth == -1:
        # Shading lemma

        for x in xrange(mp_cnt):
            if x != uf.find(x):
                outfile.write('unite %d %d\n' % (x, uf.find(x)))
        for cl in classes:
            if len(cl) >= 2:
                cur = sorted(cl)
                nclasses.append(cur)
                subclasses += len(cur)
                outfile.write('surprising %s\n' % ' '.join(map(str, cur)))
    else:

        for cl in classes:

            grp = { uf.find(x): [] for x in cl }
            for x in xrange(mp_cnt):
                p = uf.find(x)
                if p in grp:
                    grp[p].append(x)

            edges = []
            for i in range(len(cl)):
                for j in range(i+1, len(cl)):
                    for a in grp[uf.find(cl[i])]:
                        for b in grp[uf.find(cl[j])]:
                            edges.append((hamming(a,b), a, b))
            edges = sorted(edges)
            for (_,a,b) in edges:
                if uf.find(a) == uf.find(b):
                    continue

                mp1 = MeshPattern.unrank(perm, a)
                mp2 = MeshPattern.unrank(perm, b)
                if tsa5_coincident(mp1, mp2, depth, multbox=multbox, q_check=q_check, force_len=force_len):
                    uf.unite(a,b)
                    outfile.write('unite %d %d\n' % (a,b))

            cur = set()
            for x in cl:
                cur.add(uf.find(x))
            if len(cur) <= 1:
                continue
            cur = sorted(cur)
            nclasses.append(cur)
            outfile.write('surprising %s\n' % ' '.join(map(str, cur)))
            subclasses += len(cur)

    log('Done. Classes left: %d. Total no. of subclasses: %d' % (len(nclasses), subclasses))

    return nclasses

def main(argv):
    if len(argv) != 2:
        sys.stderr.write('usage: %s result_file\n' % argv[0])
        return 1

    classes = []
    with open(argv[1], 'r') as f:

        perm = f.readline().strip().split()
        assert len(perm) == 2 and perm[0] == 'perm'
        perm = Permutation(map(int, perm[1]), check=True)

        length = f.readline().strip().split()
        assert len(length) == 2 and length[0] == 'length'
        length = int(length[1])

        mp_cnt = 2**((len(perm) + 1) ** 2)
        uf = UnionFind(mp_cnt)
        assert f.readline().strip() == 'union find'
        for x, p in enumerate(map(int, f.readline().strip().split())):
            uf.unite(x, p)

        assert f.readline().strip() == 'classes'
        while True:
            cls = f.readline()
            if cls == '':
                break
            cls = map(int, cls.strip().split())
            classes.append(cls)

    global outfile
    outfile = 'surprising_%s.txt' % ''.join(map(str, perm))
    log('Writing output to %s' % outfile)
    outfile = open(outfile, 'w')

    outfile.write('perm %s\n' % ''.join(map(str, perm)))
    outfile.write('length %s\n' % length)

    params = []
    params.append((-1,False,False,0)) # Dummy params for shading lemma

    for depth in range(1, 9+1):
        for multbox in [False,True]:
            for q_check in [False,True]:
                for force_len in range(1, len(perm)+1):
                    params.append((depth, multbox, q_check, force_len))

    for par in params:
        classes = classify(classes, perm, mp_cnt, uf, *par)

    outfile.close()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

