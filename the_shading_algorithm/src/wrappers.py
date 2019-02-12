import sys
import os

from tsa5_knowledge import tsa5_coincident, tsa5_implies


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


def tsa1_pred(mpatt1, mpatt2, depth, expclass=None):
    symdiff = set(mpatt1.shading ^ mpatt2.shading)
    if len(mpatt1.shading) > len(mpatt2.shading):
        mpatt1, mpatt2 = mpatt2, mpatt1
    if len(symdiff) != 1:
        return False
    return tsa5_coincident(mpatt1, mpatt2, depth=depth, multbox=False,
                           q_check=False, force_len=1)


def lemma5_pred(mpatt1, mpatt2, expclass=None):
    return tsa5_coincident(mpatt1, mpatt2, depth=1, multbox=True,
                           q_check=False, force_len=None)


def lemma7_pred(mpatt1, mpatt2, expclass, expclasses, depth, force_len,
                prooflog=None):
    if not force_len:
        force_len = len(mpatt1)
    else:
        force_len = force_len[0]
    run = tsa5_implies(mpatt1, mpatt2, depth=depth[0], multbox=True,
                       q_check=True, force_len=min(force_len, len(mpatt1)),
                       knowledge=expclasses)
    if bool(run):
        if prooflog:
            try:
                with open(os.path.join(prooflog[0], "{}_{}_proof.txt".format(
                        mpatt1.rank(), mpatt2.rank())), 'w+') as f:
                    for r in run:
                        f.write(str(r))
                        f.write('\n')
                    f.flush()
            except Exception:
                sys.stderr.write(
                    "Failed to open a file in proof directory {}".format(
                        str(prooflog)))
                sys.stderr.write('\n')
    return bool(run)
