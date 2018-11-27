# Prior sample utility function
from RandomVariables import rv
from RunProgram import processInput
import sys

def priorsample(bayesnet):
    event = {}
    for node in bayesnet.nodes:
        event[str(node.name)] = node.sample(event)
    return event


def rejectionsample(query, evidence, bayesnet, N):
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
        if consistent(sample, evidence):
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
        if sample[key]!=value:return False
    return True



if __name__ == "__main__":
    defaultN = 25000
    net,query,evidence = processInput(sys.argv)
    distribution = rejectionsample(query,evidence,net,defaultN)
    print(distribution)
