# coding: utf-8

# 1. Generate all 2x2 mesh patterns
# 2. Create union-find of coincidences given by shading lemma (and possibly simultaneous shading lemma)
# 3. Try to merge components that have same avoidance up to some length


from permutation import Permutation
from permutations import Permutations
from mesh_pattern import MeshPattern
from mesh_patterns import MeshPatterns
from union_find import UnionFind

def subsets(elems):
    def bt(at, cur):
        if at == len(elems):
            yield cur
        else:
            for x in bt(at+1, cur): yield x
            for x in bt(at+1, cur + [elems[at]]): yield x
    for x in bt(0, []): yield x

n = 3
# check_len = 7
check_len = 0
simultaneous = True
closure = True

mps = []
idx = {}
for i,mp in enumerate(MeshPatterns(n)):
    mps.append(mp)
    idx[mp] = i
    # print(i, mp)

cnt = len(mps)
uf = UnionFind(cnt)

bla = 0
for mp in mps:
    if bla % 1000 == 0:
        print('A', bla)
    bla += 1

    poss = []
    for i in range(n+1):
        for j in range(n+1):
            ans = mp.can_shade((i,j))
            if simultaneous and (i,j) not in mp.mesh and ans:
                poss.append((ans, set([(i,j)])))
            if not simultaneous and ans:
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
                            ans = mp.can_shade2((i,j),(i2,j2))
                            if ans:
                                poss.append((ans, set([(i,j),(i2,j2)])))

        def bt(at, nm, used):
            if at == len(poss):
                mp2 = mp.shade(nm)
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
            print('B', bla)
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

ss = {}
for i in range(cnt):
    ss.setdefault(uf.find(i),[])
    ss[uf.find(i)].append(i)

res = 0
for _,v in sorted(ss.items(),key=lambda k: min(k[1])):
    res += 1
    # print('{%s}' % ','.join(map(str,sorted(v))))

    if len(v) > 1:
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

# def _rot_right(n,pos):
#     x,y = pos
#     assert 0 <= x < n+1
#     assert 0 <= y < n+1
#     return (y,n-x)
#
# # pos1 = (2,2)
# # pos2 = (2,1)
# # mp = MeshPattern(Permutation([2,1]), [])
# # for i in range(2):
# #     mp = mp.rotate_right()
# #     pos1 = _rot_right(2, pos1)
# #     pos2 = _rot_right(2, pos2)
# # print(mp)
# # print(pos1, pos2)
# # print mp._can_shade2(pos1, pos2)
#
# for mp in mps:
#     for i in range(n+1):
#         for j in range(n+1):
#             for di in range(-1,2):
#                 for dj in range(-1,2):
#                     if (di == 0) == (dj == 0):
#                         continue
#                     i2,j2 = (i+di, j+dj)
#                     if 0 <= i2 < n+1 and 0 <= j2 < n+1:
#                         print(mp, i,j, i2, j2)
#                         print mp.can_shade((i,j))
#                         print mp.can_shade((i2,j2))
#                         print mp.can_shade2((i,j),(i2,j2))
#                         if mp.can_shade2((i,j),(i2,j2)):
#                             assert mp.can_shade((i,j)) and mp.can_shade((i2,j2))
#
#                         # assert (mp.can_shade((i,j)) and mp.can_shade((i2,j2))) == mp.can_shade2((i,j),(i2,j2))


# mp = MeshPattern(Permutation([1,3,2]), [(0,1)])
# print mp.can_shade2((1,3),(2,3))


# TODO: closure (sjá hvað breytist)
# TODO: fall sem tekur við möskvamynstri og skilar flokknum sem það er í
# TODO: láta input vera umröðun
# TODO: aðskilja kóða, einfalt að gera shading lemma eða s. shading lemma +- closure

