from permuta import *
from permuta.misc import *

STR_ADJ = ["right-most","highest","left-most","lowest"]
STR_ADJ2 = ["right","up","left","down"]

MSGS = [
    ('INITIAL_PATTERN', "Initial pattern:\n{}"),
    ('CONSIDER_OCCURRENCE', "We consider the occurence of the pattern where b = {} and is the {}"),
    ('CONSIDER_POINT', "We consider the {} point in box ({}, {})"),
    ('AND_GET', "And get:\n{}"),
    ('CONSIDER_SUB_RIGHT', "We now consider the subsequence ({}) which is an occurrence of p with {} further right, CONTRADICTION"),
    ('CONSIDER_SUB_UP', "We now consider the subsequence ({}) which is an occurrence of p with {} further up, CONTRADICTION"),
    ('CONSIDER_SUB_LEFT', "We now consider the subsequence ({}) which is an occurrence of p with {} further left, CONTRADICTION"),
    ('CONSIDER_SUB_DOWN', "We now consider the subsequence ({}) which is an occurrence of p with {} further down, CONTRADICTION"),
    ('CONSIDER_SUB', 'We now consider the subsequence ({})'),
    ('WHICH_PATTERN', "Which is the pattern\n{}"),
    ('ANOTHER_OCC', "If the box ({}, {}), which corresponds to the box(es) bounded by ({},{}) and ({},{}) in the larger pattern is empty, we have a contradiction because we have another occurence of p where {} is further {}"),
]

for i, v in enumerate(MSGS):
    locals()[v[0]] = i

def tsa1(p, B, force, maxdepth=3):
    assert B not in p.mesh
    q = p.shade(B)
    k = len(p.perm)

    global instr
    instr = []

    class Popper:
        def __init__(self, k):
            self.k = k
        def __enter__(self):
            pass
        def __exit__(self, exc_type, exc_value, traceback):
            global instr
            for i in range(self.k):
                instr.pop()

    def msg(ms):
        global instr
        for x in ms:
            instr.append(x)
        return Popper(len(ms))

    instr.append((INITIAL_PATTERN, p))
    instr.append((CONSIDER_OCCURRENCE, p.perm.perm[force[0]], STR_ADJ[force[1]]))

    traces = []
    def dfs(imp, putin, impxval, impyval, seen, depth_cutoff):
        if depth_cutoff == 0:
            return False

        #print 'Calling dfs'
        #print imp
        #print putin
        #print impxval, impyval

        # if putin contains no points, then we're done
        # otherwise, it contains at least one point
        # for d in range(4):
        #for d in [3, 2]:
        #for d in [0]:
        for d in range(4):
            # d = 3
            # pick the east/north/west/south-most point
            # print imp
            # print putin
            # print d
            # print putin


            nxt = imp.add_point(putin,d)
            xval = [0] + impxval + [k+1]
            yval = [0] + impyval + [k+1]
            # print xval, yval
            # print perm, B[0]
            # print perm[1:B[0]+1]
            # print [(perm[B[0]]+perm[B[0]+1])/2.0]
            # print perm[B[0]+1:-1]
            nxtxval = xval[1:putin[0]+1] + [(xval[putin[0]]+xval[putin[0]+1])/2.0] + xval[putin[0]+1:-1]
            nxtyval = yval[1:putin[1]+1] + [(yval[putin[1]]+yval[putin[1]+1])/2.0] + yval[putin[1]+1:-1]
            # print nxtperm

            with msg([
                    (CONSIDER_POINT, STR_ADJ[d], putin[0], putin[1]),
                    (AND_GET, nxt),
                ]):

                for occ in choose(len(nxtxval), k):
                    hereperm = [ nxt.perm[occ[i]] for i in range(k) ]
                    herexval = [ nxtxval[occ[i]] for i in range(k) ]
                    hereyval = [ nxtyval[hereperm[i]-1] for i in range(k) ]

                    if tuple(herexval) in seen:
                        continue
                    nseen = set(list(seen))
                    nseen.add(tuple(herexval))
                    if not (Permutation.to_standard(hereperm) == p.perm):
                        continue

                    #print occ
                    # print hereperm

                    sub = nxt.sub_mesh([ x+1 for x in occ ])
                    add = p.mesh - sub.mesh
                    # print add

                    # print sub
                    #print herexval
                    #print hereyval
                    #print add

                    if len(add) == 0:
                        if force[1] == 0 and herexval[force[0]] > force[0]+1:
                            with msg([(CONSIDER_SUB_RIGHT, ', '.join([str(i) for i in occ]), sub.perm.perm[force[0]])]):
                                traces.append(list(instr))
                                return True
                        elif force[1] == 1 and hereyval[p.perm[force[0]]-1] > p.perm[force[0]]:
                            with msg([(CONSIDER_SUB_UP, ', '.join( [str(i) for i in occ]), sub.perm.perm[force[0]])]):
                                traces.append(list(instr))
                                return True
                        elif force[1] == 2 and herexval[force[0]] < force[0]+1:
                            with msg([(CONSIDER_SUB_LEFT, ', '.join( [str(i) for i in occ]), sub.perm.perm[force[0]])]):
                                traces.append(list(instr))
                                return True
                        elif force[1] == 3 and hereyval[p.perm[force[0]]-1] < p.perm[force[0]]:
                            with msg([(CONSIDER_SUB_RIGHT, ', '.join( [str(i) for i in occ]), sub.perm.perm[force[0]])]):
                                traces.append(list(instr))
                                return True

                    if len(add) != 1:
                        #print 'snatan2' TODO: Address this in version 2 or 3 or ...
                        continue

                    add = list(add)[0]
                    # print add
                    # print occ
                    # print sub
                    # print putin, herexval

                    if force[1] == 0 and herexval[force[0]] <= force[0]+1:
                        continue
                    elif force[1] == 1 and hereyval[p.perm[force[0]]-1] <= p.perm[force[0]]:
                        continue
                    elif force[1] == 2 and herexval[force[0]] >= force[0]+1:
                        continue
                    elif force[1] == 3 and hereyval[p.perm[force[0]]-1] >= p.perm[force[0]]:
                        continue

                    txval = [0] + herexval + [k+1]
                    tyval = [0] + hereyval + [k+1]
                    left,right = txval[add[0]], txval[add[0]+1]
                    down,up = tyval[add[1]], tyval[add[1]+1]

                    left,right = ([0]+nxtxval+[k+1]).index(left), ([0]+nxtxval+[k+1]).index(right)
                    down,up = ([0]+nxtyval+[k+1]).index(down), ([0]+nxtyval+[k+1]).index(up)

                    putin2 = set()
                    for x in range(left,right):
                        for y in range(down,up):
                            if (x,y) not in nxt.mesh:
                                putin2.add((x,y))
                    inside = False
                    for x in range(left, right-1):
                        if down < nxt.perm[x] < up:
                            inside = True
                            break
                    if inside:
                        continue
                    # print occ
                    # print sub
                    # print putin
                    if len(putin2) != 1:
                        # print 'snatan' TODO: Address this in version 2 or 3 or ...
                        return False
                    putin2 = list(putin2)[0]

                    with msg([
                            (CONSIDER_SUB, ', '.join([str(i) for i in occ])),
                            (WHICH_PATTERN, sub),
                            (ANOTHER_OCC, add[0], add[1], left, down, right, up, sub.perm.perm[force[0]], STR_ADJ2[force[1]]),
                        ]):

                        if dfs(nxt, putin2, nxtxval, nxtyval, nseen, depth_cutoff-1):
                            return True
        return False

    dfs(p, B, [ i+1 for i in range(k) ], [ i+1 for i in range(k) ], set([tuple(p.perm.perm)]), maxdepth)
    return [ [ MSGS[t[0]][1].format(*t[1:]) for t in ts ] for ts in traces ]

def all_points_all_dir(mp, B, maxdepth, cut=False):
    all_traces = []
    for i in range(len(mp.perm.perm)):
        for d in range(4):
            all_traces += tsa1(mp, B, (i,d), maxdepth)
            if cut and all_traces: return all_traces
    return all_traces


if __name__ == '__main__':

    run = all_points_all_dir(MeshPattern(Permutation([1]), [(1,1)]), (0,1), 5)

    #C1
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), 3)
    #run = tsa1(MeshPattern(Permutation([1,2,3]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), (1, 3),  3)

    #C2
    #run = tsa1(MeshPattern(Permutation([1,2,3]), [(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), 3)

    #C5
    #run = tsa1(MeshPattern(Permutation([1,2,3]), [(0,1),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), 3)

    # ---------------------------------------------------------------------------- #

    #C8
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,3),(1,0),(1,1),(1,2),(2,0),(2,2),(3,0)]), (2,3), 3)

    #C9
    #run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,0),(0,3),(1,0),(1,1),(1,2),(2,0),(2,2),(3,0)]), (2,3), 3)

    #C14
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(2,3),(3,0),(3,1),(3,2),(3,2),(3,3)]), (2,1), 3)

    # C15
    # C16

    # ---------------------------------------------------------------------------- #

    # C17
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(1,1),(1,3),(2,1),(2,2),(2,3),(3,0),(3,3)]), (1,0), 3)

    # C18
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(1,1),(1,3),(2,1),(2,2),(2,3),(3,0)]), (1,0), 3)

    # ---------------------------------------------------------------------------- #

    # C19
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(1,0),(1,3),(2,1),(3,0)]), (3,3), 10)

    # C20
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(1,3),(2,1),(3,0)]), (3,3), 4)

    # ---------------------------------------------------------------------------- #

    # C21
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,0),(0,1),(1,1),(2,1),(2,2),(3,0)]), (3,2), 3)

    # C22
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(2,1),(2,2),(3,0)]), (3,2), 6)

    # C23
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,0),(1,1),(2,1),(2,2),(3,0)]), (3,2), 3)

    # ---------------------------------------------------------------------------- #

    # C24
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(1,1),(2,1),(2,2),(2,3),(3,0),(3,3)]), (1,0), 3)

    # ---------------------------------------------------------------------------- #

    # C25
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(1,2),(2,3),(3,0)]), (3,3), 9)

    # C26
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,0),(1,1),(1,2),(2,3),(3,0)]), (3,3), 9)

    # C27
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,0),(1,2),(2,3),(3,0)]), (3,3), 9)

    # C28
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(1,2),(2,3),(3,0)]), (3,3), 9)

    # C29
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(1,1),(1,2),(2,3),(3,0)]), (3,3), 9)

    # ---------------------------------------------------------------------------- #

    # C30 This is a chain
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(2,3),(3,0)]), (2,1), 3)
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(2,1),(2,3),(3,0)]), (3,3), 4)

    # ---------------------------------------------------------------------------- #

    # C31
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(1,1),(2,1),(2,2),(2,3),(3,0)]), (1,0), 4)

    # ---------------------------------------------------------------------------- #

    # C32
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,1),(1,2),(2,2),(3,0),(3,3)]), (0,0), 8)

    # C33
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,1),(1,2),(2,2),(3,0),(3,2),(3,3)]), (0,0), 8)

    # C34
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,1),(1,2),(3,0),(3,3)]), (0,0), 10)

    # C35
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,1),(1,2),(2,2),(3,0)]), (0,0), 10)

    # C36
    # run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,1),(1,2),(3,0)]), (0,0), 10)

    # ---------------------------------------------------------------------------- #

    # ---------------------------------------------------------------------------- #

    # ---------------------------------------------------------------------------- #

    # run = tsa1(meshpattern(permutation([1,2,3]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1))
    # run = tsa1(MeshPattern(Permutation([1,2,3]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (1,1))
    # run = tsa1(MeshPattern(Permutation([1,2,3]), [(1,0),(1,3),(2,1),(3,0)]), (3,3))
    # run = tsa1(MeshPattern(Permutation([1,2,3]), [(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1))
    # run = tsa1(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(2,3),(3,0),(3,1)]), (2,1))

    print("\n================================================================================\n".join(['\n'.join(i) for i in run]))

