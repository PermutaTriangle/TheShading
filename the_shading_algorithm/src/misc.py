def shad_to_binary(shading, length):
    res = 0
    for (x, y) in shading:
        res |= 1 << (x * length + y)
    return res

def is_subset(a, b):
    return (a & ~b) == 0
