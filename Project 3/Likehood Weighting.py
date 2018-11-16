from EnumerateInference import net1, net2, net3
from RandomVariables import rv


def likehoodweighting(query, evidence, baysnet, N):
    """
    :param query: query variable, str
    :param baysnet: baysnet, from xmlfile
    :param N: sample times
    :return: the normalized probability distribution in bayesnet based on query and evidence
    """
    W = {x: 0 for x in baysnet[query].domain}
    for _ in range(N):
        sample, proba = weightedsample(baysnet, evidence)
        W[sample[query]] += proba
    rv.normalize(W)
    return W


def weightedsample(bayesnet, evidence):
    w = 1
    event = dict(evidence)
    for node in bayesnet.nodes:
        if node.name in evidence:
            w = w * node.calProba(evidence[node.name], evidence)
        else:
            event[node.name] = node.sample(event)
    return event, w


c = likehoodweighting("E", {}, net1, 25000)
print(c)
