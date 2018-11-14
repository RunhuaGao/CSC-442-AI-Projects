# Prior sample utility function
from RandomVariables import rv
from EnumerateInference import net1, net2, net3


def priorsample(bayesnet):
    event = {}
    for node in bayesnet.nodes:
        event[node.name] = node.sample(event)
    return event


def rejectionsample(query, event, bayesnet, N):
    """
    :param query: the query variable
    :param event: the evidence
    :param bayesnet: the baysnet
    :param N: do N times sampling
    :return: the normalized probability distribution by sampling
    """
    distribute = {status: 0 for status in bayesnet[query].domain}
    for _ in range(N):
        sample = priorsample(bayesnet)
        if consistent(sample, event):
            distribute[sample[query]] += 1
    rv.normalize(distribute)
    return distribute


def consistent(sample, event):
    """
    :param sample: a sample produced by prior sample
    :param event:  a event that happens
    :return: if the sample generated consistent with event
    """
    for key, value in event.items():
        if sample.get(key, value) != value:
            return False
    return True


k = rejectionsample("A", {"B": True, "E": False}, net1, 50000)
print(k)