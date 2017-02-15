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

global mps

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
            # print(i)
            # print(mp)
            # print()
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


def brute_coincify_len(l, active, contsets, singles):
    n = mps.n
    patt = mps.patt
    assert patt is not None
    cnt = len(mps)
    mesh_perms = {}

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

    cont = {}
    notcnt = 0
    sys.stderr.write('Compare mesh patterns with occurrences, active = %d\n' % len(active))
    # ProgressBar.create(sum(map(len, active)))

    # For each active class
    conts = {}
    for (mpatts, contset) in zip(active, contsets):
        # print(mpatts, contset)
        for i in mpatts:
            # ProgressBar.progress()
            perms = set()
            for (maxi, ps) in mesh_perms.items():
                if mps[i].shading <= set(maxi):
                    # print(maxi, mps[i].shading, ps)
                    perms |= set(ps)
            permset_id = get_perm_class_id(sorted(perms))
            permid_vec = contset + (permset_id,)
            cont.setdefault(permid_vec, [])
            cont[permid_vec].append(i)

            # if i == 4:
                # print(permset_id, permid_vec)
                # print(cont[permid_vec])
                # print(mps[i])

    # print(cont)

    # ProgressBar.finish()
    nowactive = []
    nowcontset = []
    # print(cont)

    for cs, v in cont.items():
        if len(v) > 1:
            nowactive.append(v)
            nowcontset.append(cs)
        else:
            singles.append(v[0])
    return (nowactive, nowcontset)

def brute_coincify(max_len):
    # active = set([ i for i in range(len(mps)) ])
    active = [list(range(len(mps)))]
    contsets = [ tuple() ]
    singles = []
    for l in range(mps.n, max_len+1):
        active, contsets = brute_coincify_len(l, active, contsets, singles)
    return (active, singles)

        # print(active)

        # print('Surprising coincidences at length %d' % l)
        # for _,v in last.items():
            # if len(v) >= 2:
                # print(v)

        # for m in sorted(active):
            # print('Group', m)
            # for t in ss[self.uf.find(m)]:
                # print(self.mps[t])
                # print()

def supersets_of_mesh(n, mesh):
    left = [ (i,j) for i in range(n) for j in range(n) if (i,j) not in mesh ]
    for sub in subsets(left):
        yield (mesh | set(sub))


# --------------------------------------------------------------------------- #
# mps = MeshPattSet(1, Perm([0]))
mps = MeshPattSet(2, Perm([0,1]))
# mps = MeshPattSet(3, Perm([0,1,2]))
# mps = MeshPattSet(3, Perm([0,2,1]))

# ---------- Look for surprising coincidences ---------- #
# Upper bound (inclusive) on the length of permutations to look for surprising
# coincidences
perm_length = 6
classes, singleclasses = brute_coincify(perm_length)

# ------------------- Sanity check --------------------- #
classes.extend([i] for i in singleclasses)
# Set to True to perform a sanity check
san_check = True

# Upper bound (inclusive) on the length of permutations to use for sanity check
check_len = 4

def san_checker():
    cnt = len(mps)
    for clas in classes:
        if len(clas) < 2:
            break
        print('Sanity checking the class  %s' % str(clas))
        for l in range(1, check_len+1):
            for p in PermSet(l):
                last = None
                for i in clas:
                    if last is None:
                        last = p.avoids(mps[i])
                        continue
                    av = p.avoids(mps[i])
                    if av != last:
                        print('Noooooooooooooooo')
                        print(mps[i - 1])
                        print('')
                        print(mps[i])
                        return
                    last = av

if san_check:
    san_checker()

# ------------------------------------------------------ #
