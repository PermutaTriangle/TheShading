
# TODO:
#   - Strongly connected component
#   - Graph datastructure for classes

import sys
import argparse
from itertools import *
from collections import deque

from permuta import MeshPatt, Perm
from tsa5_eq import tsa5_two as tsa5

underlying_classical_pattern = None

def subset_coincidence(mpatt1, mpatt2):
    return mpatt1.shading <= mpatt2.shading

def shading_lemma(mpatt1, mpatt2):
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(mpatt1.shading) > len(mpatt2.shading):
        mpatt1, mpatt2 = mpatt2, mpatt1
    if len(symdiff) != 1:
        return False
    return mpatt1.can_shade(symdiff.pop())

def tsa5_wrapper(mpatt1, mpatt2, depth):
    if len(mpatt1.shading) > len(mpatt2.shading):
        return False
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(symdiff) != 1:
        return False
    run = tsa5(mpatt1, symdiff.pop())
    all = True
    for r in run:
        all = all and bool(r.force)

    return all

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

    def compute_coinc(self, coincpred, coincargs=(), oneway=True):
        for i in range(self.len):
            for j in range(self.len):

                to = self.implies(i, j)
                fro = self.implies(j, i)

                if to:
                    continue

                mpatt1, mpatt2 = self.patts[i], self.patts[j]

                coinc = coincpred(mpatt1, mpatt2, *coincargs)

                if coinc:
                    self.add_edge(self.pattrank[i], self.pattrank[j], None)
                    if not oneway and not fro:
                        self.add_edge(self.pattrank[j], self.pattrank[i], None)

    def output_class(self):
        res = [str(self.pattrank)]
        if len(self.scc()) == 1:
            res.append("inactive")
        else:
            res.append("active")
        for i in range(self.len):
            for j in sorted(self.adj[i]):
                res.append("{} {}".format(self.pattrank[i], self.pattrank[j[0]]))
        return '\n'.join(res)

def parse_classes(inputfile):
    lines = list(l.strip() for l in dropwhile(lambda x: len(x.strip()) == 0 or x.strip()[0] == "#", inputfile.readlines()))
    linenum = 0

    global underlying_classical_pattern
    underlying_classical_pattern = Perm(eval(lines[linenum].strip()))

    linenum += 1
    while linenum < len(lines):
        assert(lines[linenum][0] == '[' and lines[linenum][-1] == ']')
        assert(lines[linenum+1] == 'active' or lines[linenum+1] == 'inactive')
        curclass = ExpClass(eval(lines[linenum]), underlying_classical_pattern, lines[linenum+1] == 'active')
        linenum += 2
        while linenum < len(lines):
            if lines[linenum][0] == '[':
                break
            u, v = lines[linenum].split()
            curclass.add_edge(int(u), int(v), None)
            linenum += 1
        yield curclass

def main(argv):
    parser = argparse.ArgumentParser(description='Classify mesh patterns.')
    parser.add_argument("input_file", type=argparse.FileType('r'))
    parser.add_argument( '-sl', '--shading-lemma', action='store_true', help="Use the Shading Lemma", dest='sl')
    parser.add_argument( '-tsa1', '--tsa1', help='TSA1 depth', nargs=1, type=int, default=0)
    parser.add_argument( '-tsa2', '--tsa2', help='TSA2 depth', nargs=1, type=int, default=0)
    parser.add_argument( '-tsa3', '--tsa3', help='TSA3 depth', nargs=1, type=int, default=0)
    parser.add_argument( '-tsa4', '--tsa4', help='TSA4 depth', nargs=1, type=int, default=0)
    parser.add_argument( '-tsa5', '--tsa5', help='TSA5 depth', nargs=1, type=int, default=0)

    args = parser.parse_args()
    output = [None]

    for clas in parse_classes(args.input_file):

        if clas.active:
            clas.compute_coinc(subset_coincidence)

            if args.sl:
                clas.compute_coinc(shading_lemma, oneway=False)
            if args.tsa5:
                clas.compute_coinc(tsa5_wrapper, args.tsa5, True)

        res = clas.output_class()
        output.append(res)
    output[0] = str(underlying_classical_pattern)

    sys.stdout.write('\n'.join(output))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

