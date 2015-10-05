from permuta import MeshPattern, Permutation, Permutations

a = MeshPattern(Permutation([1,3,2]), set([(0,1),(0,2),(1,0),(2,2),(3,0),(3,1)]))
b = MeshPattern(Permutation([1,3,2]), set([(0,1),(0,2),(1,0),(2,2),(3,0),(3,1),(3,2)]))

for l in range(1, 100):
    ok = True
    for p in Permutations(l):
        x = p.avoids(a)
        y = p.avoids(b)
        if x != y:
            ok = False
            break
    print(l, ok)

