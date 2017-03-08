from permuta import MeshPatt, Perm
from functools import partial

from tsa1 import all_points_all_dir as tsa1
from tsa2 import all_points_all_dir as tsa2
from tsa3 import tsa3
from tsa4 import tsa4
from tsa5_eq import tsa5_two as tsa5
from tsa5_eq import tsa5_coincident

def subset_pred(mpatt1, mpatt2):
    return mpatt1.shading >= mpatt2.shading

def shading_lemma(mpatt1, mpatt2):
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(mpatt1.shading) > len(mpatt2.shading):
        mpatt1, mpatt2 = mpatt2, mpatt1
    if len(symdiff) != 1:
        return False
    return mpatt1.can_shade(symdiff.pop())

def simulshading_lemma(mpatt1, mpatt2):
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(mpatt1.shading) > len(mpatt2.shading):
        mpatt1, mpatt2 = mpatt2, mpatt1
    if len(symdiff) > 2:
        return False
    if len(symdiff) == 1:
        return mpatt1.can_shade(symdiff.pop())
    else:
        return mpatt1.can_simul_shade(symdiff.pop(), symdiff.pop())

def tsa123_wrapper(tsa, mpatt1, mpatt2, depth):
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(mpatt1.shading) > len(mpatt2.shading):
        mpatt1, mpatt2 = mpatt2, mpatt1
    if len(symdiff) != 1:
        return False
    return bool(tsa(mpatt1, symdiff.pop(), depth))

def tsa1_wrapper(mpatt1, mpatt2, depth):
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(mpatt1.shading) > len(mpatt2.shading):
        mpatt1, mpatt2 = mpatt2, mpatt1
    if len(symdiff) != 1:
        return False
    return tsa5_coincident(mpatt1, mpatt2, depth=depth, multbox=False, q_check=False, force_len=1)

tsa1_pred = tsa1_wrapper
tsa2_pred = partial(tsa123_wrapper, tsa2)
tsa3_pred = partial(tsa123_wrapper, tsa3)

def tsa4_pred(tsa, mpatt1, mpatt2, depth):
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(mpatt1.shading) > len(mpatt2.shading):
        mpatt1, mpatt2 = mpatt2, mpatt1
    if len(symdiff) != 1:
        return False
    run = tsa1(mpatt1, symdiff.pop(), depth)
    return bool(run.force)

def tsa5_pred(mpatt1, mpatt2, depth):
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
