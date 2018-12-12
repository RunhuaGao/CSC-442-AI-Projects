import numpy as np
import random
from math import e
from random import shuffle
from DataParser import continuousIris, normalizedIris

# default study rate
studyrate = 0.01

# process normalizedIris dataset
for i in range(len(continuousIris[0]) - 1):
    cols = [d[i] for d in continuousIris]
    minvalue, maxvalue = min(cols), max(cols)
    length = maxvalue - minvalue
    for d in normalizedIris:
        d[i] = (eval(d[i]) - minvalue) / length


def assignvector(examples):
    for i in range(len(examples)):
        if examples[i][-1] == "setosa":
            examples[i][-1] = [1, 0, 0]
        elif examples[i][-1] == "versicolor":
            examples[i][-1] = [0, 1, 0]
        else:
            examples[i][-1] = [0, 0, 1]


assignvector(continuousIris)
assignvector(normalizedIris)


def sigmoid(x):
    return 1 / (1 + e ** (-x))


def sigmoidd(x):
    return x * (1 - x)


class OutputNode:
    def __init__(self, size, studyrate):
        self.weights = np.random.rand(1, size)
        self.bias = random.uniform(0, 1)
        self.size = size
        self.studyrate = studyrate

    def updateweight(self, targetvalue, data):
        actual = self.output(data)
        deltaWeight = (targetvalue - actual) * sigmoidd(actual)
        for i in range(self.size):
            self.weights[0, i] += self.studyrate * deltaWeight * data[i]
            self.bias += deltaWeight * self.studyrate

    def output(self, data):
        currdata = np.array(data)
        return sigmoid(np.sum(currdata * self.weights) + self.bias)

    def setinitial(self):
        self.weights = np.random.rand(1, self.size)
        self.bias = random.uniform(0, 1)


# shuffle(continuousIris)


def train(trainingtimes, dataset, studyrate):
    Nodes = [OutputNode(4, studyrate), OutputNode(4, studyrate), OutputNode(4, studyrate)]
    for _ in range(int(trainingtimes)):
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

# train(300, continuousIris)
