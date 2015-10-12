# coding: utf-8

from permuta import (
    Permutation,
    Permutations,
    MeshPattern,
    MeshPatterns,
)
from permuta.misc import UnionFind, subsets, ProgressBar, TrieMap
from permuta.math import factorial
import sys
import time
import math

from shade import *

perm_ids = TrieMap()
def get_perm_id(perm):
    if perm not in perm_ids:
        perm_ids[perm] = len(perm_ids)
    return perm_ids[perm]

perm_class_ids = TrieMap()
def get_perm_class_id(perm_class):
    # TODO: use perm_id for this as well? o.O
    if perm_class not in perm_class_ids:
        perm_class_ids[perm_class] = len(perm_class_ids)
    return perm_class_ids[perm_class]

class MeshPatternSet(object):
    def __init__(self, n, patt=None):
        self.n = n
        self.patt = patt

        self.mps = []
        self.idx = {}

        sys.stderr.write('Generating mesh patterns\n')
        ProgressBar.create(2**((n+1)*(n+1)) * (factorial(n) if patt is None else 1))
        for i,mp in enumerate(MeshPatterns(n, patt)):
            ProgressBar.progress()
            self.mps.append(mp)
            self.idx[mp] = i
        ProgressBar.finish()

    def get_id(self, mp):
        return self.idx[mp]

    def __getitem__(self, v):
        if type(v) is MeshPattern:
            return self.get_id(v)
        else:
            return self.mps[v]

    def __len__(self):
        return len(self.mps)

    def __iter__(self):
        for mp in self.mps:
            yield mp

class Coincifier(object):
    def __init__(self, mps):
        self.mps = mps
        self.uf = UnionFind(len(self.mps))

class ShadingLemmaCoincifier(Coincifier):
    def __init__(self, mps):
        super(ShadingLemmaCoincifier, self).__init__(mps)

    def coincify(self, maxdepth=3):
        cnt = len(self.mps)
        n = self.mps.n

        sys.stderr.write('Shading lemma coincifier\n')
        ProgressBar.create(len(self.mps))
        for mp in self.mps:
            ProgressBar.progress()

            poss = []
            for (i,j) in mp.non_pointless_boxes():
                if (i,j) not in mp.mesh:
                    if all_points_all_dir(mp, (i,j), maxdepth, cut=True):
                        self.uf.unite(self.mps[mp], self.mps[mp.shade((i,j))])


            #         for sh in mp.can_shade((i,j)):
            #             if simultaneous and (i,j) not in mp.mesh:
            #                 poss.append((sh, set([(i,j)])))
            #             if not simultaneous:
            #                 self.uf.unite(self.mps[mp], self.mps[mp.shade((i,j))])
            #
            # if simultaneous:
            #     for i in range(n+1):
            #         for j in range(n+1):
            #             for di in range(-1,2):
            #                 for dj in range(-1,2):
            #                     if (di == 0) == (dj == 0):
            #                         continue
            #                     i2,j2 = (i+di, j+dj)
            #                     if 0 <= i2 < n+1 and 0 <= j2 < n+1:
            #                         for sh in mp.can_shade2((i,j),(i2,j2)):
            #                             poss.append((sh, set([(i,j),(i2,j2)])))
                #
                # def bt(at, nm, used):
                #     if at == len(poss):
                #         mp2 = mp.shade(nm)
                #         self.uf.unite(self.mps[mp], self.mps[mp2])
                #         return
                #
                #     bt(at + 1, nm, used)
                #     if poss[at][0] not in used and not (nm & poss[at][1]):
                #         bt(at + 1, nm | poss[at][1], used | set([poss[at][0]]))
                #
                # bt(0, set(), set())
        ProgressBar.finish()

    def take_closure(self):
        it = 0
        while True:
            it += 1
            changed = False
            sys.stderr.write('Shading lemma closure (no %d)\n' % (it))
            cnt = len(self.mps)
            ss = {}
            for i in range(cnt):
                ss.setdefault(self.uf.find(i),[])
                ss[self.uf.find(i)].append(i)

            ProgressBar.create(len(ss))
            for _,v in sorted(ss.items(),key=lambda k: min(k[1])):
                ProgressBar.progress()

                minima = []
                maxima = []
                for i in v:
                    mp_cur = self.mps[i]
                    is_maximal = True
                    is_minimal = True
                    for j in v:
                        if i == j:
                            continue
                        mp = self.mps[j]
                        if mp_cur.mesh <= mp.mesh:
                            is_maximal = False
                        if mp.mesh <= mp_cur.mesh:
                            is_minimal = False
                    if is_maximal:
                        maxima.append(mp_cur)
                    if is_minimal:
                        minima.append(mp_cur)

                for mn in minima:
                    for mx in maxima:
                        if mn.mesh <= mx.mesh:
                            for add in subsets(list(mx.mesh - mn.mesh)):
                                mid = mn.shade(set(add))
                                if self.uf.unite(self.mps[mn], self.mps[mid]):
                                    changed = True
            ProgressBar.finish()
            if not changed:
                break

    def brute_coincify_len(self, l, active):
        n = self.mps.n
        patt = self.mps.patt
        assert patt is not None
        cnt = len(self.mps)
        mesh_perms = {}

        sys.stderr.write('Permutations of length %d\n' % l)
        ProgressBar.create(factorial(l))
        for perm in Permutations(l):
            ProgressBar.progress()
            poss = []
            for res in containment(patt, perm):
                con = set(res)
                colcnt = 0
                col = [-1]*len(perm)
                for i,v in enumerate(perm):
                    if v in con:
                        colcnt += 1
                    else:
                        col[v-1] = colcnt
                rowcnt = 0
                row = [-1]*len(perm)
                for v in range(len(perm)):
                    if v+1 in con:
                        rowcnt += 1
                    else:
                        row[v] = rowcnt
                bad = set( (u,v) for u,v in zip(col,row) if u != -1 )
                cur = set( (u,v) for u in range(len(patt)+1) for v in range(len(patt)+1) if (u,v) not in bad )
                poss.append(cur)

            last = None
            maxima = []
            for cur in sorted(poss):
                if cur == last:
                    continue
                add = True
                for other in poss:
                    if cur < other:
                        add = False
                if add:
                    maxima.append(cur)
                last = cur
            perm_id = get_perm_id(perm)
            for m in maxima:
                m = tuple(sorted(m))
                mesh_perms.setdefault(m, [])
                mesh_perms[m].append(perm_id)
        ProgressBar.finish()

        max_shaded = {}
        for i in range(cnt):
            here = self.mps[i]
            if self.uf.find(i) not in max_shaded or len(here.mesh) > len(max_shaded[self.uf.find(i)]):
                max_shaded[self.uf.find(i)] = here

        cont = {}
        notcnt = 0
        sys.stderr.write('Brute supersets, active = %d\n' % len(active))
        ProgressBar.create(len(active))
        for i in active:
            perms = set()
            here = max_shaded[i]
            ProgressBar.progress()
            notcnt += 1
            # print(i, here)
            for nxt in supersets_of_mesh(n+1, here.mesh):
                nxt = tuple(sorted(nxt))
                if nxt in mesh_perms:
                    perms |= set(mesh_perms[nxt])
            # print(i, perms)
            # perms = tuple([ tuple(p) for p in sorted(perms) ])
            perms_id = get_perm_class_id(sorted(perms))
            cont.setdefault(perms_id, [])
            cont[perms_id].append(i)
        ProgressBar.finish()

        for _, v in cont.items():
            if len(v) == 1:
                active.remove(v[0])
        return cont

    def brute_coincify(self, max_len):
        # self.coincify_len(max_len)
        active = set([ i for i in range(len(self.mps)) if i == self.uf.find(i) ])
        for l in range(self.mps.n, max_len+1):
            last = self.brute_coincify_len(l, active)

            print 'Surprising coincidences at length %d' % l
            for _,v in last.items():
                if len(v) >= 2:
                    print(v)

            ss = {}
            for i in range(len(self.mps)):
                ss.setdefault(self.uf.find(i),[])
                ss[self.uf.find(i)].append(i)

            for m in sorted(active):
                print 'Group', m
                for t in ss[self.uf.find(m)]:
                    print(self.mps[t])
                    print ""

def containment(patt, perm):
    def con(i, now):
        if len(now) == len(patt):
            yield now
        elif i < len(perm):
            nxt = now + [perm[i]]
            if Permutation.to_standard(nxt) == Permutation.to_standard(patt[:len(nxt)]):
                for res in con(i+1, nxt):
                    yield res
            for res in con(i+1, now):
                yield res
    for res in con(0, []):
        yield res

def supersets_of_mesh(n, mesh):
    left = [ (i,j) for i in range(n) for j in range(n) if (i,j) not in mesh ]
    for sub in subsets(left):
        yield (mesh | set(sub))

# print MeshPattern(Permutation([1,2]),[]).non_pointless_boxes()

# mps = MeshPatternSet(1, Permutation([1]))
mps = MeshPatternSet(2, Permutation([1,2]))
# mps = MeshPatternSet(3, Permutation([1,2,3]))
# mps = MeshPatternSet(3, Permutation([1,3,2]))

# ------------------------ Run the shading algorithm ------------------------ #
# Set the maximum depth = maximum number of points can be added
maxdepth = 2

# Set to true to take the closure of each class at the end
with_closure = False

coin = ShadingLemmaCoincifier(mps)
coin.coincify(maxdepth)

if with_closure: coin.take_closure()
# --------------------------------------------------------------------------- #

# ---------- Look for surprising coincidences ---------- #
# Upper bound (inclusive) on the length of permutations to look for surprising
# coincidences
perm_length = 8
coin.brute_coincify(perm_length)
# ------------------------------------------------------ #


# ------------------- Sanity check --------------------- #
# Set to True to perform a sanity check
san_check = False

# Upper bound (inclusive) on the length of permutations to use for sanity check
check_len = 6

if san_check:
    uf = coin.uf
    cnt = len(coin.mps)

    ss = {}
    for i in range(cnt):
        ss.setdefault(uf.find(i),[])
        ss[uf.find(i)].append(i)

    res = 0
    for _,v in sorted(ss.items(),key=lambda k: min(k[1])):
        res += 1
        # print('{%s}' % ','.join(map(str,sorted(v))))

        if len(v) > 1:
            print 'Sanity checking the class  %s' %v
            # Sanity check: make sure patterns in the same group are avoided by the same permutations
            ans = None
            for i in v:
                mp = mps[i]
                av = []
                for l in range(1,check_len+1):
                    for p in Permutations(l):
                        if p.avoids(mp):
                            av.append(p)
                if ans is None:
                    ans = av
                assert av == ans

    print(res)
# ------------------------------------------------------ #

# coin.take_closure()
# coin = BruteCoincifier(mps)
# coin.coincify(7)
