import sys
from permuta import Perm, MeshPatt
from permuta.misc import UnionFind


def is_boundary_anchored(patt):
    inv = patt.pattern.inverse()
    right, top, left, bottom = patt.has_anchored_point()
    in_bound = set()
    if not right and not left and not top and not bottom:
        return False
    if right:
        in_bound.add(len(patt) - 1)
    if left:
        in_bound.add(0)
    if top:
        in_bound.add(inv[len(patt) - 1])
    if bottom:
        in_bound.add(inv[0])
    uf = UnionFind(len(patt))
    for i in range(1, len(patt)):
        if all((i, j) in patt.shading for j in range(len(patt) + 1)):
            uf.unite(i - 1, i)
        if all((j, i) in patt.shading for j in range(len(patt) + 1)):
            uf.unite(inv[i - 1], inv[i])
    # print(uf.leaders)
    return uf.leaders == set(uf.find(b) for b in in_bound)


# cpatt = Perm(map(int, sys.stdin.readline().split()))
cpatt = Perm(map(int, sys.argv[1]))
mpatts = map(int, sys.stdin.readlines())
for p in mpatts:
    patt = MeshPatt.unrank(cpatt, p)
    if not is_boundary_anchored(patt) and len(patt.shading) < 10:
        print(patt)
        print()
