# example file 1
from xmlParser import rv
from RunProgram import processInput
import sys

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
                summation += first.calProba(value, evidence) * enumerateall(rest,
                                                                extend(evidence, first.name, value))
            return summation


def extend(original, variable, value):
    result = original.copy()
    result[variable] = value
    return result

if __name__ == "__main__":
    net,query,evidence = processInput(sys.argv)
    distribution = enumerate(query,evidence,net)
    print(distribution)
