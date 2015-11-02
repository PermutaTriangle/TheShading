from permuta import *
from permuta.misc import *

STR_ADJ = ["right-most","highest","left-most","lowest"]
STR_ADJ2 = ["right","up","left","down"]

# MSGS = [
#     ('INITIAL_PATTERN', "Initial pattern:\n{}"),
#     ('CONSIDER_OCCURRENCE', "We consider the occurence of the pattern where b = {} and is the {}"),
#     ('CONSIDER_POINT', "We consider the {} point in box ({}, {})"),
#     ('AND_GET', "And get:\n{}"),
#     ('CONSIDER_SUB_RIGHT', "We now consider the subsequence ({}) which is an occurrence of p with {} further right, CONTRADICTION"),
#     ('CONSIDER_SUB_UP', "We now consider the subsequence ({}) which is an occurrence of p with {} further up, CONTRADICTION"),
#     ('CONSIDER_SUB_LEFT', "We now consider the subsequence ({}) which is an occurrence of p with {} further left, CONTRADICTION"),
#     ('CONSIDER_SUB_DOWN', "We now consider the subsequence ({}) which is an occurrence of p with {} further down, CONTRADICTION"),
#     ('CONSIDER_SUB', 'We now consider the subsequence ({})'),
#     ('WHICH_PATTERN', "Which is the pattern\n{}"),
#     ('ANOTHER_OCC', "If the box ({}, {}), which corresponds to the box(es) bounded by ({},{}) and ({},{}) in the larger pattern is empty, we have a contradiction because we have another occurence of p where {} is further {}"),
#     ('DOING_SNATAN', 'MEOWOOOOOOOOOOOOOOOOOOOOOO {}'),
# ]
#
# for i, v in enumerate(MSGS):
#     locals()[v[0]] = i

class TSAResult:
    CONTRADICTION = 0
    NO_CONTRADICTION = 1

    def __init__(self, res, desc='', cases=None):
        self.res = res
        self.desc = desc
        if cases:
            self.cases = [ case for case in cases ]
        else:
            self.cases = []

    @staticmethod
    def contradiction(*args):
        return TSAResult(TSAResult.CONTRADICTION, *args)
    @staticmethod
    def no_contradiction(*args):
        return TSAResult(TSAResult.NO_CONTRADICTION, *args)

    def __repr__(self):
        return 'TSAResult(%s, desc=%s, cases=%s)' % (
                    repr(self.res),
                    repr(self.desc),
                    repr(self.cases)
                )

    def _output(self, case, indent):
        pad = '    '*indent
        res = []
        if self.desc is not None:
            outp = 'Case %s: %s' % (case, self.desc)
            res.append('\n'.join([ pad + line for line in outp.split('\n') ]))
        for c in range(len(self.cases)):
            if len(self.cases) == 1:
                res.append(self.cases[c]._output(case, indent))
            else:
                if c != 0:
                    res.append(pad + '    ----------')
                res.append(self.cases[c]._output(case + '.%d' % (c+1), indent+1))
        return ''.join( s + '\n' for s in res )

    def __str__(self):
        return self._output('1', 0).rstrip()

class TSA:
    def __init__(self, p, q, depth):
        # TODO: clean up
        # TODO: assertions

        if q.mesh <= p.mesh:
            p,q = q,p
        assert p.mesh <= q.mesh
        add = q.mesh - p.mesh
        assert len(add) == 1

        self.p = p
        self.q = q
        self.shade = list(add)[0]
        self.cut = False
        self.mx_size = len(self.p) + depth
        self.k = len(p.perm)

    def do_empty_boxes(self, boxes, mp, *args):
        if len(boxes) == 1:
            desc = None
        else:
            desc = 'Now we have %d case(s)' % len(boxes)
        cases = []
        all = True
        shaded = set()
        for pi in boxes:
            res = self.init_dfs(mp.shade(shaded), pi, *args)
            if res.res != TSAResult.CONTRADICTION:
                all = False
                break
            shaded.add(pi)
            cases.append(res)

        if all:
            return TSAResult.contradiction(desc, cases)
        return TSAResult.no_contradiction()

    def add_point(self, mp, xyval, putin, d):
        xval, yval = xyval
        nxt = mp.add_point(putin,d)
        xval = [0] + xval + [self.k+1]
        yval = [0] + yval + [self.k+1]
        xval = xval[1:putin[0]+1] + [(xval[putin[0]]+xval[putin[0]+1])/2.0] + xval[putin[0]+1:-1]
        yval = yval[1:putin[1]+1] + [(yval[putin[1]]+yval[putin[1]+1])/2.0] + yval[putin[1]+1:-1]
        return (nxt, (xval, yval))

    def init_dfs(self, mp, putin, force, xyval, seen):

        # if putin contains no points, then we're done
        # otherwise, it contains at least one point
        for d in DIRS:
            # choose the east/north/west/south-most point

            nxt, nxtxyval = self.add_point(mp, xyval, putin, d)
            res = self.dfs(nxt, force, nxtxyval, seen)
            if res.res == TSAResult.CONTRADICTION:
                return TSAResult.contradiction('Choose the %s point in %s' % (STR_ADJ[d], putin), [res])

        return TSAResult.no_contradiction()

    def dfs(self, mp, force, xyval, seen):
        # print seen
        xval, yval = xyval

        desc0 = 'Now we have the permutation:\n%s' % mp

        for occ in choose(len(xval), self.k):
            subperm = [ mp.perm[occ[i]] for i in range(self.k) ]
            subxval = sorted([ xval[occ[i]] for i in range(self.k) ])
            subyval = sorted([ yval[subperm[i]-1] for i in range(self.k) ])

            if tuple(subxval) in seen:
                continue
            nseen = set(list(seen))
            nseen.add(tuple(subxval))
            if not (Permutation.to_standard(subperm) == self.p.perm):
                continue

            sub = mp.sub_mesh([ x+1 for x in occ ])
            adds = self.p.mesh - sub.mesh

            desc1 = desc0 + '\nWe choose the subsequence at indices %s and get the pattern:\n%s' % (occ, sub)

            if self.q.mesh <= sub.mesh:
                desc2 = desc1 + '\nThis is an instance of the objective pattern q, which means this branch leads to a contradiction'
                return TSAResult.contradiction(desc2)

            if len(adds) == 0:
                desc2 = desc1 + '\nThis is another instance of p where the point (%d,%d) is more to the %s, which means this branch leads to a contradiction.' % (force[0]+1, self.p.perm[force[0]], STR_ADJ2[force[1]])
                if force[1] == 0 and subxval[force[0]] > force[0]+1:
                    return TSAResult.contradiction(desc2)
                elif force[1] == 1 and subyval[self.p.perm[force[0]]-1] > self.p.perm[force[0]]:
                    return TSAResult.contradiction(desc2)
                elif force[1] == 2 and subxval[force[0]] < force[0]+1:
                    return TSAResult.contradiction(desc2)
                elif force[1] == 3 and subyval[self.p.perm[force[0]]-1] < self.p.perm[force[0]]:
                    return TSAResult.contradiction(desc2)

            if len(mp) >= self.mx_size:
                # We can't afford inserting more points :'(
                continue

            # if len(adds) != 1:
            #     #print 'snatan2' TODO: Address this in version 2 or 3 or ...
            #     continue

            # Use the force, Luke
            if force[1] == 0 and subxval[force[0]] <= force[0]+1:
                continue
            elif force[1] == 1 and subyval[self.p.perm[force[0]]-1] <= self.p.perm[force[0]]:
                continue
            elif force[1] == 2 and subxval[force[0]] >= force[0]+1:
                continue
            elif force[1] == 3 and subyval[self.p.perm[force[0]]-1] >= self.p.perm[force[0]]:
                continue

            boxes = set()
            inside = False
            for add in adds:
                txval = [0] + subxval + [self.k+1]
                tyval = [0] + subyval + [self.k+1]
                left,right = txval[add[0]], txval[add[0]+1]
                down,up = tyval[add[1]], tyval[add[1]+1]

                left,right = ([0]+xval+[self.k+1]).index(left), ([0]+xval+[self.k+1]).index(right)
                down,up = ([0]+yval+[self.k+1]).index(down), ([0]+yval+[self.k+1]).index(up)

                for x in range(left,right):
                    for y in range(down,up):
                        if (x,y) not in mp.mesh:
                            boxes.add((x,y))
                for x in range(left, right-1):
                    if down < mp.perm[x] < up:
                        inside = True
                        break
                if inside:
                    break
            if inside:
                continue

            assert len(boxes) > 0
            # if len(boxes) == 0:
            #     print repr(self.p)
            #     print repr(self.q)
            #     print repr(sub)
            #     print repr(xval), repr(yval)
            #     print repr(subxval), repr(subyval)

            # if len(boxes) != len(adds):
            #     continue

            # if len(boxes) != 1:
            #     # print 'snatan' TODO: Address this in version 2 or 3 or ...
            #     continue

            desc2 = desc1 + '\nWe need to worry about the non-shaded boxes %s in this sub-pattern, which correspond to %s in the current permutation' % (adds, boxes)
            res = self.do_empty_boxes(boxes, mp, force, xyval, nseen)
            if res.res == TSAResult.CONTRADICTION:
                return TSAResult.contradiction(desc2, [res])

        return TSAResult.no_contradiction()

    def run_specific(self, force):

        assert self.shade not in self.p.mesh

        # res = self.init_dfs(self.p, self.shade, force, ([ i+1 for i in range(self.k) ], [ i+1 for i in range(self.k) ]), set([tuple(self.p.perm.perm)]))
        res = self.init_dfs(self.p, self.shade, force, ([ i+1 for i in range(self.k) ], [ i+1 for i in range(self.k) ]), set([tuple([ i for i in range(1,self.k+1) ])]))
        return res

    def tsa3(self):
        for i in range(self.k):
            for d in range(4):
                res = self.run_specific((i,d))
                if res.res == TSAResult.CONTRADICTION:
                    return TSAResult.contradiction('Choose the occurrence of the pattern p where the point (%d,%d) is %s' % (i+1, self.p.perm[i], STR_ADJ[d]), [res])
        return TSAResult.no_contradiction()

    def run(self):
        return self.tsa3()

def tsa3(mp, shade, depth):
    print mp
    print 'shade', shade
    mp2 = mp.shade(shade)
    tsa = TSA(mp, mp2, depth)
    return tsa.run()

if __name__ == '__main__':

# [1 2 3] PATTERNS

    # run = tsa3(MeshPattern(Permutation([1]), [(1,1)]), (0,1), 5)

    #C1
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), 3)
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), (1, 3),  3)

    #C2
    # mp1 = MeshPattern(Permutation([1,2,3]), [(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)])
    # mp2 = mp1.shade((2,1))
    # run = TSA(mp1, mp2, 3).run()
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), 3)

    #C5
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,1),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), 3)

    # ---------------------------------------------------------------------------- #

    #C8
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,3),(1,0),(1,1),(1,2),(2,0),(2,2),(3,0)]), (2,3), 3)

    #C9
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(0,3),(1,0),(1,1),(1,2),(2,0),(2,2),(3,0)]), (2,3), 5)

    #C14
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(2,3),(3,0),(3,1),(3,2),(3,2),(3,3)]), (2,1), 3)

    # C15
    # C16

    # ---------------------------------------------------------------------------- #

    # C17
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(1,1),(1,3),(2,1),(2,2),(2,3),(3,0),(3,3)]), (1,0), 3)

    # C18
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(1,1),(1,3),(2,1),(2,2),(2,3),(3,0)]), (1,0), 3)

    # ---------------------------------------------------------------------------- #

    # C19
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(1,0),(1,3),(2,1),(3,0)]), (3,3), 4)

    # C20
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(1,3),(2,1),(3,0)]), (3,3), 5)

    # ---------------------------------------------------------------------------- #

    # C21
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(0,1),(1,1),(2,1),(2,2),(3,0)]), (3,2), 3)

    # C22
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(2,1),(2,2),(3,0)]), (3,2), 5)

    # C23
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(1,1),(2,1),(2,2),(3,0)]), (3,2), 3)

    # ---------------------------------------------------------------------------- #

    # C24
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(1,1),(2,1),(2,2),(2,3),(3,0),(3,3)]), (1,0), 3)

    # ---------------------------------------------------------------------------- #

    # C25
    #run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(1,2),(2,3),(3,0)]), (3,3), 5)

    # C26
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(1,1),(1,2),(2,3),(3,0)]), (3,3), 6)

    # C27
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(1,2),(2,3),(3,0)]), (3,3), 6)

    # C28
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(1,2),(2,3),(3,0)]), (3,3), 4)

    # C29
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(1,1),(1,2),(2,3),(3,0)]), (3,3), 4)

    # ---------------------------------------------------------------------------- #

    # C30 This is a chain
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(2,3),(3,0)]), (2,1), 3)
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(2,1),(2,3),(3,0)]), (3,3), 4)

    # ---------------------------------------------------------------------------- #

    # C31
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(1,1),(2,1),(2,2),(2,3),(3,0)]), (1,0), 4)

    # ---------------------------------------------------------------------------- #

    # C32
    #run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,1),(1,2),(2,2),(3,0),(3,3)]), (0,0), 5)

    # C33
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,1),(1,2),(2,2),(3,0),(3,2),(3,3)]), (0,0), 6)

    # C34
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,1),(1,2),(3,0),(3,3)]), (0,0), 6)

    # C35
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,1),(1,2),(2,2),(3,0)]), (0,0), 4)

    # C36
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,1),(1,2),(3,0)]), (0,0), 4)

    # ---------------------------------------------------------------------------- #

    # ---------------------------------------------------------------------------- #

    # C37
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,1),(1,1),(2,1),(2,2),(3,0)]), (3,2), 6)

    # ---------------------------------------------------------------------------- #

    # C38 This is a chain
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,1),(2,2),(3,0),(3,2),(3,3)]), (2,1), 6)
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,1),(2,1),(2,2),(3,0),(3,2),(3,3)]), (0,0), 6)

    # ---------------------------------------------------------------------------- #

    # ---------------------------------------------------------------------------- #

    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), 3)
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (1,1))
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(1,0),(1,3),(2,1),(3,0)]), (3,3))
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1))
    # run = tsa3(MeshPattern(Permutation([1,2,3]), [(0,0),(1,0),(1,1),(2,3),(3,0),(3,1)]), (2,1))

    # print("\n================================================================================\n".join(['\n'.join(i) for i in run]))
    # print("\nTotal number of successful branches: {}\n".format(len(run)))

# [1 3 2] PATTERNS

    # C32
    #run = tsa3(MeshPattern(Permutation([1,3,2]), [(0,1),(1,0),(3,2)]), (1,1), 5)

    # C34
    #run = tsa3(MeshPattern(Permutation([1,3,2]), [(0,1),(1,0),(1,2),(1,3),(2,2),(3,2)]), (1,1), 100000)

    # C35
    #run = tsa3(MeshPattern(Permutation([1,3,2]), [(0,1),(1,0),(2,2)]), (1,1), 2)

    # C36
    #run = tsa3(MeshPattern(Permutation([1,3,2]), [(0,1),(1,0)]), (1,1), 3)

    # C39
    #run = tsa3(MeshPattern(Permutation([1,3,2]), [(0,1),(1,0),(2,2),(2,3)]), (1,1), 5)

    # C39
    #run = tsa3(MeshPattern(Permutation([1,3,2]), [(0,1),(1,0),(2,2),(2,3)]), (1,1), 10)


    #run = tsa3(MeshPattern(Permutation([1,3,2]), []),(0,0), 100)

    if run.res == TSAResult.CONTRADICTION:
        print run
        # run.output()
    else:
        print run
        print 'Noooooooooo'

