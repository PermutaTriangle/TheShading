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

# def subsets(elems):
#     def bt(at, cur):
#         if at == len(elems):
#             yield cur
#         else:
#             for x in bt(at+1, cur): yield x
#             for x in bt(at+1, cur + [elems[at]]): yield x
#     for x in bt(0, []): yield x
#

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
    return visited

mp = MeshPatterns(5).random_element()

cnt = 0
for v in get_class(mp, True, True):
    print(repr(v))
    print(v)
    print('')
    cnt += 1
print(cnt)

