import glob
import os

arr = [
    'tsa2_simple',
    'tsa2_nonsimple',
    'tsa3_simple',
    'tsa3_nonsimple',
]

res = {}

for d in arr:
    for path in glob.glob('./%s/C*' % d):
    # for path in glob.glob('./%s/C*_132_*' % d):
        name = os.path.basename(path)
        success = None
        err = False
        for depath in glob.glob('%s/depth*.txt' % path):
            depth = int(os.path.basename(depath).split('_')[1].split('.')[0])
            with open(depath, 'r') as f:
                txt = f.read()
            ans = txt.split('\n')[0]
            # print name, depth, ans
            if ans == 'SUCCESS':
                if success is not None:
                    success = min(success, depth)
                else:
                    success = depth
            elif ans != 'FAIL':
                err = True
        # print name, (success if success else 'FAIL')
        res.setdefault(name, {})
        res[name][d] = success if success else ('ERROR' if err else 'FAIL')

for k,v in sorted(res.items(), key=lambda x: (x[0].split('_')[1], x)):
    perm = k.split('_')[1]
    num = k.split('_')[0]
    no = k.split('_')[2]
    print perm, ('%s_%s' % (num,no)).ljust(7), ' '.join([ str(v[t]).rjust(10) for t in arr ])

