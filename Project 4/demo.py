from math import e
from random import shuffle


def sigmoid(x):
    return 1 / (1 + e ** (-x))


def sigmoidd(x):
    return x * (1 - x)


def loss(output, target):
    return (output - target) ** 2


studyrate = 0.3

import numpy as np


class OutputNode:
    def __init__(self, size):
        self.weights = np.random.rand(1, size)
        self.size = size

    def updateweight(self, targetvalue, data):
        actual = self.output(data)
        for i in range(self.size):
            deltaWeight = (targetvalue - actual) * sigmoidd(actual) * data[i]
            self.weights[0, i] += studyrate * deltaWeight

    def output(self, data):
        currdata = np.array(data[:self.size])
        return sigmoid(np.sum(currdata * self.weights))


from DataParser import continuousIris

# shuffle(continuousIris)
Nodes = [OutputNode(4), OutputNode(4), OutputNode(4)]
for i in range(len(continuousIris)):
    if continuousIris[i][-1] == "setosa":
        continuousIris[i][-1] = [1, 0, 0]
    elif continuousIris[i][-1] == "versicolor":
        continuousIris[i][-1] = [0, 1, 0]
    else:
        continuousIris[i][-1] = [0, 0, 1]
