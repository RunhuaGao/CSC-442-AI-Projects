import csv


def readfile(filename):
    file = open(filename)
    str = file.readlines()
    res = [s.strip().split(',') for s in str]
    for data in res:
        if "-" in data[-1]: data[-1] = data[-1].split("-")[1]
    return res


def readconFile(filename):
    file = open(filename)
    str = file.readlines()
    res = [s.strip().split(',') for s in str]
    for data in res:
        data[-1] = data[-1].split("-")[1]
        for i in range(len(data) - 1):
            data[i] = float(data[i])
    return res


continuousIris = readconFile("iris.data.txt")
