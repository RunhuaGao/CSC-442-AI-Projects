from random import choice
from EnumerateInference import extend, net1, net2, net3
from RandomVariables import rv, probability


def gibbssampling(query, evidence, bayesnet, N):
    assert query not in evidence
    counts = {x: 0 for x in bayesnet[query].domain}
    Z = [r.name for r in bayesnet.nodes if r.name not in evidence]
    state = dict(evidence)
    for z in Z:
        state[z] = choice(bayesnet[z].domain)
    for _ in range(N):
        for z in Z:
            state[z] = markovsample(z, state, bayesnet)
            counts[state[query]] += 1
    rv.normalize(counts)
    return query, counts


def markovsample(query, evidence, bayesnet):
    centralnode = bayesnet[query]
    Q = {}
    for value in bayesnet[query].domain:
        currevent = extend(evidence, query, value)
        markovchainProb = [node.calProba(currevent[node.name], currevent) for node in centralnode.childNodes]
        Q[value] = centralnode.calProba(value, evidence) * calProduct(markovchainProb)
    rv.normalize(Q)
    return probability(Q[True])


def calProduct(nums):
    result = 1
    for num in nums:
        result *= num
    return result


a, b = gibbssampling("dog-out", {"bowel-problem": True, "family-out": True}, net3, 25000)
print(b)
