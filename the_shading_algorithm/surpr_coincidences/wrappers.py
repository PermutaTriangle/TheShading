from permuta import MeshPatt, Perm
from functools import partial
import sys
import os

from tsa1 import all_points_all_dir as tsa1
from tsa2 import all_points_all_dir as tsa2
from tsa3 import tsa3
from tsa4 import tsa4
from tsa5_knowledge import tsa5_two as tsa5
from tsa5_knowledge import tsa5_coincident, tsa5_implies
# from tsa5_eq import tsa5_coincident
# from classify import ExpClass

def subset_pred(mpatt1, mpatt2, expclass=None):
    return mpatt1.shading >= mpatt2.shading

def shading_lemma(mpatt1, mpatt2, expclass=None):
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(mpatt1.shading) > len(mpatt2.shading):
        mpatt1, mpatt2 = mpatt2, mpatt1
    if len(symdiff) != 1:
        return False
    return mpatt1.can_shade(symdiff.pop())

def simulshading_lemma(mpatt1, mpatt2, expclass=None):
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(mpatt1.shading) > len(mpatt2.shading):
        mpatt1, mpatt2 = mpatt2, mpatt1
    if len(symdiff) > 2:
        return False
    if len(symdiff) == 1:
        return mpatt1.can_shade(symdiff.pop())
    else:
        return mpatt1.can_simul_shade(symdiff.pop(), symdiff.pop())

# def tsa123_wrapper(tsa, mpatt1, mpatt2, depth):
#     symdiff = set(mpatt1.shading ^ mpatt2.shading)
#     if len(mpatt1.shading) > len(mpatt2.shading):
#         mpatt1, mpatt2 = mpatt2, mpatt1
#     if len(symdiff) != 1:
#         return False
#     return bool(tsa(mpatt1, symdiff.pop(), depth))

def tsa1_wrapper(mpatt1, mpatt2, depth, expclass=None):
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(mpatt1.shading) > len(mpatt2.shading):
        mpatt1, mpatt2 = mpatt2, mpatt1
    if len(symdiff) != 1:
        return False
    return tsa5_coincident(mpatt1, mpatt2, depth=depth, multbox=False, q_check=False, force_len=1)

def lemma5_wrapper(mpatt1, mpatt2, expclass=None):
    # if len(mpatt1.shading) > len(mpatt2.shading):
        # mpatt1, mpatt2 = mpatt2, mpatt1
    return tsa5_coincident(mpatt1, mpatt2, depth=1, multbox=True, q_check=False, force_len=None)

tsa1_pred = tsa1_wrapper
lemma5_pred = lemma5_wrapper
# tsa2_pred = partial(tsa123_wrapper, tsa2)
# tsa3_pred = partial(tsa123_wrapper, tsa3)

def tsa4_pred(tsa, mpatt1, mpatt2, depth, expclass=None):
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(mpatt1.shading) > len(mpatt2.shading):
        mpatt1, mpatt2 = mpatt2, mpatt1
    if len(symdiff) != 1:
        return False
    run = tsa1(mpatt1, symdiff.pop(), depth)
    return bool(run.force)

def lemma7_pred(mpatt1, mpatt2, expclass, expclasses, depth, force_len, prooflog=None):
    if not force_len:
        force_len = len(mpatt1)
    else:
        force_len = force_len[0]
    run = tsa5_implies(mpatt1, mpatt2, depth=depth[0], multbox=True, q_check=True, force_len=min(force_len, len(mpatt1)), knowledge=expclasses)
    if bool(run):
        if prooflog:
            try:
                with open(os.path.join(prooflog[0], "{}_{}_proof.txt".format(mpatt1.rank(), mpatt2.rank())), 'w+') as f:
                    for r in run:
                        f.write(str(r))
                        f.write('\n')
                    f.flush()
            except:
                sys.stderr.write("Failed to open a file in proof directory {}".format(str(prooflog)))
                sys.stderr.write('\n')
    return bool(run)
    # return tsa5_coincident(mpatt1, mpatt2, depth=1, multbox=True, q_check=True, force_len=len(mpatt1))

def tsa5_pred(mpatt1, mpatt2, depth, expclass=None):
    # if len(mpatt1.shading) > len(mpatt2.shading):
        # return False
    # symdiff = set(mpatt1.shading ^ mpatt2.shading)
    # if len(symdiff) != 1:
        # return False
    # run = tsa5_coincidence(mpatt1, symdiff.pop(), depth)
    # all = True
    # for r in run:
        # all = all and bool(r.force)

    return tsa5_coincidence(mpatt1, mpatt2, depth=depth, )
    # return all
