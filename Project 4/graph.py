import matplotlib.pyplot as plt
import numpy as np
from DecisionTree import DecisionTree,iris,cars


def plotNeuralNetwork(dataset):
    x = np.linspace(10, 1000, 20)
    y = [train(int(c), dataset) for c in x]
    plt.plot(x, y)
    plt.xlabel("training times")
    plt.ylabel("Error number")
    plt.title("Error number vs training times")
    plt.show()


def plotDecisionTree(dataset):
    dt = DecisionTree(dataset)
    size = len(dataset)
    x = [i for i in range(2, size // 2 + 1) if size % i == 0]
    y = []
    for t in x:
        y.append(dt.crossValidation(t))
    plt.scatter(x, y,edgecolors="blue")
    plt.xlabel("Cross validation piece")
    plt.ylabel("Error rate")
    plt.title("Error rate vs piece number")
    plt.show()

plotDecisionTree(cars)