def readfile(filename):
    file = open(filename)
    str = file.readlines()
    res = [s.strip().split(',') for s in str]
    for data in res:
        data[-1] = data[-1].split("-")[1]
    return res
