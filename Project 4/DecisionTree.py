from math import log
from DataParser import readfile
from random import shuffle

iris = readfile("iris.data.discrete.txt")
restaurant = readfile("AIMA_Restaurant-data.txt")
cars = readfile("cars.txt")


class DecisionTree:
    def __init__(self, examples):
        shuffle(examples)
        self.examples = examples
        self.defaultype = DecisionTree.getDefaultValue(examples)

    @property
    def datasize(self):
        return len(self.examples)

    @property
    def initialattrs(self):
        return list(range(len(self.examples[0]) - 1))

    @classmethod
    # return the entropy with a probability
    def calH(cls, prob):
        return -prob * log(prob, 2)

    @classmethod
    # calculate entropy based on input data set
    def calEntropy(cls, data):
        dic = {}
        for d in data:
            currtype = d[-1]  # get the data's class
            if currtype not in dic:
                dic[currtype] = 0
            dic[currtype] += 1
        res = 0
        totaldata = len(data)
        for key, value in dic.items():
            res += DecisionTree.calH(float(value / totaldata))
        return res

    @classmethod
    # return the subset data split by a specific attribute
    def splitDataByAttr(cls, data, attr):
        if len(data) > 0:
            dic = {}
            for i in range(len(data)):
                currtype = data[i][attr]
                if currtype not in dic:
                    dic[currtype] = []
                dic[currtype].append(i)
            return dic
        return {}

    @classmethod
    # calculate the entropy after split by a specific attribute
    def calEntropySplitByAttr(cls, data, attr):
        exs = DecisionTree.splitDataByAttr(data, attr)
        res = 0
        totalsize = len(data)
        for key, value in exs.items():
            currsize = len(value)
            res += float(currsize / totalsize) * DecisionTree.calEntropy([data[i] for i in value])
        return res

    @classmethod
    # choose a attribute from the data depends on entropy
    def chooseAttr(cls, data, attrs):
        assert len(data) > 0
        parententropy = DecisionTree.calEntropy(data)
        res = 0
        gain = None
        for a in attrs:
            tempvalue = parententropy - DecisionTree.calEntropySplitByAttr(data, a)
            if gain is None or tempvalue > gain:
                gain = tempvalue
                res = a
        return res

    @classmethod
    # choose a most common output from the inout data
    def plurality(cls, data):
        res = {}
        for d in data:
            currtype = d[-1]
            if currtype not in res:
                res[currtype] = 0
            res[currtype] += 1
        output = -1
        maxvalue = 0
        for key, value in res.items():
            if value > maxvalue:
                output = key
                maxvalue = value
        return output

    @classmethod
    def getDefaultValue(cls, exmaples):
        dic = {}
        for d in exmaples:
            t = d[-1]
            if t not in dic: dic[t] = 0
            dic[t] += 1
        value = max(dic.values())
        for key in dic:
            if dic[key] == value: return key

    # implement Figure 18.3's algorithm
    def learning(self, examples, attrs, parentexamples):
        if len(examples) == 0:
            return DecisionTree.plurality(parentexamples)
        elif len(set([i[-1] for i in examples])) == 1:
            return examples[0][-1]
        elif len(attrs) == 0:
            return DecisionTree.plurality(examples)
        else:
            splitattr = DecisionTree.chooseAttr(examples, attrs)
            root = DecisionTreeNode(splitattr, self.defaultype)
            for att, exs in DecisionTree.splitDataByAttr(examples, splitattr).items():
                subtree = self.learning([examples[i] for i in exs],
                                        DecisionTree.deleteattr(attrs, splitattr), examples)
                root.addbranch(att, subtree)
            return root

    @classmethod
    def deleteattr(self, attrs, attr):
        res = attrs.copy()
        if attr in attrs: res.remove(attr)
        return res

    # Do experiment with cross validation
    # parameter k: split while data set into k pieces
    def crossValidation(self, k):
        validationdata = splitData(self.examples, k)
        errorate = 0
        for _ in range(k):
            traindata, testdata = validationdata.croosvalidationdata()
            tree = self.learning(traindata, self.initialattrs, traindata)
            errorate += tree.testData(testdata)
        print("Average error rate is: ", float(errorate / k))
        return float(errorate / k)


# Decision tree's node class
class DecisionTreeNode:
    def __init__(self, attr, defaultvalue):
        self.attr = attr
        self.defaultvalue = defaultvalue
        self.branch = {}

    # add a branch to current node,used in learning method
    def addbranch(self, key, value):
        self.branch[key] = value

    # print out whole tree with
    def showTree(self, spacenum=0):
        prefix = " " * spacenum
        print(prefix + "curr attribute is " + str(self.attr))
        for key, value in self.branch.items():
            if isinstance(value, DecisionTreeNode):
                print(prefix + "current value is " + str(key))
                value.showTree(spacenum + 4)
            else:
                print(prefix + "current value is " + str(key), "classified as " + str(value))
            print(prefix + "--- this branch has printed out, splited by attribute %d" % self.attr)
        print(prefix + "whole branches has printed out at attribute %d" % self.attr)

    # evaluating a single data based on the tree
    def evaluatedata(self, data):
        assert self.attr < len(data) - 1
        # if the tree do not have a branch with value that data has
        # directly classify it to default type
        if data[self.attr] not in self.branch: return self.defaultvalue
        nextbranch = self.branch[data[self.attr]]
        if isinstance(nextbranch, DecisionTreeNode):
            return nextbranch.evaluatedata(data)
        else:
            return nextbranch

    # test single data
    def __test__(self, data):
        return self.evaluatedata(data) == data[-1]

    # test whole data, calculate error rate
    def testData(self, data):
        count = 0
        for item in data:
            if not self.__test__(item): count += 1
        print("Error rate is: ", float(count / len(data)))
        return float(count / len(data))


# auxiliary class to split a data set into k pieces to
# implement cross validation experiment
# ths instance has some local state
class splitData:
    def __init__(self, data, k):
        self.data = data
        assert len(data) % k == 0, \
            "Please input another proper k to split data set"
        self.piecesize = len(data) // k
        self.start = 0

    def croosvalidationdata(self):
        traindata = self.data[:self.start] \
                    + self.data[self.start + self.piecesize:]
        testdata = self.data[self.start:self.start + self.piecesize]
        self.start += self.piecesize
        if self.start == len(self.data):
            self.start = 0
        return traindata, testdata



def docrossvaidation(example,num):
    dt = DecisionTree(example)
    dt.crossValidation(num)

docrossvaidation(cars,27)