# coding: utf-8

# 1. Generate all 2x2 mesh patterns
# 2. Create union-find of coincidences given by shading lemma (and possibly simultaneous shading lemma)
# 3. Try to merge components that have same avoidance up to some length

from permuta import (
    Permutation,
    Permutations,
    MeshPattern,
    MeshPatterns
)
from permuta.misc import UnionFind

def subsets(elems):
    def bt(at, cur):
        if at == len(elems):
            yield cur
        else:
            for x in bt(at+1, cur): yield x
            for x in bt(at+1, cur + [elems[at]]): yield x
    for x in bt(0, []): yield x

# n = 2
# check_len = 7
#
# ss = {}
# for i in range(cnt):
#     ss.setdefault(uf.find(i),[])
#     ss[uf.find(i)].append(i)
#
# for _,v in sorted(ss.items(),key=lambda k: min(k[1])):
#     # print('{%s}' % ','.join(map(str,sorted(v))))
#
#     if len(v) > 1:
#         # Sanity check: make sure patterns in the same group are avoided by the same permutations
#         ans = None
#         for i in v:
#             mp = mps[i]
#             av = []
#             for l in range(1,check_len+1):
#                 for p in Permutations(l):
#                     if p.avoids(mp):
#                         av.append(p)
#             if ans is None:
#                 ans = av
#             assert av == ans
#
# # DONE: closure (sjá hvað breytist)
# # DONE: fall sem tekur við möskvamynstri og skilar flokknum sem það er í
# # TODO: láta input vera umröðun
# # DONE: aðskilja kóða, einfalt að gera shading lemma eða s. shading lemma +- closure
#

mps = []
mpid = {}
uf = UnionFind()

def get_mpid(mp):
    if mp not in mpid:
        mpid[mp] = uf.add()
        assert mpid[mp] == len(mps)
        mps.append(mp)
    return mpid[mp]

def get_class(mp, simultaneous=True, closure=True):
    visited = set([mp])
    stack = [mp]
    while stack:
        while stack:
            cur = stack.pop()

            poss = []
            for i in range(len(cur)+1):
                for j in range(len(cur)+1):
                    # TODO: only go through boxes that have an adjacent point
                    ans = cur.can_shade((i,j))
                    if ans:
                        if simultaneous:
                            if (i,j) not in cur.mesh:
                                poss.append((ans, set([(i,j)])))
                        else:
                            nxt = cur.shade((i,j))
                            if nxt not in visited:
                                stack.append(nxt)
                                visited.add(nxt)

            if simultaneous:
                for i in range(len(cur)+1):
                    for j in range(len(cur)+1):
                        for di in range(-1,2):
                            for dj in range(-1,2):
                                if (di == 0) == (dj == 0):
                                    continue
                                # TODO: only go through pairs of boxes that have an adjacent point
                                i2,j2 = (i+di, j+dj)
                                if 0 <= i2 < len(cur)+1 and 0 <= j2 < len(cur)+1:
                                    ans = cur.can_shade2((i,j),(i2,j2))
                                    if ans:
                                        poss.append((ans, set([(i,j),(i2,j2)])))

                def bt(at, nm, used):
                    if at == len(poss):
                        nxt = cur.shade(nm)
                        if nxt not in visited:
                            stack.append(nxt)
                            visited.add(nxt)
                        return

                    bt(at + 1, nm, used)
                    if poss[at][0] not in used and not (nm & poss[at][1]):
                        bt(at + 1, nm | poss[at][1], used | set([poss[at][0]]))

                bt(0, set(), set())
        if closure:
            minima = []
            maxima = []
            for mp_cur in visited:
                is_maximal = True
                is_minimal = True
                for mp in visited:
                    if mp == mp_cur:
                        continue
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
                            if mid not in visited:
                                visited.add(mid)
                                stack.append(mid)
    return visited

# while True:
# mp = MeshPatterns(3).random_element()
# print(repr(mp))
# mp = MeshPattern(Permutations(3).random_element(), [])

# print(mp)

# mp = MeshPattern(Permutation([3,1,2]), [(0,1),(0,2),(0,3), (1,2), (2,0), (2,1), (2,3), (3,0)])
# print(mp)
# mp = MeshPattern(Permutation([1,2]), [(0,0),(1,0),(1,1),(1,2),(2,0)])
mp = MeshPattern(Permutation([1,2]), [(2,0)])

cnt = 0
for v in get_class(mp, True, True):
    print(repr(v))
    print(v)
    print('')
    cnt += 1
print(cnt)


# if closure:
#     ss = {}
#     for i in range(cnt):
#         ss.setdefault(uf.find(i),[])
#         ss[uf.find(i)].append(i)
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

