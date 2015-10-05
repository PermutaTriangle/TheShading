from permuta import MeshPattern, Permutations, Permutation

# a = MeshPattern(Permutation([2,1,3,4]), set([]))
# b = MeshPattern(Permutation([2,1,3,4]), set([(3,0)]))
a = MeshPattern(Permutation([1,2,4,3]), set([ (i,j) for i in range(0,4+1) for j in range(0,4+1) if (i,j) not in {(2,2),(3,2),(4,4)} ]))
b = MeshPattern(Permutation([1,2,4,3]), set([ (i,j) for i in range(0,4+1) for j in range(0,4+1) if (i,j) not in {(3,2),(4,4)}]))

for l in range(1, 100):
    same = True
    for p in Permutations(l):
        x = p.avoids(a)
        y = p.avoids(b)
        if x != y:
            same = False
    print(l, same)

