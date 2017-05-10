# coding: utf-8

from permuta import (
    Perm,
    PermSet,
    MeshPatt,
    gen_meshpatts
)
from permuta.misc import UnionFind, subsets, ProgressBar, TrieMap, factorial
import sys
import time
import math

from tsa5_eq import tsa5_coincident

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

class MeshPattSet(object):
    def __init__(self, n, patt=None):
        self.n = n
        self.patt = patt

        self.mps = []
        self.idx = {}

        sys.stderr.write('Generating mesh patterns\n')
        ProgressBar.create(2**((n+1)*(n+1)) * (factorial(n) if patt is None else 1))
        for i, mp in enumerate(gen_meshpatts(n, patt)):
            ProgressBar.progress()
            self.mps.append(mp)
            self.idx[mp] = i
        ProgressBar.finish()

    def get_id(self, mp):
        return self.idx[mp]

    def __getitem__(self, v):
        if type(v) is MeshPatt:
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

    def coincify(self, maxdepth=3, multbox=True, q_check=True, force_len=None):
        cnt = len(self.mps)
        n = self.mps.n

        sys.stderr.write('Shading lemma coincifier\n')
        ProgressBar.create(len(self.mps))
        for mpi, mp in enumerate(self.mps):
            ProgressBar.progress()

            if True:
                for mpj in range(mpi+1, len(self.mps)):
                    mp2 = self.mps[mpj]
                    if self.uf.find(self.mps[mp]) != self.uf.find(self.mps[mp2]) and tsa5_coincident(mp, mp2, maxdepth, multbox=multbox, q_check=q_check, force_len=force_len):
                        self.uf.unite(self.mps[mp], self.mps[mp2])
            else:
                poss = []
                for (i,j) in mp.non_pointless_boxes():
                    if (i,j) not in mp.shading:
                        # if all_points_all_dir(mp, (i,j), maxdepth, cut=True):
                        mp2 = mp.shade((i,j))
                        if self.uf.find(self.mps[mp]) != self.uf.find(self.mps[mp2]) and tsa5_coincident(mp, mp2, maxdepth, multbox=multbox, q_check=q_check, force_len=force_len):
                            self.uf.unite(self.mps[mp], self.mps[mp2])

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
                        if mp_cur.shading <= mp.shading:
                            is_maximal = False
                        if mp.shading <= mp_cur.shading:
                            is_minimal = False
                    if is_maximal:
                        maxima.append(mp_cur)
                    if is_minimal:
                        minima.append(mp_cur)

                for mn in minima:
                    for mx in maxima:
                        if mn.shading <= mx.shading:
                            for add in subsets(list(mx.shading - mn.shading)):
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
        # TODO: Comment this SHIT ALL THE WAY TO THE MAX

        sys.stderr.write('Permutations of length %d\n' % l)
        ProgressBar.create(factorial(l))
        # For each permutation
        for perm in PermSet(l):
            ProgressBar.progress()
            poss = []
            # loop over the occurrences of the underlying pattern exactly once
            for res in patt.occurrences_in(perm):
                con = set(perm[i] for i in res)
                colcnt = 0
                col = [-1]*len(perm)
                for v in perm:
                    if v in con:
                        colcnt += 1
                    else:
                        col[v] = colcnt
                rowcnt = 0
                row = [-1]*len(perm)
                for v in range(len(perm)):
                    if v in con:
                        rowcnt += 1
                    else:
                        row[v] = rowcnt
                # bad is the set of boxes that contain points and can not be shaded
                bad = set( (u,v) for u,v in zip(col,row) if u != -1 )
                # cur is the set of boxes that can be shaded
                cur = set( (u,v) for u in range(len(patt)+1) for v in range(len(patt)+1) if (u,v) not in bad )
                poss.append(cur)

            last = None
            maxima = []
            # compute the maximal sets of boxes that can be shaded
            for cur in sorted(poss):
                if cur == last:
                    continue
                add = True
                for other in poss:
                    if cur < other:
                        add = False
                # pick out the maximal ones
                if add:
                    maxima.append(cur)
                last = cur
            # for each maximal set, append the permutation to the list of containing permutations
            # any subset of the maximal set is then also contained in the permutation
            perm_id = get_perm_id(perm)
            for m in maxima:
                m = tuple(sorted(m))
                mesh_perms.setdefault(m, [])
                mesh_perms[m].append(perm_id)
        ProgressBar.finish()

        # find the maximally shaded mesh pattern in each component
        # max_shaded = {}
        # for i in range(cnt):
            # here = self.mps[i]
            # if self.uf.find(i) not in max_shaded or len(here.shading) > len(max_shaded[self.uf.find(i)]):
                # max_shaded[self.uf.find(i)] = here

        cont = {}
        notcnt = 0
        sys.stderr.write('Brute supersets, active = %d\n' % len(active))
        ProgressBar.create(len(active))
        # For each active component
        for i in active:
            perms = set()
            #here = max_shaded[i] # maximum shaded one in the component
            here = self.mps[i]
            ProgressBar.progress()
            notcnt += 1
            # print(i, here)
            # for every superset of the maximum shaded one in the component
            for nxt in supersets_of_mesh(n+1, here.shading):
                nxt = tuple(sorted(nxt))
                # gather all permutations that contain this maximum shaded mesh pattern
                if nxt in mesh_perms:
                    perms |= set(mesh_perms[nxt])

            # get id of the permutation class and append the active component
            # to the list of components that contain the class
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
        # active = set([ i for i in range(len(self.mps)) if i == self.uf.find(i) ])
        active = set([ i for i in range(len(self.mps)) ])
        for l in range(self.mps.n, max_len+1):
            last = self.brute_coincify_len(l, active)

            print('Surprising coincidences at length %d' % l)
            for _,v in last.items():
                if len(v) >= 2:
                    print(v)

            # ss = {}
            # for i in range(len(self.mps)):
                # ss.setdefault(self.uf.find(i),[])
                # ss[self.uf.find(i)].append(i)

            # for m in sorted(active):
                # print('Group', m)
                # for t in ss[self.uf.find(m)]:
                    # print(self.mps[t])
                    # print()

def supersets_of_mesh(n, mesh):
    left = [ (i,j) for i in range(n) for j in range(n) if (i,j) not in mesh ]
    for sub in subsets(left):
        yield (mesh | set(sub))

# mps = MeshPattSet(1, Perm([0]))
mps = MeshPattSet(2, Perm([0,1]))
# mps = MeshPattSet(3, Perm([1,2,3]))
# mps = MeshPattSet(3, Perm([1,3,2]))

# --------------------------------------------------------------------------- #
coin = ShadingLemmaCoincifier()

# ---------- Look for surprising coincidences ---------- #
# Upper bound (inclusive) on the length of permutations to look for surprising
# coincidences
perm_length = 7
coin.brute_coincify(perm_length)
# ------------------------------------------------------ #


# ------------------- Sanity check --------------------- #
# Set to True to perform a sanity check
san_check = True

# Upper bound (inclusive) on the length of permutations to use for sanity check
check_len = 0

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
            print('Sanity checking the class  %s' %v)
            # Sanity check: make sure patterns in the same group are avoided by the same permutations
            ans = None
            for i in v:
                mp = mps[i]
                av = []
                for l in range(1,check_len+1):
                    for p in PermSet(l):
                        if p.avoids(mp):
                            av.append(p)
                if ans is None:
                    ans = av
                if av != ans:
                    print('Noooooooooooooooo')
                    print(mps[0])
                    print('')
                    print(mps[i])
                    # for mp in [ mps[i] for i in v ]:
                    #     print mp
                    #     print ''
                assert av == ans

    print(res)
# ------------------------------------------------------ #

# coin.take_closure()
# coin = BruteCoincifier(mps)
# coin.coincify(7)
