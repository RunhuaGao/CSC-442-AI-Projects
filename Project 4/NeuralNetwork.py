from math import e
import numpy as np
import random

sigmoid = lambda x: 1 / (1 + e ** (-x))
loss = lambda x, y: (x - y) ** 2
sderivation = lambda x: x * (1 - x)

studyrate =0.6


class InputLayer:
    def __init__(self, size):
        self.size = size

    def addlaterlayer(self, layer):
        self.laterlayer = layer
        self.weight = np.mat(np.random.rand(self.size, self.laterlayer.size))

    def output(self, data):
        return np.mat(data)

    def updateweight(self, data, laterdelta):
        output = self.output(data).T
        delta = -studyrate * output * laterdelta
        self.weight += delta


class MiddleLayer(InputLayer):
    def __init__(self, size):
        InputLayer.__init__(self, size)

    def addformerlayer(self, layer):
        self.formerlayer = layer

    def output(self, data):
        sum = np.dot(self.formerlayer.output(data), self.formerlayer.weight)
        res = []
        for i in range(sum.shape[1]):
            res.append(sigmoid(sum[0, i]))
        return np.mat(res)

    def updateweight(self, data, target):
        delta = -studyrate * np.multiply(self.output(data).T,
                                         self.laterlayer.errorderivation(data, target))
        self.weight += delta

    def errorderivation(self, laterdelta, data):
        output = self.output(data)
        other = np.mat(np.ones(output.shape)) - output
        res = np.multiply(output, other)
        res1 = self.weight * laterdelta.T
        return np.multiply(res1.T, res)


class OutputLayer(MiddleLayer):
    def __init__(self, size):
        MiddleLayer.__init__(self, size)

    def errorderivation(self, data, target):
        output = self.output(data)
        lossmat = output - np.mat(target)
        res = np.multiply(lossmat, output)
        other = np.mat(np.ones(output.shape))
        other = other - output
        return np.multiply(res, other)


from DataParser import continuousIris

# shuffle(continuousIris)
for i in range(len(continuousIris)):
    if continuousIris[i][-1] == "setosa":
        continuousIris[i][-1] = [1, 0, 0]
    elif continuousIris[i][-1] == "versicolor":
        continuousIris[i][-1] = [0, 1, 0]
    else:
        continuousIris[i][-1] = [0, 0, 1]

inputlayer = InputLayer(4)
middlelayer = MiddleLayer(2)
outputlayer = OutputLayer(3)
inputlayer.addlaterlayer(middlelayer)
middlelayer.addformerlayer(inputlayer)
middlelayer.addlaterlayer(outputlayer)
outputlayer.addformerlayer(middlelayer)


def train(examples):
    for data in examples:
        d, target = data[:-1], data[-1]
        outerr = outputlayer.errorderivation(d, target)
        miderr = middlelayer.errorderivation(outerr, d)
        inputlayer.updateweight(d, miderr)
        middlelayer.updateweight(d, outerr)

        # print("input layer weight is: ",inputlayer.weight)
        # print("middle layer weight is: ",middlelayer.weight)


    for data in examples:
        d = data[:-1]
        print(outputlayer.output(d))



train(continuousIris)