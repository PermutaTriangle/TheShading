# coding: utf-8

# 1. Generate all 2x2 mesh patterns
# 2. Create union-find of coincidences given by shading lemma (and possibly simultaneous shading lemma)
# 3. Try to merge components that have same avoidance up to some length

from permuta import (
    Permutation,
    Permutations,
    MeshPattern,
    MeshPatterns,
)
from permuta.misc import UnionFind
import sys

def subsets(elems):
    def bt(at, cur):
        if at == len(elems):
            yield cur
        else:
            for x in bt(at+1, cur): yield x
            for x in bt(at+1, cur + [elems[at]]): yield x
    for x in bt(0, []): yield x

n = 3
# n = 3
# check_len = 7
check_len = 7
# check_len = 2
simultaneous = True
closure = True

mps = []
idx = {}
no = 0
for i,mp in enumerate(MeshPatterns(n)):
    if not (mp.perm == Permutation([1,3,2])):
        continue
    mps.append(mp)
    idx[mp] = no
    no += 1

cnt = len(mps)
uf = UnionFind(cnt)

bla = 0
for mp in mps:
    if bla % 1000 == 0:
        sys.stderr.write('A %d\n' % bla)
    bla += 1

    poss = []
    for i in range(n+1):
        for j in range(n+1):
            for sh in mp.can_shade((i,j)):
                if simultaneous and (i,j) not in mp.mesh:
                    poss.append((sh, set([(i,j)])))
                if not simultaneous:
                    uf.unite(idx[mp], idx[mp.shade((i,j))])

    if simultaneous:
        for i in range(n+1):
            for j in range(n+1):
                for di in range(-1,2):
                    for dj in range(-1,2):
                        if (di == 0) == (dj == 0):
                            continue
                        i2,j2 = (i+di, j+dj)
                        if 0 <= i2 < n+1 and 0 <= j2 < n+1:
                            for sh in mp.can_shade2((i,j),(i2,j2)):
                                poss.append((sh, set([(i,j),(i2,j2)])))

        def bt(at, nm, used):
            if at == len(poss):
                mp2 = mp.shade(nm)
                # print(cnt, idx[mp], idx[mp2])
                uf.unite(idx[mp], idx[mp2])
                return

            bt(at + 1, nm, used)
            if poss[at][0] not in used and not (nm & poss[at][1]):
                bt(at + 1, nm | poss[at][1], used | set([poss[at][0]]))

        bt(0, set(), set())

# print(len(found))

if closure:
    ss = {}
    for i in range(cnt):
        ss.setdefault(uf.find(i),[])
        ss[uf.find(i)].append(i)

    bla = 0
    for _,v in sorted(ss.items(),key=lambda k: min(k[1])):
        if bla % 1000 == 0:
            sys.stderr.write('B %d\n' % bla)
        bla += 1

        minima = []
        maxima = []
        for i in v:
            mp_cur = mps[i]
            is_maximal = True
            is_minimal = True
            for j in v:
                if i == j:
                    continue
                mp = mps[j]
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
                if mn <= mx:
                    for add in subsets(list(mx.mesh - mn.mesh)):
                        mid = mn.shade(set(add))
                        uf.unite(idx[mn], idx[mid])

comps = 0
for i in range(cnt):
    if i == uf.find(i):
        comps += 1

avoidance = {}
no = 1
for i in range(cnt):
    if i == uf.find(i):
        sys.stderr.write('%d/%d\n' % (no, comps))
        no += 1

        lst = []
        for l in range(check_len+1):
            for p in Permutations(l):
                if p.avoids(mps[i]):
                    lst.append(tuple(p.perm))
        lst = tuple(lst)
        avoidance.setdefault(lst, [])
        avoidance[lst].append(i)

mentioned = set()
for _,v in avoidance.items():
    if len(v) <= 1:
        continue
    print(v)
    mentioned |= set(v)
    # for i in range(len(v)):
    #     for j in range(i+1, len(v)):
    #         # print 'should be coincident', mps[v[i]], mps[v[j]]
    #         print 'should be coincident', v[i], v[j]
    #         mentioned.add(v[i])
    #         mentioned.add(v[j])

ss = {}
for i in range(cnt):
    ss.setdefault(uf.find(i),[])
    ss[uf.find(i)].append(i)

for m in sorted(mentioned):
    print 'Group', m
    for t in ss[uf.find(m)]:
        print(mps[t])
        print ""

# ss = {}
# for i in range(cnt):
#     ss.setdefault(uf.find(i),[])
#     ss[uf.find(i)].append(i)
#
# res = 0
# dudes = set()
# for _,v in sorted(ss.items(),key=lambda k: min(k[1])):
#     res += 1
#
#     found = False
#     for x in v:
#         if not mps[x].mesh:
#             found = True
#     if not found:
#         continue
#
#     # print('{%s}' % ','.join(map(str,sorted(v))))
#
#     #print(len(v))
#     for x in v:
#         dudes.add(mps[x])
#     # for bla in sorted(v):
#         # print(mps[bla])
#
#
#     # if len(v) > 1:
#     #     # Sanity check: make sure patterns in the same group are avoided by the same permutations
#     #     ans = None
#     #     for i in v:
#     #         mp = mps[i]
#     #         av = []
#     #         for l in range(1,check_len+1):
#     #             for p in Permutations(l):
#     #                 if p.avoids(mp):
#     #                     av.append(p)
#     #         if ans is None:
#     #             ans = av
#     #         assert av == ans
#
# print(res)

# def _rot_right(n,pos):
#     x,y = pos
#     assert 0 <= x < n+1
#     assert 0 <= y < n+1
#     return (y,n-x)
#
#     bla = 0
#     for _,v in sorted(ss.items(),key=lambda k: min(k[1])):
#         if bla % 1000 == 0:
#             print('B', bla)
#         bla += 1
#
#         minima = []
#         maxima = []
#         for i in v:
#             mp_cur = mps[i]
#             is_maximal = True
#             is_minimal = True
#             for j in v:
#                 if i == j:
#                     continue
#                 mp = mps[j]
#                 if mp_cur.mesh <= mp.mesh:
#                     is_maximal = False
#                 if mp.mesh <= mp_cur.mesh:
#                     is_minimal = False
#             if is_maximal:
#                 maxima.append(mp_cur)
#             if is_minimal:
#                 minima.append(mp_cur)
#
#         for mn in minima:
#             for mx in maxima:
#                 if mn <= mx:
#                     for add in subsets(list(mx.mesh - mn.mesh)):
#                         mid = mn.shade(set(add))
#                         uf.unite(idx[mn], idx[mid])

