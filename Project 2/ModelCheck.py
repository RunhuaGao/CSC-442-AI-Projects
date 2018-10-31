# input: a list arguments/Propositional arguments
# output: all possible worlds for the list of argument
class GetModel:
    def getModel(self, arguments):
        return self.getModelHelper(arguments)

    def getModelHelper(self, argument):
        if len(argument) == 1:
            return [[argument[0].trueValue()], [argument[0].falseValue()]]
        results = self.getModelHelper(argument[1:])
        start = argument[0]
        currentResult = []
        for i in results:
            currentResult.append([start.trueValue()] + i)
            currentResult.append([start.falseValue()] + i)
        return currentResult


# The relation is a three
class ModelChecking:
    def __init__(self, arguments):
        self.indexs = {value: key for key, value in enumerate(arguments)}
        self.models = GetModel().getModel(arguments)
        self.size = len(self.models[0])

    def checkSentences(self, sentences):
        for model in self.models:
            self.checkSentenceModel(model, sentences)

    def checkSentenceModel(self, model, sentences):
        self.printModel(model)
        for sentence in sentences:
            value = sentence.value(model, self.indexs)
            print("{} is {}".format(repr(sentence), value))
        print()

    def ifModelSatisfySentence(self, model, sentence):
        return sentence.value(model, self.indexs)

    def printModel(self, model):
        string = ""
        for key, value in self.indexs.items():
            string += "{} is {}, ".format(repr(key), model[value])
        print(string)

    def printSentenceModel(self, model, sentence):
        value = self.ifModelSatisfySentence(model, sentence)
        print("{} is {}".format(repr(sentence), value))

    def check(self, KB, prove=None):
        models = []
        passed = True
        for model in self.models:
            if sum([self.ifModelSatisfySentence(model, s) for s in KB]) == len(KB):
                models.append(model)
                self.printModel(model)
                for v in KB:
                    self.printSentenceModel(model, v)
                if prove:
                    self.printSentenceModel(model, prove)
                    passed = self.ifModelSatisfySentence(model, prove) and passed
                print("\n")
        if prove:
            if passed:
                print("KB entails {}".format(repr(prove)))
            else:
                print("There exist an model that KB is True and {} is False".format(repr(prove)))
        return models
