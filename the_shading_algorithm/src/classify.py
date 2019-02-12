import sys
import argparse
from itertools import product, chain, dropwhile
from collections import deque
import graphviz

from permuta import MeshPatt, Perm
from misc import is_subset
from wrappers import (subset_pred,
                      shading_lemma,
                      tsa1_pred,
                      lemma5_pred,
                      lemma7_pred)

underlying_classical_pattern = None


class ExpClasses(object):
    def __init__(self, classes):
        self.classes = classes
        self.clasmap = dict()
        for (i, clas) in enumerate(classes):
            for patt in clas.pattrank:
                self.clasmap[patt] = i

    def implies(self, p, q):
        pclass = self.clasmap[p]
        visited = self.classes[pclass].dfs(self.classes[pclass].idmap[p],
                                           self.classes[pclass].adj)
        return any(is_subset(q, self.classes[pclass].pattrank[r])
                   for r in visited)


class ExpClass(object):
    def __init__(self, patts, classical_pattern, active):
        self.idmap = dict()
        self.pattrank = patts
        self.adj = [[] for _ in range(len(patts))]
        self.patts = [MeshPatt.unrank(classical_pattern, n) for n in patts]
        self.len = len(patts)
        self.active = active
        for patt in patts:
            if patt not in self.idmap:
                self.idmap[patt] = len(self.idmap)
            else:
                msg = "Element twice in class list: {}".format(patt)
                raise ValueError(msg)

    def __repr__(self):
        return "ExpClass({})".format(self.pattrank.__repr__())

    def __str__(self):
        return "ExpClass({})".format(self.pattrank.__str__())

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
        rev = [[] for i in range(len(self))]
        for u in range(len(self)):
            for (v, t) in self.adj[u]:
                rev[v].append((u, t))
        visited = set()
        L = []

        def visit(u):
            visited.add(u)
            for (v, t) in self.adj[u]:
                if v not in visited:
                    visit(v)
            L.append(u)
        for u in range(len(self)):
            if u not in visited:
                visit(u)
        visited.clear()
        L.reverse()
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

                coinc = coincpred(mpatt1, mpatt2, self, *coincargs)

                if coinc:
                    self.add_edge(self.pattrank[i], self.pattrank[j], None)
                    if not oneway and not fro:
                        self.add_edge(self.pattrank[j], self.pattrank[i], None)

    def compute_coinc_SSL(self):
        for i in range(self.len):
            patt = self.patts[i]
            boxes = patt.shadable_boxes()
            for key in boxes.keys():
                boxes[key].append(tuple())
            for sh in product(*boxes.values()):
                coincwith = patt.shade(k for k in chain(*sh) if k).rank()
                if coincwith not in self.idmap:
                    sys.stdout.write(str(self) + '\n')
                    sys.stdout.write(
                        "The pattern {} is not in the expclass.\n")
                    sys.stdout.write("\n" + str(patt) + "\n")
                    sys.stdout.write("\n" + str(coincwith) + "\n")
                if not self.implies(i, self.idmap[coincwith]):
                    self.add_edge(self.pattrank[i], coincwith, None)
                if not self.implies(self.idmap[coincwith], i):
                    self.add_edge(coincwith, self.pattrank[i], None)

    def output_class(self):
        res = [str(self.pattrank)]
        if len(self.scc()) == 1:
            res.append("inactive")
        else:
            res.append("active")
        for i in range(self.len):
            for j in sorted(self.adj[i]):
                res.append("{} {}".format(
                    self.pattrank[i], self.pattrank[j[0]]))
        return '\n'.join(res)

    def graphviz(self):
        dot = graphviz.Digraph(comment="active" if self.active else "inactive")
        for patt in self.pattrank:
            dot.node(str(patt))
        for patt in self.pattrank:
            for edge in self.adj[self.idmap[patt]]:
                dot.edge(str(patt), str(self.pattrank[edge[0]]))
        return dot


def parse_classes(inputfile):
    lines = list(l.strip() for l in dropwhile(
        lambda x: len(x.strip()) == 0 or x.strip()[0] == "#",
        inputfile.readlines()))
    linenum = 0

    global underlying_classical_pattern
    underlying_classical_pattern = Perm(eval(lines[linenum].strip()))

    linenum += 1
    while linenum < len(lines):
        assert(lines[linenum][0] == '[' and lines[linenum][-1] == ']')
        assert(lines[linenum+1] == 'active' or lines[linenum+1] == 'inactive')
        curclass = ExpClass(eval(lines[linenum]),
                            underlying_classical_pattern,
                            lines[linenum+1] == 'active')
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
    parser.add_argument('-sl', '--shading-lemma', action='store_true',
                        help="Use the Shading Lemma", dest='sl')
    parser.add_argument('-ssl', '--simultaneous-shading-lemma',
                        action='store_true',
                        help="Use the Simultaneous Shading Lemma", dest='ssl')
    parser.add_argument('-lemma2', '--lemma2', help='Lemma 2',
                        action='store_true')
    parser.add_argument('-lemma5', '--lemma5', help='Lemma 5',
                        action='store_true')
    parser.add_argument('-lemma7', '--lemma7', help='Lemma 7 depth', nargs=1,
                        type=int, default=0)
    parser.add_argument('-proof', '--proof',
                        help='Directory for proof outputs', nargs=1, type=str)
    parser.add_argument('-fl', '--force_len', help='Number of force points',
                        nargs=1, type=int)

    args = parser.parse_args()
    output = [None]

    sys.stderr.write("Starting with parameters {}\n".format(args))

    lem7 = []

    for clas in parse_classes(args.input_file):

        if clas.active:
            clas.compute_coinc(subset_pred)

            if args.sl:
                clas.compute_coinc(shading_lemma, oneway=False)
            if args.ssl:
                clas.compute_coinc_SSL()
            if args.lemma2:
                clas.compute_coinc(tsa1_pred, [1], oneway=False)
            if args.lemma5:
                clas.compute_coinc(lemma5_pred, [], oneway=False)

        if args.lemma7:
            lem7.append(clas)
        else:
            res = clas.output_class()
            output.append(res)

    output[0] = str(underlying_classical_pattern)

    if args.lemma7:
        lem7classes = ExpClasses(lem7)
        for clas in lem7:
            clas.compute_coinc(lemma7_pred, oneway=True,
                               coincargs=(lem7classes, args.lemma7,
                                          args.force_len, args.proof))
            output.append(clas.output_class())

    sys.stdout.write('\n'.join(output))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
