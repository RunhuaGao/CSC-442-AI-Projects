# example file 1
from xmlParser import parseFile, files
from xmlParser import rv


def enumerate(queryvariable, evidence, bayesnet):
    # make sure query not in evidence
    assert queryvariable not in evidence
    Q = dict()
    for i in bayesnet[queryvariable].domain:
        Q[i] = enumerateall(bayesnet.nodes, extend(evidence, queryvariable, i))
    rv.normalize(Q)
    return Q


def enumerateall(vars, evidence):
    if not vars:
        return 1
    else:
        first, rest = vars[0], vars[1:]
        if first.name in evidence:
            value = evidence[first.name]
            return first.calProba(value, evidence) * enumerateall(rest, evidence)
        else:
            summation = 0
            for value in first.domain:
                summation += first.calProba(value, evidence) * enumerateall(rest, extend(evidence, first.name, value))
            return summation


def extend(original, variable, value):
    result = original.copy()
    result[variable] = value
    return result


def normalize(iterablevalue):
    return 0


net1 = parseFile(files[0])
net2 = parseFile(files[1])
net3 = parseFile(files[2])
