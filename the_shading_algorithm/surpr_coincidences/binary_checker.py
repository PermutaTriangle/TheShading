# coding: utf-8
import sys

from collections import Counter
from permuta import *
from permuta.misc import ProgressBar, factorial
from misc import shad_to_binary, is_subset
perm_set = None

def filter_binary(patterns, cpatt):
    binarypatterns = set(patterns)
    for l in range(len(cpatt), len(cpatt) * 2 + 1):
        sys.stderr.write("Permutations of length {}\n".format(l))
        ProgressBar.create(factorial(l))
        for perm in perm_set.of_length(l):
            ProgressBar.progress()
            poss = []
            for res in cpatt.occurrences_in(perm):
                con = set(perm[i] for i in res)
                colcnt = 0
                col = [-1]*len(perm)
                for v in perm:
                    if v in con:
                        colcnt += 1
                    else:
                        col[v] = colcnt
                rowcnt = 0
                row = [-1]*len(perm)
                for v in range(len(perm)):
                    if v in con:
                        rowcnt += 1
                    else:
                        row[v] = rowcnt
                # bad is the set of boxes that contain points and can not be shaded
                bad = set( (u,v) for u,v in zip(col,row) if u != -1 )
                # cur is the set of boxes that can be shaded
                cur = set( (u,v) for u in range(len(cpatt)+1) for v in range(len(cpatt)+1) if (u,v) not in bad )
                poss.append(shad_to_binary(cur, len(cpatt) + 1))

            occurring = set()
            nonbinary = set()
            for binpatt in binarypatterns:
                for occ in poss:
                    if is_subset(binpatt, occ):
                        if binpatt in occurring:
                            nonbinary.add(binpatt)
                            # print(MeshPatt.unrank(cpatt, binpatt))
                            # print(perm)
                            break
                        else:
                            occurring.add(binpatt)
            binarypatterns -= nonbinary
        ProgressBar.finish()

    return binarypatterns


################################################################################

# pattern_ranks = [0, 1, 2, 3, 16, 17, 32, 33, 34, 35, 48, 49, 64, 65, 66, 67, 80, 81, 96, 97, 98, 99, 112, 113, 512, 513, 514, 515, 528, 529, 544, 545, 546, 547, 560, 561, 1024, 1025, 1026, 1027, 1040, 1041, 1056, 1057, 1058, 1059, 1072, 1073, 1088, 1089, 1090, 1091, 1104, 1105, 1120, 1121, 1122, 1123, 1136, 1137, 1536, 1537, 1538, 1539, 1552, 1553, 1568, 1569, 1570, 1571, 1584, 1585, 2048, 2049, 2050, 2051, 2064, 2065, 2080, 2081, 2082, 2083, 2096, 2097, 2112, 2113, 2114, 2115, 2128, 2129, 2144, 2145, 2146, 2147, 2160, 2161, 2560, 2561, 2562, 2563, 2576, 2577, 2592, 2593, 2594, 2595, 2608, 2609, 3072, 3073, 3074, 3075, 3088, 3089, 3104, 3105, 3106, 3107, 3120, 3121, 3136, 3137, 3138, 3139, 3152, 3153, 3168, 3169, 3170, 3171, 3184, 3185, 3584, 3585, 3586, 3587, 3600, 3601, 3616, 3617, 3618, 3619, 3632, 3633, 16384, 16385, 16386, 16387, 16400, 16401, 16416, 16417, 16418, 16419, 16432, 16433, 16448, 16449, 16450, 16451, 16464, 16465, 16480, 16481, 16482, 16483, 16496, 16497, 16896, 16897, 16898, 16899, 16912, 16913, 16928, 16929, 16930, 16931, 16944, 16945, 17408, 17409, 17410, 17411, 17424, 17425, 17440, 17441, 17442, 17443, 17456, 17457, 17472, 17473, 17474, 17475, 17488, 17489, 17504, 17505, 17506, 17507, 17520, 17521, 17920, 17921, 17922, 17923, 17936, 17937, 17952, 17953, 17954, 17955, 17968, 17969, 32768, 32769, 32770, 32771, 32784, 32785, 32800, 32801, 32802, 32803, 32816, 32817, 32832, 32833, 32834, 32835, 32848, 32849, 32864, 32865, 32866, 32867, 32880, 32881, 33280, 33281, 33282, 33283, 33296, 33297, 33312, 33313, 33314, 33315, 33328, 33329, 33792, 33793, 33794, 33795, 33808, 33809, 33824, 33826, 33840, 33856, 33857, 33858, 33859, 33872, 33873, 33888, 33890, 33904, 34304, 34305, 34306, 34307, 34320, 34321, 34336, 34338, 34352, 34816, 34817, 34818, 34819, 34832, 34833, 34848, 34849, 34850, 34851, 34864, 34865, 34880, 34881, 34882, 34883, 34896, 34897, 34912, 34913, 34914, 34915, 34928, 34929, 35328, 35329, 35330, 35331, 35344, 35345, 35360, 35361, 35362, 35363, 35376, 35377, 35840, 35841, 35842, 35843, 35856, 35857, 35872, 35874, 35888, 35904, 35905, 35906, 35907, 35920, 35921, 35936, 35938, 35952, 36352, 36353, 36354, 36355, 36368, 36369, 36384, 36386, 36400, 49152, 49153, 49154, 49155, 49168, 49169, 49184, 49185, 49186, 49187, 49200, 49201, 49216, 49217, 49218, 49219, 49232, 49233, 49248, 49249, 49250, 49251, 49264, 49265, 49664, 49665, 49666, 49667, 49680, 49681, 49696, 49697, 49698, 49699, 49712, 49713, 50176, 50177, 50178, 50179, 50192, 50193, 50208, 50210, 50224, 50240, 50241, 50242, 50243, 50256, 50257, 50272, 50274, 50288, 50688, 50689, 50690, 50691, 50704, 50705, 50720, 50722, 50736]
# cpatt = Perm((0, 1, 2))

################################################################################

cpatt = Perm(map(int, list(sys.argv[1])))
avoidance = []
if len(sys.argv) > 2:
    # avoidance = [ Perm(map(int, p)) for p in map(list, sys.argv[2].split())]
    avoidance = [ Perm(map(int, p)) for p in map(list, sys.argv[2:]) ]
perm_set = PermSet.avoiding(avoidance)
pattern_ranks = [ i for i in range(2**((len(cpatt) + 1)**2)) ]

################################################################################

internal_check = False
external_check = False
print_clas = True
binarypatterns = filter_binary(pattern_ranks, cpatt)

if internal_check:
    for patt in binarypatterns:
        for length in range(len(cpatt), len(cpatt) * 2 + 2):
            for perm in perm_set.of_length(length):
                if perm.count_occurrences_of(MeshPatt.unrank(cpatt, patt)) > 1:
                    print("INTERNAL FAAAAAAAAAAAAAAAAAAAAAIIIIIIIIIIIIIIIIIIIIIIIIILLLLLLLLLLLLLLL")
                    print(MeshPatt.unrank(cpatt, patt))
                    sys.exit(1)
if external_check:
    for mpatt in gen_meshpatts(len(cpatt), cpatt):
        if mpatt.rank() in binarypatterns:
            continue
        if all(perm.count_occurrences_of(mpatt) == 1 for length in range(len(cpatt), len(cpatt) * 2 + 2) for perm in perm_set.of_length(length)):
            print("EXTERNAL FAAAAAAAAAAAAAAAAAAAAAIIIIIIIIIIIIIIIIIIIIIIIIILLLLLLLLLLLLLLL")
            print(MeshPatt.unrank(cpatt, mpatt))
            sys.exit(1)

if print_clas:
    sys.stdout.write("0\n")

# print(sorted(binarypatterns))
sys.stdout.write('\n'.join(map(str, binarypatterns)) + '\n')
# for patt in sorted(binarypatterns):
#     print(MeshPatt.unrank(cpatt, patt))
#     print()
