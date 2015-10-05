from permuta import MeshPattern, Permutation


# mp = MeshPattern(Permutation([1,3,2]), [(0, 0), (1, 0), (2, 1), (2, 2), (3, 1)])
mp = MeshPattern(Permutation([1,3,2]), [])
print(mp)

print(mp.can_shade2((0,0), (0,1)))
print(mp.can_shade((2,2)))
print(mp.can_shade2((2,1), (3,1)))

