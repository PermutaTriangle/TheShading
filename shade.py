from permuta import *
from permuta.misc import *

def tsa1(p,B):
    assert B not in p.mesh
    q = p.shade(B)
    k = len(p.perm)

    force = (1,3)

    def dfs(imp, putin, impxval, impyval, seen, depth_cutoff):
        if depth_cutoff == 0:
            return

        print 'Calling dfs'
        print imp
        print putin
        print impxval, impyval

        # if putin contains no points, then we're done
        # otherwise, it contains at least one point
        # for d in range(4):
        for d in [3, 2]:
        # for d in [0,1]:
        # for d in range(1):
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
            nxtyval = xval[1:putin[1]+1] + [(yval[putin[1]]+yval[putin[1]+1])/2.0] + yval[putin[1]+1:-1]
            # print nxtperm

            print 'Omg, it became'
            print nxt
            print nxtxval, nxtyval

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

                print occ
                # print hereperm

                sub = nxt.sub_mesh([ x+1 for x in occ ])
                add = p.mesh - sub.mesh
                # print add

                # print sub
                # print herexval
                # print hereyval
                # print add

                if len(add) == 0:
                    if force[1] == 0 and herexval[force[0]] > force[0]+1:
                        print 'wooooooooooooooooooooooooooooooooo'
                        return
                    elif force[1] == 1 and hereyval[p.perm[force[0]]-1] > p.perm[force[0]]:
                        print 'WoWowWowooooOOOoo'
                        return
                    elif force[1] == 2 and herexval[force[0]] < force[0]+1:
                        print 'woooooooooooooooooooooooo'
                        return
                    elif force[1] == 3 and hereyval[p.perm[force[0]]-1] < p.perm[force[0]]:
                        print 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwoooooooooooooooooooooooooo'
                        return

                if len(add) != 1:
                    print 'snatan2'
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

                print left, right, down, up

                left,right = ([0]+nxtxval+[k+1]).index(left), ([0]+nxtxval+[k+1]).index(right)
                down,up = ([0]+nxtyval+[k+1]).index(down), ([0]+nxtyval+[k+1]).index(up)

                # if herexval[B[0]-1] <= p.perm[B[0]-1]:
                #     continue
                #
                # # print sub
                # # print add
                # # print nxt
                # # print add, occ
                # print occ
                # left = occ[add[0]-1]
                # try:
                #     right = occ[add[0]]
                # except:
                #     right = len(nxt.perm)
                # # print left, right
                # # print occ[add[0]-1], occ[add[0]]
                # # print add[1]+1, sub.perm.perm
                # print (hereyval)[add[1]]
                # osomperm = [0] + sub.perm.perm
                # # print osomperm.index(add[1]) - 1
                # # print osomperm.index(add[1]) - 1, occ[osomperm.index(add[1]+1) - 1]
                # # down, up = nxt.perm[occ[osomperm.index(add[1]) - 1]], nxt.perm[occ[osomperm.index(add[1]+1) - 1]]
                # # down, up = osomperm.index(add[1]) - 1, osomperm.index(add[1]+1) - 1
                # # print left, right, down, up

                # print nxt
                # print sub

                # print 'meow'
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
                    print 'snatan'
                    return
                putin2 = list(putin2)[0]
                dfs(nxt, putin2, nxtxval, nxtyval, nseen, depth_cutoff-1)
                        # print x,y

    dfs(p, B, [ i+1 for i in range(k) ], [ i+1 for i in range(k) ], set([tuple(p.perm.perm)]), 8)


    # # if B contains no points, then we're done
    # # otherwise, it contains at least one point
    # # for i in range(4):
    # for i in range(1):
    #     # pick the east/north/west/south-most point
    #     nxt = p.add_point(B,i)
    #     val = [0] + p.perm.perm + [len(p.perm)+1]
    #     # print perm, B[0]
    #     # print perm[1:B[0]+1]
    #     # print [(perm[B[0]]+perm[B[0]+1])/2.0]
    #     # print perm[B[0]+1:-1]
    #     nxtval = val[1:B[0]+1] + [(val[B[0]]+val[B[0]+1])/2.0] + val[B[0]+1:-1]
    #     # print nxtperm
    #
    #     for occ in choose(len(nxtval), k):
    #         hereperm = [ nxt.perm[occ[i]] for i in range(k) ]
    #         hereval = [ nxtval[occ[i]] for i in range(k) ]
    #         if tuple(hereval) in seen:
    #             continue
    #         if not (Permutation.to_standard(hereperm) == p.perm):
    #             continue
    #         sub = nxt.sub_mesh([ x+1 for x in occ ])
    #         add = p.mesh - sub.mesh
    #         if len(add) != 1:
    #             continue
    #         add = list(add)[0]
    #         if hereval[B[0]-1] <= p.perm[B[0]-1]:
    #             continue
    #         # print sub
    #         # print add
    #         # print nxt
    #         # print add, occ
    #         left = occ[add[0]-1]
    #         try:
    #             right = occ[add[0]]
    #         except:
    #             right = len(nxt.perm)
    #         # print left, right
    #         # print occ[add[0]-1], occ[add[0]]
    #         down, up = nxt.perm[occ[sub.perm.perm.index(add[1])]], nxt.perm[occ[sub.perm.perm.index(add[1]+1)]]
    #         # print 'meow'
    #         putin = set()
    #         for x in range(left+1,right+1):
    #             for y in range(down,up):
    #                 if (x,y) not in nxt.mesh:
    #                     putin.add((x,y))
    #         assert len(putin) == 1
    #         putin = list(putin)[0]
    #         dfs(nxt, putin, nxtval)
    #                 # print x,y
    #         # dfs()


# tsa1(MeshPattern(Permutation([1,2,3]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1))
# tsa1(meshpattern(permutation([1,2,3]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1))
# tsa1(MeshPattern(Permutation([1,2,3]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (1,1))
# tsa1(MeshPattern(Permutation([1,2,3]), [(1,0),(1,3),(2,1),(3,0)]), (3,3))
# tsa1(MeshPattern(Permutation([1,2,3]), [(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1))
# tsa1(MeshPattern(Permutation([1,2,3]), [(0,1),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1))
# tsa1(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(2,3),(3,0),(3,1),(3,2),(3,2),(3,3)]), (2,1))
# tsa1(MeshPattern(Permutation([1,2,3]), [(0,3),(1,0),(1,1),(1,2),(2,0),(2,2),(3,0)]), (2,3))
# tsa1(MeshPattern(Permutation([1,2,3]), [(0,0),(0,3),(1,0),(1,1),(1,2),(2,0),(2,2),(3,0)]), (2,3))
tsa1(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(2,3),(3,0),(3,1)]), (2,1))

