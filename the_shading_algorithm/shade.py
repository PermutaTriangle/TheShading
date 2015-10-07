from permuta import *
from permuta.misc import *

def dir_adj(d):
    if d == 0:
        return "right-most"
    elif d == 1:
        return "highest"
    elif d == 2:
        return "left-most"
    elif d == 3:
        return "lowest"

def dir_adj2(d):
    if d == 0:
        return "right"
    elif d == 1:
        return "up"
    elif d == 2:
        return "left"
    elif d == 3:
        return "down"

def tsa1(p, B, force=(1,0), maxdepth=3):
    assert B not in p.mesh
    q = p.shade(B)
    k = len(p.perm)

    instr = ["Initial pattern:",
            str(p),
            "We consider the occurence of the pattern where b = {} and is the {}".format(p.perm.perm[force[0]], dir_adj(force[1]))]
    traces = []

    def dfs(imp, putin, impxval, impyval, seen, depth_cutoff, instructions):
        if depth_cutoff == 0:
            return

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

            cur_instr1 = list(instructions)
            cur_instr1.append("We consider the {} point in box ({}, {})".format(dir_adj(d), putin[0], putin[1]))
            cur_instr1.append("And get:")
            cur_instr1.append(str(nxt))

            #print 'Omg, it became'
            #print nxt
            #print nxtxval, nxtyval

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

                cur_instr2 = list(cur_instr1)
                if len(add) == 0:
                    if force[1] == 0 and herexval[force[0]] > force[0]+1:
                        cur_instr2.append("We now consider the subsequence ({}) which is an occurrence of p with {} further right, CONTRADICTION".format(
                                ', '.join([str(i) for i in occ]), sub.perm.perm[force[0]]))
                        traces.append(cur_instr2)
                        #print "wooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
                        return
                    elif force[1] == 1 and hereyval[p.perm[force[0]]-1] > p.perm[force[0]]:
                        cur_instr2.append("We now consider the subsequence ({}) which is an occurrence of p with {} further up, CONTRADICTION".format(
                                    ', '.join( [str(i) for i in occ]), sub.perm.perm[force[0]]))
                        traces.append(cur_instr2)
                        #print "wooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
                        return
                    elif force[1] == 2 and herexval[force[0]] < force[0]+1:
                        cur_instr2.append("We now consider the subsequence ({}) which is an occurrence of p with {} further left, CONTRADICTION".format(
                                ', '.join( [str(i) for i in occ]), sub.perm.perm[force[0]]))
                        traces.append(cur_instr2)
                        #print "wooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
                        return
                    elif force[1] == 3 and hereyval[p.perm[force[0]]-1] < p.perm[force[0]]:
                        cur_instr2.append("We now consider the subsequence ({}) which is an occurrence of p with {} further down, CONTRADICTION".format(
                                ', '.join([str(i) for i in occ]), sub.perm.perm[force[0]]))
                        traces.append(cur_instr2)
                        #print "wooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
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

                #print left, right, down, up

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

                cur_instr2.append('We now consider the subsequence ({})'.format(', '.join([str(i) for i in occ])))
                cur_instr2.append("Which is the pattern")
                cur_instr2.append(str(sub))

                cur_instr2.append(("If the box ({}, {}), which corresponds to "
                        "the box(es) bounded by ({},{}) and ({},{}) in the larger "
                        "pattern is empty, we have a contradiction because we "
                        "have another occurence of p where {} is further "
                        "{}").format(add[0], add[1], left, down, right, up,
                        sub.perm.perm[force[0]], dir_adj2(force[1])))

                dfs(nxt, putin2, nxtxval, nxtyval, nseen, depth_cutoff-1, cur_instr2)
                        # print x,y

    dfs(p, B, [ i+1 for i in range(k) ], [ i+1 for i in range(k) ], set([tuple(p.perm.perm)]), maxdepth, instr)
    return traces


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

def all_points_all_dir(mp, B, maxdepth):
    all_traces = []
    for i in range(len(mp.perm.perm)):
        for d in range(4):
            all_traces += tsa1(mp, B, (i,d), maxdepth)
    return all_traces

#C1
#run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), 3)
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
run = all_points_all_dir(MeshPattern(Permutation([1,2,3]), [(1,0),(1,3),(2,1),(3,0)]), (3,3), 10)

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
print("\nTotal number of successful branches: {}\n".format(len(run)))
