from math import e
from random import shuffle


def sigmoid(x):
    return 1 / (1 + e ** (-x))


def sigmoidd(x):
    return x * (1 - x)


def loss(output, target):
    return (output - target) ** 2


studyrate = 0.01

import numpy as np
import random


class OutputNode:
    def __init__(self, size):
        self.weights = np.random.rand(1, size)
        self.bias = random.uniform(0, 1)
        self.size = size

    def updateweight(self, targetvalue, data):
        actual = self.output(data)
        deltaWeight = (targetvalue - actual) * sigmoidd(actual)
        for i in range(self.size):
            self.weights[0, i] += studyrate * deltaWeight * data[i]
            self.bias += deltaWeight * studyrate

    def output(self, data):
        currdata = np.array(data)
        return sigmoid(np.sum(currdata * self.weights) + self.bias)

    def setinitial(self):
        self.weights = np.random.rand(1, self.size)
        self.bias = random.uniform(0, 1)


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

normalizedIris = continuousIris.copy()
for i in range(len(continuousIris[0]) - 1):
    cols = [d[i] for d in continuousIris]
    minvalue, maxvalue = min(cols), max(cols)
    length = maxvalue
    for d in normalizedIris:
        d[i] = (d[i] - minvalue) / length


def test(i):
    testnode = Nodes[i]
    shuffle(continuousIris)
    for d in continuousIris:
        data, target = d[:-1], d[-1][i]
        testnode.updateweight(target, data)

    for d in continuousIris:
        data, target = d[:-1], d[-1][i]
        out = testnode.output(data)
        print("Predcit result is : ", out)
        print("Actual is:", target)


def train(times, dataset):
    for _ in range(times):
        shuffle(dataset)
        for d in dataset:
            data, target = d[:-1], d[-1]
            for i in range(len(Nodes)):
                Nodes[i].updateweight(target[i], data)
    shuffle(dataset)
    count = 0
    for d in dataset:
        data, target = d[:-1], d[-1]
        output = [node.output(data) for node in Nodes]

        pre = np.argmax(output) + 1
        actual = np.argmax(target) + 1
        if pre != actual: count += 1
        # print("Predicted type is: ",pre)
        # print("Actual type is: ",actual)
    print('Error number is: ', count)
    [node.setinitial() for node in Nodes]
    return count


train(1000, normalizedIris)
