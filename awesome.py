from permuta import MeshPattern, Permutations, Permutation

a = MeshPattern(Permutation([1, 3, 2]), set([(0,0), (0,2), (1,1), (2,3)]))
b = MeshPattern(Permutation([1, 3, 2]), set([(0,0), (0,2), (1,1), (2,3), (2,2)]))

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

perm = Permutation([3, 4, 1, 6, 8, 2, 7, 5])
# for con in containment(a.perm, perm):
#     print(con)
#
# for res in containment(patt, perm):
patt = a.perm
for res in containment(a.perm, perm):
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
    print(cur)
    # poss.append(cur)

# for perm in Permutations(9):
#     if perm.contains(a) and not perm.contains(b):
#         print(perm)

