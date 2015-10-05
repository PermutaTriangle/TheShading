from permuta import MeshPattern, MeshPatterns, Permutation, Permutations
from permuta.misc import ProgressBar, subsets
from permuta.math import factorial
import sys

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

#
# a = MeshPattern(Permutation([1,2]), set([(0,1),(1,2)]))
# b = MeshPattern(Permutation([1,2]), set([(0,1),(1,2), (2,2)]))
# #
# #  |#|
# # -+-2-
# # #| |
# # -1-+-
# #  | |
# #
# #
# #  |#|#
# # -+-2-
# # #| |
# # -1-+-
# #  | |
# #
#
# for p in Permutations(2):
#     x = p.contains(a)
#     y = p.contains(b)
#     if x != y:
#         print('hahah, fuck you Henning')
#         print(p)

# a = MeshPattern(Permutation([1,2]), set([(0,0), (0,2), (1,0), (2,1)]))
# b = MeshPattern(Permutation([1,2]), set([(0,0), (0,2), (1,0), (2,1), (2,2)]))
# # #| |
# # -+-2-
# #  | |#
# #  -1-+-
# # #|#|
# #
# # #| |#
# # -+-2-
# #  | |#
# #  -1-+-
# # #|#|
#
# for l in range(2, 5+1):
#     for p in Permutations(l):
#         if p.avoids(b):
#             print l, p

# patt = Permutation([1,3,2])
# patt = Permutation([1,2,3])
patt = Permutation([1,2,4,3])
# patt = Permutation([1,2])
n = len(patt)
mxlen = 9

# idx = {}
# mps = []
# groups = {}
# groupid = {}
# for mp in MeshPatterns(len(patt), patt):
#     idx[mp] = len(mps)
#     mps.append(mp)
#
#     no = idx[mp]
#     groups[no] = []
#     for l in range(len(patt), mxlen+1):
#         av = []
#         for perm in Permutations(l):
#             if perm.avoids(mp):
#                 av.append(perm)
#         av = tuple( tuple(p) for p in av )
#         if av not in groupid:
#             groupid[av] = len(groupid)
#         groups[no].append(groupid[av])
#
#     # print('%s %s' % (' '.join(map(str, groups[no])), no))
#
# for i in range(len(mps)):
#     for j in range(i+1, len(mps)):
#         diff = False
#         for k in range(len(groups[i])):
#             if groups[i][k] == groups[j][k]:
#                 if diff:
#                     print('counterexample:')
#                     print(mps[i])
#                     print(mps[j])
#             else:
#                 diff = True



idx = {}
mps = []
groups = {}
groupid = {}
for mp in MeshPatterns(len(patt), patt):
    idx[mp] = len(mps)
    mps.append(mp)

active = None
for l in range(n+1, mxlen+1):
    print('length %d' % l)

    ProgressBar.create(factorial(l))
    mesh_perms = {}
    for perm in Permutations(l):
        ProgressBar.progress()
        # perm = Permutation([5,2,1,6,4,3,7])
        # perm = Permutation([5,2,11,1,8,6,4,9,3,10,7])
        idx = {}
        for i,x in enumerate(perm):
            idx[x] = i
        poss = []
        for res in containment(patt, perm):
            # print([ i-1 for i in res ])
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
        for m in maxima:
            m = tuple(sorted(m))
            mesh_perms.setdefault(m, [])
            mesh_perms[m].append(perm)
    ProgressBar.finish()

    curactive = set()
    cont = {}
    notcnt = 0
    sys.stderr.write('Brute supersets, cnt = %d\n' % len(mps))
    ProgressBar.create(len(mps))
    for i in range(len(mps)):
        perms = set()
        here = mps[i]
        ProgressBar.progress()
        notcnt += 1
        # print(i, here)
        for nxt in supersets_of_mesh(n+1, here.mesh):
            nxt = tuple(sorted(nxt))
            if nxt in mesh_perms:
                perms |= set(mesh_perms[nxt])
        # print(i, perms)
        perms = tuple([ tuple(p) for p in sorted(perms) ])
        cont.setdefault(perms, [])
        cont[perms].append(i)
    ProgressBar.finish()

    sys.stdout.write('Looking for counterexamples, num active = %d\n' % (len(active) if active is not None else 0))
    for _,v in cont.items():
        v = sorted(v)
        for i in range(len(v)):
            for j in range(i+1, len(v)):
                # if active is not None and (i,j) not in active:
                #     print('Counterexample:')
                #     print(mps[i])
                #     print(mps[j])
                # print i,j
                # curactive.add((i,j))
                if active is not None and (v[i],v[j]) not in active:
                    print('Counterexample:')
                    print(mps[v[i]])
                    print(mps[v[j]])
                # print i,j
                curactive.add((v[i],v[j]))
    active = curactive
    # print '################'

