# coding: utf-8

from permuta import (
    Perm,
    PermSet,
    MeshPatt,
    gen_meshpatts
)
from permuta.misc import UnionFind, subsets, ProgressBar, TrieMap, factorial
from misc import shad_to_binary, is_subset
import sys
import time
import math

mps = None
classpatt = None

perm_ids = dict()
id_perm = dict()
perm_set = None

def get_perm_id(perm):
    if perm not in perm_ids:
        perm_ids[perm] = len(perm_ids)
        id_perm[perm_ids[perm]] = perm
    return perm_ids[perm]

perm_class_ids = dict()

def get_perm_class_id(perm_class):
    # TODO: use perm_id for this as well? o.O
    if perm_class not in perm_class_ids:
        perm_class_ids[perm_class] = len(perm_class_ids)
        # perm_class_ids_dict[perm_class] = perm_class_ids[perm_class]
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
            assert MeshPatt.unrank(patt, i) == mp
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
    global mps
    global classpatt
    patt = classpatt
    assert patt is not None
    cnt = len(mps)
    mesh_perms = {}

    sys.stderr.write('Permutations of length %d\n' % l)
    ProgressBar.create(factorial(l))
    # For each permutation
    for perm in perm_set.of_length(l):
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
            poss.append(shad_to_binary(cur, len(patt) + 1))

        last = None
        maxima = []
        # compute the maximal sets of boxes that can be shaded
        for cur in sorted(poss):
            if cur == last:
                continue
            add = True
            for other in poss:
                if is_subset(cur, other) and cur != other:
                    add = False
                    break
            # pick out the maximal ones
            if add:
                maxima.append(cur)
            last = cur
        # for each maximal set, append the permutation to the list of containing permutations
        # any subset of the maximal set is then also contained in the permutation
        perm_id = get_perm_id(perm)
        for m in maxima:
            mesh_perms.setdefault(m, [])
            mesh_perms[m].append(perm_id)
    ProgressBar.finish()

    cont = {}
    notcnt = 0
    sys.stderr.write('Compare mesh patterns with occurrences, active = %d\n' % len(active))
    ProgressBar.create(sum(map(len, active)))

    # For each active class
    conts = {}
    for (mpatts, contset) in zip(active, contsets):

        # We monitor whether the class will split or not
        for i in mpatts:
            ProgressBar.progress()
            perms = set()
            for (maxi, ps) in mesh_perms.items():
                if is_subset(mps[i], maxi):
                    perms |= set(ps)
            permset_id = get_perm_class_id(tuple(sorted(perms)))
            permid_vec = contset + (permset_id,)
            cont.setdefault(permid_vec, [])
            cont[permid_vec].append(i)

    ProgressBar.finish()
    nowactive = []
    nowcontset = []

    for cs, v in cont.items():
        if len(v) > 1:
            nowactive.append(v)
            nowcontset.append(cs)
        else:
            singles.append(v[0])
    return (nowactive, nowcontset)

def brute_coincify(max_len):
    active = [list(range(len(mps)))]
    contsets = [ tuple() ]
    singles = []
    for l in range(len(classpatt), max_len+1):
        active, contsets = brute_coincify_len(l, active, contsets, singles)
    return (active, singles)

def supersets_of_mesh(n, mesh):
    left = [ (i,j) for i in range(n) for j in range(n) if (i,j) not in mesh ]
    for sub in subsets(left):
        yield (mesh | set(sub))


# --------------------------------------------------------------------------- #
classpatt = Perm(map(int, sys.argv[1].split()))

# mps = MeshPattSet(len(classpatt), classpatt)
# mps = [ i for i in range(2**((len(classpatt) + 1)**2))]
mps = [ int(p) for p in sys.stdin.readlines()]
avoidance_set = [Perm((2,0,1))]
perm_set = PermSet.avoiding(avoidance_set)

# ---------- Look for surprising coincidences ---------- #
# Upper bound (inclusive) on the length of permutations to look for surprising
# coincidences
perm_length = int(sys.argv[2])
classes, singleclasses = brute_coincify(perm_length)
print()
print('# Number of surprising coincidence classes {}'.format(len(classes) + len(singleclasses)))
print('# Number of non-singleton coincidence classes {}'.format(len(classes)))
print()

# ------------------- Sanity check --------------------- #
classes.extend([[i] for i in singleclasses])
# Set to True to perform a sanity check
san_check = False
print_classes = True
print_singleclasses = True

# Upper bound (inclusive) on the length of permutations to use for sanity check
check_len = 6

def internal_san_checker():
    avoiding = []
    cnt = len(mps)
    sys.stderr.write("Starting internal sanity check with {} classes.\n".format(len(classes)))
    ProgressBar.create(len(classes))
    for clas in classes:
        if len(clas) < 2:
            continue
        print('Sanity checking the class  %s' % str(clas))
        for l in range(1, check_len+1):
            for p in PermSet(l):
                last = None
                for i in clas:
                    if last is None:
                        last = p.avoids(MeshPatt.unrank(classpatt, mps[i]))
                        continue
                    av = p.avoids(MeshPatt.unrank(classpatt, mps[i]))
                    if av != last:
                        print('Noooooooooooooooo')
                        print(MeshPatt.unrank(classpatt, mps[i - 1]))
                        print('')
                        print(mps[i])
                        return
                    last = av
        ProgressBar.progress()
    ProgressBar.finish()
    print("Sanity check completed.")

def external_san_checker():
    for i in range(len(classes)):
        for j in range(i + 1, len(classes)):
            differ = False
            for l in range(1, check_len+1):
                for p in PermSet(l):
                    if p.avoids(classes[i][0]) != p.avoids(classes[j][0]):
                        differ = True
                        break
                if differ:
                    break
            if not differ:
                print('Noooooooooooooo')
                print(classes[i])
                print()
                print(classes[j])


if san_check:
    internal_san_checker()
    # external_san_checker()

if print_classes:
    print(tuple(classpatt))
    for clas in classes:
        if len(clas) < 2:
            continue
        print([mps[i] for i in clas])
        print("active")

if print_singleclasses:
    for clas in singleclasses:
        print([mps[clas]])
        print("inactive")

# ------------------------------------------------------ #
