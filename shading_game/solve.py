import sys
sys.argv[1]

def solve_123_1():
    print 's'
    print '1 3 4'

    print 'e'
    print '1 4 5'

    # #
    # print 's'
    # print '4 5 6'
    # print '5 1'
    #
    # print 'e'
    # print '4 6 7'
    #
    # #
    # print 's'
    # print '6 7 8'
    # print '7 1'
    #
    # print 'e'
    # print '6 8 9'

    at = 4
    while True:
        print 's'
        print at, at+1, at+2
        print at+1, 1
        print 'e'
        print at,at+2,at+3
        at += 2

def solve_123_2():
    print 's'
    print '1 3 4'
    print 'e'
    print '1 4 5'
    print 's'
    print '4 5 6'
    print '5 1'

    at = 4
    while True:
        print 'e'
        print at,at+2,at+3
        print 's'
        print at+2, at+3, at+4
        at += 2

def solve_123_3():
    print 's'
    print '1 2 4'
    print 's'
    print '1 4 5'

    at = 4
    while True:
        print 's'
        print at,at+1,at+2
        print at+1,1
        print 's'
        print at,at+2,at+3
        at += 2

def solve_123_4():
    print 's'
    print '1 3 4'
    print 'e'
    print '1 4 5'

    at = 4
    while True:
        print 's'
        print at,at+1,at+2
        print at+1,1
        print 'e'
        print at,at+2,at+3
        at += 2

def solve_123_5():
    print 's'
    print '1 2 4'
    print 's'
    print '1 4 5'
    print 's'

    at = 4
    while True:
        print at,at+1,at+2
        print at+1, 1
        print 's'
        print at,at+2,at+3
        print 's'
        at += 2

eval('solve_' + sys.argv[1] + '()')

