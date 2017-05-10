import sys
from permuta import *
from misc import *

# 0 1
# mpatts = [0, 1, 2, 3, 8, 9, 16, 17, 18, 19, 24, 25, 32, 33, 34, 35, 40, 41, 48, 49, 50, 51, 56, 57, 128, 129, 130, 131, 136, 137, 144, 145, 146, 147, 152, 153, 256, 257, 258, 259, 264, 265, 272, 274, 280, 288, 289, 290, 291, 296, 297, 304, 306, 312, 384, 385, 386, 387, 392, 393, 400, 402, 408]

# 0 1 2
# mpatts = [0, 1, 2, 3, 16, 17, 32, 33, 34, 35, 48, 49, 64, 65, 66, 67, 80, 81, 96, 97, 98, 99, 112, 113, 512, 513, 514, 515, 528, 529, 544, 545, 546, 547, 560, 561, 1024, 1025, 1026, 1027, 1040, 1041, 1056, 1057, 1058, 1059, 1072, 1073, 1088, 1089, 1090, 1091, 1104, 1105, 1120, 1121, 1122, 1123, 1136, 1137, 1536, 1537, 1538, 1539, 1552, 1553, 1568, 1569, 1570, 1571, 1584, 1585, 2048, 2049, 2050, 2051, 2064, 2065, 2080, 2081, 2082, 2083, 2096, 2097, 2112, 2113, 2114, 2115, 2128, 2129, 2144, 2145, 2146, 2147, 2160, 2161, 2560, 2561, 2562, 2563, 2576, 2577, 2592, 2593, 2594, 2595, 2608, 2609, 3072, 3073, 3074, 3075, 3088, 3089, 3104, 3105, 3106, 3107, 3120, 3121, 3136, 3137, 3138, 3139, 3152, 3153, 3168, 3169, 3170, 3171, 3184, 3185, 3584, 3585, 3586, 3587, 3600, 3601, 3616, 3617, 3618, 3619, 3632, 3633, 16384, 16385, 16386, 16387, 16400, 16401, 16416, 16417, 16418, 16419, 16432, 16433, 16448, 16449, 16450, 16451, 16464, 16465, 16480, 16481, 16482, 16483, 16496, 16497, 16896, 16897, 16898, 16899, 16912, 16913, 16928, 16929, 16930, 16931, 16944, 16945, 17408, 17409, 17410, 17411, 17424, 17425, 17440, 17441, 17442, 17443, 17456, 17457, 17472, 17473, 17474, 17475, 17488, 17489, 17504, 17505, 17506, 17507, 17520, 17521, 17920, 17921, 17922, 17923, 17936, 17937, 17952, 17953, 17954, 17955, 17968, 17969, 32768, 32769, 32770, 32771, 32784, 32785, 32800, 32801, 32802, 32803, 32816, 32817, 32832, 32833, 32834, 32835, 32848, 32849, 32864, 32865, 32866, 32867, 32880, 32881, 33280, 33281, 33282, 33283, 33296, 33297, 33312, 33313, 33314, 33315, 33328, 33329, 33792, 33793, 33794, 33795, 33808, 33809, 33824, 33826, 33840, 33856, 33857, 33858, 33859, 33872, 33873, 33888, 33890, 33904, 34304, 34305, 34306, 34307, 34320, 34321, 34336, 34338, 34352, 34816, 34817, 34818, 34819, 34832, 34833, 34848, 34849, 34850, 34851, 34864, 34865, 34880, 34881, 34882, 34883, 34896, 34897, 34912, 34913, 34914, 34915, 34928, 34929, 35328, 35329, 35330, 35331, 35344, 35345, 35360, 35361, 35362, 35363, 35376, 35377, 35840, 35841, 35842, 35843, 35856, 35857, 35872, 35874, 35888, 35904, 35905, 35906, 35907, 35920, 35921, 35936, 35938, 35952, 36352, 36353, 36354, 36355, 36368, 36369, 36384, 36386, 36400, 49152, 49153, 49154, 49155, 49168, 49169, 49184, 49185, 49186, 49187, 49200, 49201, 49216, 49217, 49218, 49219, 49232, 49233, 49248, 49249, 49250, 49251, 49264, 49265, 49664, 49665, 49666, 49667, 49680, 49681, 49696, 49697, 49698, 49699, 49712, 49713, 50176, 50177, 50178, 50179, 50192, 50193, 50208, 50210, 50224, 50240, 50241, 50242, 50243, 50256, 50257, 50272, 50274, 50288, 50688, 50689, 50690, 50691, 50704, 50705, 50720, 50722, 50736]

# 0 2 1
mpatts = [0, 2, 4, 6, 16, 18, 20, 22, 32, 34, 36, 38, 48, 50, 52, 54, 64, 68, 80, 84, 96, 100, 112, 116, 256, 258, 260, 262, 272, 274, 276, 278, 288, 290, 304, 306, 320, 324, 336, 340, 352, 368, 512, 514, 516, 518, 544, 546, 548, 550, 576, 580, 608, 612, 768, 770, 772, 774, 800, 802, 832, 836, 864, 1024, 1026, 1028, 1030, 1040, 1042, 1044, 1046, 1056, 1058, 1060, 1062, 1072, 1074, 1076, 1078, 1088, 1092, 1104, 1108, 1120, 1124, 1136, 1140, 1280, 1282, 1284, 1286, 1296, 1298, 1300, 1302, 1312, 1314, 1328, 1330, 1344, 1348, 1360, 1364, 1376, 1392, 1536, 1538, 1540, 1542, 1568, 1570, 1572, 1574, 1600, 1604, 1632, 1636, 1792, 1794, 1796, 1798, 1824, 1826, 1856, 1860, 1888, 2048, 2050, 2052, 2054, 2064, 2066, 2068, 2070, 2080, 2082, 2084, 2086, 2096, 2098, 2100, 2102, 2112, 2116, 2128, 2132, 2144, 2148, 2160, 2164, 2304, 2306, 2308, 2310, 2320, 2322, 2324, 2326, 2336, 2338, 2352, 2354, 2368, 2372, 2384, 2388, 2400, 2416, 2560, 2562, 2564, 2566, 2592, 2594, 2596, 2598, 2624, 2628, 2656, 2660, 2816, 2818, 2820, 2822, 2848, 2850, 2880, 2884, 2912, 3072, 3074, 3076, 3078, 3088, 3090, 3092, 3094, 3104, 3106, 3108, 3110, 3120, 3122, 3124, 3126, 3136, 3140, 3152, 3156, 3168, 3172, 3184, 3188, 3328, 3330, 3332, 3334, 3344, 3346, 3348, 3350, 3360, 3362, 3376, 3378, 3392, 3396, 3408, 3412, 3424, 3440, 3584, 3586, 3588, 3590, 3616, 3618, 3620, 3622, 3648, 3652, 3680, 3684, 3840, 3842, 3844, 3846, 3872, 3874, 3904, 3908, 3936, 16384, 16386, 16388, 16390, 16400, 16402, 16404, 16406, 16416, 16418, 16420, 16422, 16432, 16434, 16436, 16438, 16448, 16452, 16464, 16468, 16480, 16484, 16496, 16500, 16640, 16642, 16644, 16646, 16656, 16658, 16660, 16662, 16672, 16674, 16688, 16690, 16704, 16708, 16720, 16724, 16736, 16752, 16896, 16898, 16900, 16902, 16928, 16930, 16932, 16934, 16960, 16964, 16992, 16996, 17152, 17154, 17156, 17158, 17184, 17186, 17216, 17220, 17248, 17408, 17410, 17412, 17414, 17424, 17426, 17428, 17430, 17440, 17442, 17444, 17446, 17456, 17458, 17460, 17462, 17472, 17476, 17488, 17492, 17504, 17508, 17520, 17524, 17664, 17666, 17668, 17670, 17680, 17682, 17684, 17686, 17696, 17698, 17712, 17714, 17728, 17732, 17744, 17748, 17760, 17776, 17920, 17922, 17924, 17926, 17952, 17954, 17956, 17958, 17984, 17988, 18016, 18020, 18176, 18178, 18180, 18182, 18208, 18210, 18240, 18244, 18272, 32768, 32770, 32772, 32774, 32784, 32786, 32788, 32790, 32800, 32802, 32804, 32806, 32816, 32818, 32820, 32822, 32832, 32836, 32848, 32852, 32864, 32868, 32880, 32884, 33024, 33026, 33028, 33030, 33040, 33042, 33044, 33046, 33056, 33058, 33072, 33074, 33088, 33092, 33104, 33108, 33120, 33136, 33280, 33282, 33284, 33286, 33312, 33314, 33316, 33318, 33344, 33348, 33376, 33380, 33536, 33538, 33540, 33542, 33568, 33570, 33600, 33604, 33632, 34816, 34818, 34820, 34822, 34832, 34834, 34836, 34838, 34848, 34850, 34852, 34854, 34864, 34866, 34868, 34870, 34880, 34884, 34896, 34900, 34912, 34916, 34928, 34932, 35072, 35074, 35076, 35078, 35088, 35090, 35092, 35094, 35104, 35106, 35120, 35122, 35136, 35140, 35152, 35156, 35168, 35184, 35328, 35330, 35332, 35334, 35360, 35362, 35364, 35366, 35392, 35396, 35424, 35428, 35584, 35586, 35588, 35590, 35616, 35618, 35648, 35652, 35680, 49152, 49154, 49156, 49158, 49168, 49170, 49172, 49174, 49184, 49186, 49188, 49190, 49200, 49202, 49204, 49206, 49216, 49220, 49232, 49236, 49248, 49252, 49264, 49268, 49408, 49410, 49412, 49414, 49424, 49426, 49428, 49430, 49440, 49442, 49456, 49458, 49472, 49476, 49488, 49492, 49504, 49520, 49664, 49666, 49668, 49670, 49696, 49698, 49700, 49702, 49728, 49732, 49760, 49764, 49920, 49922, 49924, 49926, 49952, 49954, 49984, 49988, 50016]

sys.stdin.readline()
binary = set(map(int, sys.stdin.readline().split()))

res = []
for i in mpatts:
    if i in binary:
        res.append(i)
print(res)
