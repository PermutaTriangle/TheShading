
def subsets(elems):
    def bt(at, cur):
        if at == len(elems):
            yield cur
        else:
            for x in bt(at+1, cur): yield x
            for x in bt(at+1, cur + [elems[at]]): yield x
    for x in bt(0, []): yield x

want = set([
    (0,0),
    (0,1),
    (1,0),
    (1,1),
    (1,2),
    (1,3),
    (2,1),
    (2,2),
    (2,3),
    (3,1),
    (3,2)
])

bad = [
    set([(0,0),(1,1)]),
    set([(1,2),(2,3)]),
    set([(2,1),(3,2)]),
    set([(0,1),(1,0)]),
    set([(1,3),(2,2),(3,1)])
]

for mp in subsets(list(want)):
    mps = set(mp)
    if any( x <= mps for x in bad ):
        continue
    print(mp)

