import matplotlib.pyplot as plt
import numpy as np
from DecisionTree import DecisionTree, iris, cars
from NeuralNetwork import train, continuousIris, normalizedIris

#iris and cars are used for decision tree experiment
# continuousIris and normalizedIris are used for neural network experiment

# plot the change of error rate with change of training times: Neural netWork
# set default studyrate as 0.01
def plotNeuralNetworkwithTrainingtimes(dataset, mintrainingtimes, maxtrainingtimes):
    x = np.linspace(mintrainingtimes, maxtrainingtimes, 100)
    y = [train(int(c), dataset) for c in x]
    plt.plot(x, y)
    plt.xlabel("training times")
    plt.ylabel("Error number")
    plt.title("Error number vs training times")
    plt.show()


def plotNeuralNetworkwithStudyrate(dataset, minstudyrate, maxstudyrate, trainingtimes):
    studyrate = np.linspace(minstudyrate, maxstudyrate, 50)
    y = [train(trainingtimes, dataset, s) for s in studyrate]
    plt.plot(studyrate, y)
    plt.xlabel("Studyrate")
    plt.ylabel("Error number")
    plt.title("Error number vs studyrate at trainingtimes %d" % trainingtimes)
    plt.show()


# plot change of error number with change of piece num in cross validation:Decision Tree
def plotDecisionTreewithPieceNum(dataset):
    dt = DecisionTree(dataset)
    size = len(dataset)
    x = [i for i in range(2, size // 2 + 1) if size % i == 0]
    y = []
    for t in x:
        y.append(dt.crossValidation(t))
    plt.scatter(x, y, edgecolors="blue")
    plt.xlabel("Cross validation piece")
    plt.ylabel("Error rate")
    plt.title("Error rate vs piece number")
    plt.show()


# plotNeuralNetworkwithStudyrate(dataset=normalizedIris, minstudyrate=0.005,
#                                maxstudyrate=0.01, trainingtimes=1000)
