with open('bla2.txt', 'r') as f:
    for line in f.readlines():
        print(sorted(eval(line.strip())))
