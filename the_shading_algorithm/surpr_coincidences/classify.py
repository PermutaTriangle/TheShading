
# TODO:
#   - Strongly connected component
#   - Graph datastructure for classes

import sys
from itertools import *
from collections import deque

from permuta import MeshPatt, Perm

def subset_coincidence(mpatt1, mpatt2):
    return mpatt1.shading <= mpatt2.shading

def shading_lemma(mpatt1, mpatt2):
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(mpatt1.shading) > len(mpatt2.shading):
        mpatt1, mpatt2 = mpatt2, mpatt1
    if len(symdiff) != 1:
        return False
    return mpatt1.can_shade(symdiff.pop())

class ExpClass(object):
    def __init__(self, patts, classical_pattern, active):
        self.idmap = dict()
        self.pattrank = patts
        self.adj = [ [] for _ in range(len(patts)) ]
        self.patts = [ MeshPatt.unrank(classical_pattern, n) for n in patts ]
        self.len = len(patts)
        self.active = active
        for patt in patts:
            if patt not in self.idmap:
                self.idmap[patt] = len(self.idmap)
            else:
                msg = "Element twice in class list: {}".format(patt)
                raise ValueError(msg)

    def __repr__(self):
        return self.pattrank.__repr__()

    def __str__(self):
        return self.pattrank.__str__()

    def __len__(self):
        return self.len

    def add_edge(self, mpatt1, mpatt2, edgetype):
        self.adj[self.idmap[mpatt1]].append((self.idmap[mpatt2], edgetype))

    def dfs(self, root, adj):
        stack = deque()
        stack.append(root)
        visited = set()
        visited.add(root)
        while len(stack):
            cur = stack.pop()
            visited.add(cur)
            for (nbr, etype) in adj[cur]:
                if nbr not in visited:
                    visited.add(nbr)
                    stack.append(nbr)
        return visited

    def scc(self):
        rev = [ [] for i in range(len(self)) ]
        for u in range(len(self)):
            for (v,t) in self.adj[u]:
                rev[v].append((u,t))
        visited = set()
        L = []
        def visit(u):
            visited.add(u)
            for (v,t) in self.adj[u]:
                if v not in visited:
                    visit(v)
            L.append(u)
        for u in range(len(self)):
            if u not in visited:
                visit(u)
        visited.clear()
        # return len(dfs(L[0])) == self.len
        L.reverse()
        stack = []
        components = []
        for v in L:
            if v not in visited:
                comp = self.dfs(v, rev)
                visited |= comp
                components.append(list(comp))
        return components

    def implies(self, i, j):
        return j in self.dfs(i, self.adj)

    def compute_coinc(self, coincpred, oneway=True):
        for i in range(self.len):
            for j in range(i + 1, self.len):

                to, fro = self.implies(i, j), self.implies(j, i)

                if to and fro:
                    continue

                mpatt1, mpatt2 = self.patts[i], self.patts[j]

                coinc = coincpred(mpatt1, mpatt2)

                if oneway:
                    if coinc:
                        self.add_edge(self.pattrank[i], self.pattrank[j], None)
                    if not fro:
                        if coincpred(mpatt2, mpatt1):
                            self.add_edge(self.pattrank[j], self.pattrank[i], None)
                elif coinc:
                    if not to:
                        self.add_edge(self.pattrank[i], self.pattrank[j], None)
                    if not fro :
                        self.add_edge(self.pattrank[j], self.pattrank[i], None)

    def output_class(self):
        res = str(self.pattrank) + '\n'
        if len(self.scc()) == 1:
            res += "inactive\n"
        else:
            res += "active\n"
        for i in range(self.len):
            for j in self.adj[i]:
                res += "{} {}\n".format(self.pattrank[i], self.pattrank[j[0]])
        return res

def parse_classes(filename):
    with open(filename, 'r') as f:

        lines = list(l.strip() for l in dropwhile(lambda x: len(x.strip()) == 0 or x.strip()[0] == "#", f.readlines()))
        linenum = 0
        classes = []

        classical_pattern = Perm(eval(lines[linenum].strip()))
        # classical_pattern = Perm((0, 1, 2))
        # print(classical_pattern)
        linenum += 1
        while linenum < len(lines):
            assert(lines[linenum][0] == '[' and lines[linenum][-1] == ']')
            assert(lines[linenum+1] == 'active' or lines[linenum+1] == 'inactive')
            curclass = ExpClass(eval(lines[linenum]), classical_pattern, lines[linenum+1] == 'active')
            linenum += 2
            while linenum < len(lines) and lines[linenum][0] != '[':
                assert(lines[linenum][0] == '[' and lines[linenum][-1] == ']')
                u, v = lines[linenum].split()
                curclass.add_edge(int(u), int(v))
                linenum += 1
            yield curclass
            classes.append(curclass)
        # yield (classical_pattern, classes)

def main(argv):
    if len(argv) != 2:
        sys.stderr.write('usage: %s input_file\n' % argv[0])
        return 1

    # classes = parse_classes(argv[1])

    for clas in parse_classes(argv[1]):
        # if(len(clas) == 1):
        #     continue
        # print(clas)
        if clas.active:
            clas.compute_coinc(subset_coincidence)
            clas.compute_coinc(shading_lemma, False)
        res = clas.output_class()
        sys.stdout.write(res)
        # for i in range(len(clas)):
        #     print("{}:".format(clas.pattrank[i]))
        #     print(str(clas.patts[i]))
        #     print()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

