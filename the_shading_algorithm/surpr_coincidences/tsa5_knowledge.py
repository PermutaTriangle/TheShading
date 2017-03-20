from permuta import *
from permuta.misc import *
from misc import *

# To try to prove that mesh patterns m1 and m2 are coincident, run tsa5_coincident(m1, m2, D), where D is a suitable depth.
# Note that permuta [1] has to be installed.
# [1]: https://github.com/PermutaTriangle/Permuta

STR_ADJ = ["right-most","highest","left-most","lowest"]
STR_ADJ2 = ["right","up","left","down"]

def splice(a, b):
    a = a.rstrip().split('\n')
    b = b.rstrip().split('\n')
    indent = max([ len(s) for s in a ]) + 5
    res = [ (a[i] if i < len(a) else '').ljust(indent) + (b[i] if i < len(b) else '') for i in range(max(len(a), len(b))) ]
    return '\n'.join(res)

class TSAForce:

    def __init__(self, force, is_universe=False):
        self.force = force if not is_universe else set()
        self.is_universe = is_universe

    @staticmethod
    def from_sub(perm, xval, yval, force_len):
        # TODO: update
        res = TSAForce(set())

        poss = [ set() for _ in range(len(perm)) ]
        same = [ False for _ in range(len(perm)) ]

        for i in range(len(perm)):
            cur = set()
            # INDEX CHANGE
            # if xval[i] == i+1:
            if xval[i] == i:
                same[i] = True
            # if xval[i] < i+1:
            if xval[i] < i:
                cur.add(DIR_WEST)
            # if xval[i] > i+1:
            if xval[i] > i:
                cur.add(DIR_EAST)
            # if yval[perm[i]-1] > perm[i]:
            if yval[perm[i]] > perm[i]:
                cur.add(DIR_NORTH)
            # if yval[perm[i]-1] < perm[i]:
            if yval[perm[i]] < perm[i]:
                cur.add(DIR_SOUTH)

            poss[i] = cur

        # print same
        # print poss

        rperm = []
        dirs = {}
        def bt(same_prefix, done):
            if len(rperm) == min(force_len, len(perm)):
                if not same_prefix:
                    # TODO: WTF DOES THIS DO
                    # INDEX CHANGE
                    # res.force.add(tuple([ (x+1,dirs[x]) for x in rperm ]))
                    res.force.add(tuple([ (x,dirs[x]) for x in rperm ]))
            else:
                for i in range(len(perm)):
                    if i in done:
                        continue

                    for d in range(4):
                        if same[i] or not same_prefix or (same_prefix and d in poss[i]):
                            dirs[i] = d
                            rperm.append(i)
                            bt(same_prefix and same[i], done | set([i]))
                            rperm.pop()

        bt(True, set())
        return res

    @staticmethod
    def none():
        return TSAForce(set())

    @staticmethod
    def all():
        return TSAForce(set(), is_universe=True)

    def __or__(self, other):
        if self.is_universe or other.is_universe: return TSAForce([], is_universe=True)
        return TSAForce(self.force | other.force)

    def __and__(self, other):
        if self.is_universe: return other
        if other.is_universe: return self
        return TSAForce(self.force & other.force)

    def __bool__(self):
        return self.is_universe or bool(self.force)
    __nonzero__ = __bool__

    def __repr__(self):
        if self.is_universe: return 'TSAForce(%s, is_universe=True)' % repr(self.force)
        return 'TSAForce(%s)' % repr(self.force)

    def __eq__(self, other):
        if self.is_universe or other.is_universe:
            return self.is_universe and other.is_universe
        return self.force == other.force

    def __len__(self):
        assert not self.is_universe
        return len(self.force)

    def __contains__(self, key):
        return self.is_universe or key in self.force

    # def __getitem__(self, *args):
    #     assert not self.is_universe
    #     return self.force.__getitem__(*args)



# for (a,b) in TSAForce.from_sub(Perm([0,2,1]), [1,1.25, 1.5], [1,1.25,1.5]).force:
# for (a,b) in TSAForce.from_sub(Perm([0,2,1]), [1.5,2,3], [1.5,2,3]).force:
#     print a,b
#
# import sys
# sys.exit(0)

class TSAResult:
    # CONTRADICTION = 0
    # NO_CONTRADICTION = 1

    def __init__(self, force, desc=None, cases=None, is_and=False):
        self.force = force
        self.desc = desc
        self.is_and = is_and
        if cases:
            self.cases = [ case for case in cases ]
        else:
            self.cases = []

    # @staticmethod
    # def contradiction(*args):
    #     return TSAResult(TSAResult.CONTRADICTION, *args)
    # @staticmethod
    # def no_contradiction(*args):
    #     return TSAResult(TSAResult.NO_CONTRADICTION, *args)

    def __repr__(self):
        return 'TSAResult(%s, desc=%s, is_and=%s, cases=%s)' % (
                    repr(self.force),
                    repr(self.desc),
                    repr(self.is_and),
                    repr(self.cases)
                )

    def _output(self, case, indent, force, do_case):
        pad = '    '*indent
        res = []
        if self.desc is not None:
            if case == '' or not do_case:
                outp = ''
            else:
                outp = 'Case %s: ' % case
                do_case = False
            # outp += self.desc % {'force':force, 'force_point': ', '.join([ str(i+1) for i,x in enumerate(force.force) if x ])}
            outp += self.desc % {'force':force}
            res.append('\n'.join([ pad + line for line in outp.split('\n') ]))
        curc = 0
        one_case = len(self.cases) == 1 or not self.is_and
        for c in range(len(self.cases)):
            if not self.is_and and force not in self.cases[c].force:
                # print self.cases[c].force & force
                continue

            if one_case:
                res.append(self.cases[c]._output(case, indent, force, do_case))
            else:
                if curc != 0:
                    res.append(pad + '    ----------')
                res.append(self.cases[c]._output(case + ('' if case == '' else '.') + '%d' % (curc+1), indent+1, force, True))
                curc += 1

            if one_case:
                # res.append('%s, %s' % (self.cases[c].force, force))
                break

        return ''.join( s + '\n' for s in res ).rstrip('\n')

    def __str__(self):
        # use_force = TSAForce.none()
        # for i in range(len(self.force)):
        #     if self.force[i]:
        #         use_force = TSAForce([ set([ list(self.force[i])[0] ]) if i == j else set() for j in range(len(self.force)) ])
        #         break
        if not self.force:
            return 'FAIL'
        try:
            use_force = list(self.force.force)[0]
        except:
            use_force = ((),())
        return self._output('', 0, use_force, False).rstrip()

# COUNTER = 0
# OUTPUT = False

class TSA:
    def __init__(self, p, q, depth, multbox=True, q_check=True, force_len=None, knowledge=None):
        if force_len is None: force_len = len(p)
        # TODO: clean up
        # TODO: assertions

        # if q.mesh <= p.mesh:
        #     p,q = q,p
        # assert p.mesh <= q.mesh
        # add = q.mesh - p.mesh
        # assert len(add) == 1

        assert p.pattern == q.pattern
        self.p = p
        self.q = q
        # self.shade = list(add)[0]
        self.cut = False
        self.mx_size = len(self.p) + depth
        self.k = len(p.pattern)
        self.multbox = multbox
        self.q_check = q_check
        self.force_len = force_len
        if not knowledge:
            # self.knowledge = ([shad_to_binary(self.q.shading, self.k + 1)], [shad_to_binary(self.p.shading, self.k + 1)])
            self.knowledge = set([shad_to_binary(self.q.shading, self.k + 1)])
        else:
            self.knowledge = set(knowledge)

    def do_empty_boxes(self, boxes, mp, *args):
        if len(boxes) == 1:
            desc = None
        else:
            desc = 'Now we have %d case(s)' % len(boxes)

        cases = []
        possforce = TSAForce.all()
        all = True
        shaded = set()
        for pi in boxes:
            res = self.init_dfs(mp.shade(shaded), pi, *args)

            possforce &= res.force
            if not possforce:
                break

            # if res.res != TSAResult.CONTRADICTION:
            #     all = False
            #     break
            shaded.add(pi)
            cases.append(res)

        if not possforce:
            return TSAResult(possforce)
        return TSAResult(possforce, cases=cases, is_and=True)

        # if all:
        #     return TSAResult.contradiction(desc, cases)
        # return TSAResult.no_contradiction()

    def add_point(self, mp, xyval, putin, d):
        xval, yval = xyval
        nxt = mp.add_point(putin,d)
        # INDEX CHANGE
        # TODO: Why is this needed?
        # xval = [0] + xval + [self.k+1]
        # yval = [0] + yval + [self.k+1]
        xval = [-1] + xval + [self.k]
        yval = [-1] + yval + [self.k]
        xval = xval[1:putin[0]+1] + [(xval[putin[0]]+xval[putin[0]+1])/2.0] + xval[putin[0]+1:-1]
        yval = yval[1:putin[1]+1] + [(yval[putin[1]]+yval[putin[1]+1])/2.0] + yval[putin[1]+1:-1]
        return (nxt, (xval, yval))

    def init_dfs(self, mp, putin, force, xyval, seen):

        # if putin contains no points, then we're done
        # otherwise, it contains at least one point
        possforce = TSAForce.none()
        cases = []
        for d in DIRS:
            # choose the east/north/west/south-most point

            # if len(mp) == 3 and d != 2: continue

            nxt, nxtxyval = self.add_point(mp, xyval, putin, d)
            res = self.dfs(nxt, force, nxtxyval, seen)

            if not res.force:
                continue

            possforce |= res.force
            cases.append(TSAResult(res.force, desc='Choose the %s point in %s' % (STR_ADJ[d], putin), cases=[res]))

            if force == res.force:
                # Early exit since there's nothing more to discover
                break

            # if res.res == TSAResult.CONTRADICTION:
            #     return 

        if not possforce:
            return TSAResult(possforce)
        return TSAResult(possforce, cases=cases, is_and=False)
        # return TSAResult.no_contradiction()

    def dfs(self, mp, force, xyval, seen):
        xval, yval = xyval

        # if OUTPUT:
        #     print '-------------------------'
        #     print '-------------------------'

        # print mp

        desc0 = 'Now we have the permutation:\n%s'.format(mp)

        possforce = TSAForce.none()
        cases = []
        for occ in choose(len(xval), self.k):

            # if len(mp) == 3 and occ != [0,1,2]: continue
            # if len(mp) == 4 and occ != [0,1,2]: continue
            # if len(mp) == 5 and occ != [0,1,2]: continue
            # if len(mp) == 4 and occ != [0,1,2]: continue

            subperm = [ mp.pattern[occ[i]] for i in range(self.k) ]
            subxval = sorted([ xval[occ[i]] for i in range(self.k) ])
            subyval = sorted([ yval[subperm[i]] for i in range(self.k) ])
            subperm = Perm.to_standard(subperm)

            if tuple(subxval) in seen:
                continue

            nseen = set(list(seen))
            nseen.add(tuple(subxval))
            if not (subperm == self.p.pattern):
                continue

            sub = mp.sub_mesh_pattern(occ)

            desc1 = desc0 + '\nWe choose the subsequence at indices %s and get the pattern:\n%s' % (occ, sub)

            subbinshad = shad_to_binary(sub.shading, self.k + 1)
            pbinshad = shad_to_binary(self.p.shading, self.k + 1)
            # if self.q_check and any(is_subset(k, subbinshad) for k in self.knowledge[0]):
            # if self.q_check and any(is_subset(k, subbinshad) for k in self.knowledge):
            if self.q_check and subbinshad in self.knowledge:
                desc2 = desc1 + '\nThis is an instance of a pattern implying the occurrence of the objective pattern q.'
                return TSAResult(force, desc=desc2)
            # if self.q_check and self.q.shading <= sub.shading:
                # desc2 = desc1 + '\nThis is an instance of the objective pattern q.'
                # return TSAResult(force, desc=desc2)


            next_steps = [ (True, self.p.shading - sub.shading) ]
            if self.q_check or len(mp) == self.k:
                next_steps.append((False, self.q.shading - sub.shading))

            for (p_occ, adds) in next_steps:

                if p_occ:

                    # Use the force, Luke
                    forceprime = force & TSAForce.from_sub(subperm, subxval, subyval, self.force_len)

                    # global COUNTER
                    # global OUTPUT
                    # COUNTER += 1
                    #
                    # if COUNTER == 58:
                    #     OUTPUT = True
                    # OUTPUT = len(mp) <= 3
                    #
                    # if OUTPUT:
                    #     print ''
                    #     print COUNTER
                    #     print mp
                    #     print occ, p_occ, adds
                    #     print sub
                    #     print force
                    #     print forceprime
                    #     print subperm
                    #     print subxval
                    #     print subyval
                    #     print TSAForce.from_sub(subperm, subxval, subyval, self.force_len)
                    #     print ''

                    if not forceprime:
                        # if OUTPUT: print 'aaaaa'
                        continue

                    if len(adds) == 0:
                        # desc2 = desc1 + '\nThis is another instance of p where the point (%d,%d) is more to the %s, which means this branch leads to a contradiction.' % (force[0]+1, self.p.perm[force[0]], STR_ADJ2[force[1]])
                        desc2 = desc1 + '\nThis is another instance of p with higher force = %(force)s, which means this branch leads to a contradiction.' # % forceprime
                        # if OUTPUT: print 'bbbbb'
                        return TSAResult(forceprime, desc=desc2)
                else:
                    forceprime = force

                    if len(adds) == 0:
                        desc2 = desc1 + '\nThis is an instance of the objective pattern q.'
                        # if OUTPUT: print 'ccccc'
                        return TSAResult(force, desc=desc2)

                if len(mp) >= self.mx_size:
                    # We can't afford inserting more points :'(
                    # if OUTPUT: print 'ddddd'
                    continue

                boxes = set()
                inside = False
                for add in adds:
                    # INDEX CHANGE
                    # txval = [0] + subxval + [self.k+1]
                    # tyval = [0] + subyval + [self.k+1]
                    # left,right = txval[add[0]], txval[add[0]+1]
                    # down,up = tyval[add[1]], tyval[add[1]+1]
                    txval = [-1] + subxval + [self.k]
                    tyval = [-1] + subyval + [self.k]
                    left,right = txval[add[0]], txval[add[0]+1]
                    down,up = tyval[add[1]], tyval[add[1]+1]

                    # left,right = ([0]+xval+[self.k+1]).index(left), ([0]+xval+[self.k+1]).index(right)
                    # down,up = ([0]+yval+[self.k+1]).index(down), ([0]+yval+[self.k+1]).index(up)
                    left,right = ([-1]+xval+[self.k]).index(left), ([-1]+xval+[self.k]).index(right)
                    down,up = ([-1]+yval+[self.k]).index(down), ([-1]+yval+[self.k]).index(up)

                    for x in range(left,right):
                        for y in range(down,up):
                            if (x,y) not in mp.shading:
                                boxes.add((x,y))
                    for x in range(left, right-1):
                        if down < mp.pattern[x] < up:
                            inside = True
                            break
                    if inside:
                        break
                if inside:
                    # if OUTPUT: print 'eeeee'
                    continue

                if not self.multbox and len(boxes) > 1:
                    continue

                # if OUTPUT:
                #     print 'boxes ^ = %s' % boxes
                #     print 'mp ^ = %s' % mp
                #     print 'adds ^ = %s' % adds
                #     print 'subxval ^ = %s' % subxval
                #     print 'subyval ^ = %s' % subyval

                # assert len(boxes) > 0

                # desc2 = desc1 + '\nWe need to worry about the non-shaded boxes %s in this sub-pattern, which correspond to %s in the current permutation' % (adds, boxes)
                desc2 = desc1 + '\nConsider the non-shaded boxes %s in this sub-pattern, which correspond to %s in the current permutation' % (adds, boxes)
                if p_occ:
                    desc2 += '\nIf they\'re empty, then we\'ve found another instance of p satisfying blaa'
                else:
                    desc2 += '\nIf they\'re empty, then we\'ve found an instance of q'
                desc2 += '\nOtherwise we have a few cases:'

                # if COUNTER == 58:
                #     OUTPUT = False

                res = self.do_empty_boxes(boxes, mp, forceprime, xyval, nseen)

                if not res.force:
                    continue

                possforce |= res.force
                cases.append(TSAResult(res.force, desc=desc2, cases=[res]))

            #     if forceprime == res.force:
            #         # Early exit because there's nothing more we can discover
            #         break
            # if forceprime == res.force:
            #     # Early exit because there's nothing more we can discover
            #     break

        if not possforce:
            return TSAResult(possforce)
        return TSAResult(possforce, cases=cases, is_and=False)

    def run_specific(self, force):

        # assert self.shade not in self.p.mesh

        # res = self.init_dfs(self.p, self.shade, force, ([ i+1 for i in range(self.k) ], [ i+1 for i in range(self.k) ]), set([tuple(self.p.perm.perm)]))
        # res = self.init_dfs(self.p, self.shade, force, ([ i+1 for i in range(self.k) ], [ i+1 for i in range(self.k) ]), set([tuple([ i for i in range(1,self.k+1) ])]))
        # INDEX CHANGE
        # res = self.dfs(self.p, force, ([ i+1 for i in range(self.k) ], [ i+1 for i in range(self.k) ]), set())
        res = self.dfs(self.p, force, ([ i for i in range(self.k) ], [ i for i in range(self.k) ]), set())
        return res

    def tsa5(self):
        desc = 'The input patterns are:\n\n%s\n\n' % (splice(' p =\n'+str(self.p), ' q =\n'+str(self.q)))
        # desc += 'They differ by: %s\n' % str(self.shade)
        # desc += 'We consider the occurence of the pattern p where the point at index %(force_point)s is the %(force)s\n'
        desc += 'We consider the occurence of the pattern p where %(force)s\n'
        res = self.run_specific(TSAForce.all())
        return TSAResult(res.force, desc=desc, cases=[res])
        # for i in range(self.k):
        #     for d in range(4):
        #         res = self.run_specific((i,d))
        #         if res.res == TSAResult.CONTRADICTION:
        #             return TSAResult.contradiction('Choose the occurrence of the pattern p where the point (%d,%d) is %s' % (i+1, self.p.perm[i], STR_ADJ[d]), [res])
        # return TSAResult.no_contradiction()

    def run(self):
        ress = []

        ress.append(self.tsa5())

        return ress

def tsa5_two(mp1, mp2, depth, multbox=True, q_check=True, force_len=None, knowledge=None):
    tsa = TSA(mp1, mp2, depth, multbox=multbox, q_check=q_check, force_len=force_len, knowledge=knowledge)
    return tsa.run()

def tsa5(mp, shade, depth, multbox=True, q_check=True, force_len=None, knowledge=None):
    return tsa5_two(mp, mp.shade(shade), depth, multbox=multbox, q_check=q_check, force_len=force_len)

def tsa5_implies(mp1, mp2, depth, multbox=True, q_check=True, force_len=None, knowledge=None):
    run = tsa5_two(mp1, mp2, depth, multbox=multbox, q_check=q_check, force_len=force_len, knowledge=knowledge)
    for r in run:
        if bool(r.force):
            return True
    return False

def tsa5_coincident(mp1, mp2, depth, multbox=True, q_check=True, force_len=None, knowledge=(None, None)):
    res = []
    run = tsa5_two(mp1, mp2, depth, multbox=multbox, q_check=q_check, force_len=force_len, knowledge=knowledge[0])
    res.extend(run)
    run = tsa5_two(mp2, mp1, depth, multbox=multbox, q_check=q_check, force_len=force_len, knowledge=knowledge[1])
    res.extend(run)
    for r in res:
        if not bool(r.force):
            return False
    return True

if __name__ == '__main__':

    run = tsa5_two(MeshPatt.unrank(Perm((0,1,2)), 8), MeshPatt.unrank(Perm((0,1,2)), 34923), depth=1, multbox=True, q_check=True, force_len=3)

    for line in run:
        print(line)
    import sys
    sys.exit(0)


# [1 2] PATTERNS

    # 2-comp
    # run = tsa5_two(MeshPatt(Perm([0,1]), [(0,1),(0,2),(1,1),(1,2),(2,0)]), MeshPatt(Perm([0,1]), [(0,2),(1,0),(1,1),(2,0),(2,1)]), 2)
    run = tsa5_two(MeshPatt.unrank(Perm([0,1]), 118), MeshPatt.unrank(Perm([0,1]), 220), depth=1, force_len=2)
    # run = TSA(MeshPatt(Perm([1,2]), [(0,1),(0,2),(1,1),(1,2),(2,0)]), MeshPatt(Perm([1,2]), [(0,2),(1,0),(1,1),(2,0),(2,1)]), 2).run()
    # run = TSA(MeshPatt(Perm([1,2]), [(0,2),(1,0),(1,1),(2,0),(2,1)]), MeshPatt(Perm([1,2]), [(0,1),(0,2),(1,1),(1,2),(2,0)]), 2).run()
    # run = tsa5(MeshPatt(Perm([0,1]), [(0,2),(1,0),(1,1),(2,0),(2,1)]), MeshPatt(Perm([0,1]), [(0,1),(0,2),(1,1),(1,2),(2,0)]), 2, True, True, 1)
    # run = tsa5(MeshPatt.unrank((0,1), 9), (2,1), depth=1, multbox=False, q_check=False, force_len=1)
    # run = tsa5(MeshPatt.unrank((0,1), 1), (1,0), depth=1, multbox=False, q_check=False, force_len=1)
    # print(run)
    for line in run:
        print(line)
    import sys
    sys.exit(0)


# [1 2 3] PATTERNS

    # run = tsa5(MeshPatt(Perm([1]), [(1,1)]), (0,1), 5)

    #C1
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), 3)
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), (1, 3),  3)

    #C2
    # mp1 = MeshPatt(Perm([0,1,2]), [(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)])
    # mp2 = mp1.shade((2,1))
    # run = TSA(mp1, mp2, 3).run()
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), 3)

    #C5
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,1),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), 3)

    # ---------------------------------------------------------------------------- #

    #C8
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,3),(1,0),(1,1),(1,2),(2,0),(2,2),(3,0)]), (2,3), 3)

    #C9
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(0,3),(1,0),(1,1),(1,2),(2,0),(2,2),(3,0)]), (2,3), 5)

    #C14
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(1,0),(1,1),(2,3),(3,0),(3,1),(3,2),(3,2),(3,3)]), (2,1), 3)

    # C15
    # C16

    # ---------------------------------------------------------------------------- #

    # C17
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(1,1),(1,3),(2,1),(2,2),(2,3),(3,0),(3,3)]), (1,0), 3)

    # C18
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(1,1),(1,3),(2,1),(2,2),(2,3),(3,0)]), (1,0), 3)

    # ---------------------------------------------------------------------------- #

    # C19
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(1,0),(1,3),(2,1),(3,0)]), (3,3), 4)

    # C20
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(1,3),(2,1),(3,0)]), (3,3), 5)

    # ---------------------------------------------------------------------------- #

    # C21
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(0,1),(1,1),(2,1),(2,2),(3,0)]), (3,2), 3)

    # C22
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(1,0),(1,1),(2,1),(2,2),(3,0)]), (3,2), 5)

    # C23
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(1,1),(2,1),(2,2),(3,0)]), (3,2), 3)

    # ---------------------------------------------------------------------------- #

    # C24
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(1,1),(2,1),(2,2),(2,3),(3,0),(3,3)]), (1,0), 3)

    # ---------------------------------------------------------------------------- #

    # C25
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(1,0),(1,1),(1,2),(2,3),(3,0)]), (3,3), 100, 1)

    # C26
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(1,1),(1,2),(2,3),(3,0)]), (3,3), 6)

    # C27
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(1,2),(2,3),(3,0)]), (3,3), 6)

    # C28
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(1,2),(2,3),(3,0)]), (3,3), 100, 1)

    # C29
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(1,1),(1,2),(2,3),(3,0)]), (3,3), 4)

    # ---------------------------------------------------------------------------- #

    # C30 This is a chain
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(1,0),(1,1),(2,3),(3,0)]), (2,1), 3)
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(1,0),(1,1),(2,1),(2,3),(3,0)]), (3,3), 4)

    # ---------------------------------------------------------------------------- #

    # C31
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(1,1),(2,1),(2,2),(2,3),(3,0)]), (1,0), 4)

    # ---------------------------------------------------------------------------- #

    # C32
    #run = tsa5(MeshPatt(Perm([0,1,2]), [(0,1),(1,2),(2,2),(3,0),(3,3)]), (0,0), 5)

    # C33
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,1),(1,2),(2,2),(3,0),(3,2),(3,3)]), (0,0), 6)

    # C34
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,1),(1,2),(3,0),(3,3)]), (0,0), 6)

    # C35
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,1),(1,2),(2,2),(3,0)]), (0,0), 4)

    # C36
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,1),(1,2),(3,0)]), (0,0), 4)

    # ---------------------------------------------------------------------------- #

    # ---------------------------------------------------------------------------- #

    # C37
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,1),(1,1),(2,1),(2,2),(3,0)]), (3,2), 6)

    # ---------------------------------------------------------------------------- #

    # C38 This is a chain
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,1),(2,2),(3,0),(3,2),(3,3)]), (2,1), 6)
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,1),(2,1),(2,2),(3,0),(3,2),(3,3)]), (0,0), 6)


    # C85
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(1, 2), (3, 3), (2, 3), (2, 2), (0, 3), (1, 1)]), (0,1), 5)


    # ---------------------------------------------------------------------------- #
    # run = tsa5(MeshPatt(Perm((0,1,2)), [(1,2), (2,3), (3,0)]), (3,3), 2)

    # ---------------------------------------------------------------------------- #

    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1), 3)
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (1,1))
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(1,0),(1,3),(2,1),(3,0)]), (3,3))
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,1),(1,0),(2,0),(2,2),(3,0),(3,2),(3,3)]), (2,1))
    # run = tsa5(MeshPatt(Perm([0,1,2]), [(0,0),(1,0),(1,1),(2,3),(3,0),(3,1)]), (2,1))

    # print("\n================================================================================\n".join(['\n'.join(i) for i in run]))
    # print("\nTotal number of successful branches: {}\n".format(len(run)))

# [1 3 2] PATTERNS

    # C6_3
    # run = tsa5(MeshPatt(Perm([0,2,1]), [(0, 1), (1, 3), (2, 3), (0, 2)]), (1,1), 2)

    # C32
    # run = tsa5(MeshPatt(Perm([0,2,1]), [(0,1),(1,0),(3,2)]), (1,1), 5)

    # C34
    #run = tsa5(MeshPatt(Perm([0,2,1]), [(0,1),(1,0),(1,2),(1,3),(2,2),(3,2)]), (1,1), 100000)

    # C35
    #run = tsa5(MeshPatt(Perm([0,2,1]), [(0,1),(1,0),(2,2)]), (1,1), 2)

    # C36
    # run = tsa5(MeshPatt(Perm([0,2,1]), [(0,1),(1,0)]), (1,1), 2)

    # C39
    #run = tsa5(MeshPatt(Perm([0,2,1]), [(0,1),(1,0),(2,2),(2,3)]), (1,1), 5)

    # C39
    #run = tsa5(MeshPatt(Perm([0,2,1]), [(0,1),(1,0),(2,2),(2,3)]), (1,1), 10)

    # C69
    # run = tsa5(MeshPatt(Perm([0,2,1]), [(3, 0), (0, 3), (2, 3), (1, 0), (2, 2)]), (3,2), 4)

    # C85
    # run = tsa5(MeshPatt(Perm([0,2,1]), [(0, 1), (1, 2), (0, 0), (2, 1), (0, 3)]), (1, 3), 6)


    # run = tsa5(MeshPatt(Perm([0,2,1]), [(0,1),(0,2),(1,0),(1,3),(2,0),(3,1)]), (1,1), 2)

    #run = tsa5(MeshPatt(Perm([0,2,1]), []),(0,0), 100)

    # if run.res == TSAResult.CONTRADICTION:
    all = True
    for r in run:
        all = all and bool(r.force)
    if all:
        print()
        for r in run:
            print(r)
            print()
    else:
        print('Noooooooooo')

# mp1 = MeshPatt(Perm([1,2]), set())
# mp2 = MeshPatt(Perm([1,2]), set([(1,2), (2,1)]))
# res = tsa5_two(mp1, mp2, 1, False, False, 1)
# print res

