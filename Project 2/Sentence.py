# A Propositional logical expression class
# The constructor should includes arguments and one operator
# The arg could also be sentence


from Parameters import *


# more like a parser
class Sentence:
    def __init__(self, operator, args, sentenceBase=False):
        self.operator = operator
        self.args = args
        self.sentenceBase = sentenceBase

    def value(self, model, indexs=None):
        if self.sentenceBase:
            return self.valueSentenceBase(model, indexs)
        else:
            return self.valueArgumentBase(model, indexs)

    def valueArgumentBase(self, model, indexs):
        assert indexs is not None
        model = [model[indexs[arg]] for arg in self.args]
        if self.operator in [conjunction, disjunction]:
            return operatorValues[self.operator](model)
        if self.operator in [implies, equals]:
            if self.sentenceBase:
                return self.valueSentenceBase()
            return operatorValues[self.operator](model[0], model[1])
        if self.operator in [unit, negative]:
            return operatorValues[self.operator](model[0])

    def valueSentenceBase(self, model, indexs):
        if self.operator in [implies, equals]:
            assert indexs is not None
            value1 = self.args[0].value(model, indexs)
            value2 = self.args[1].value(model, indexs)
            return operatorValues[self.operator](value1, value2)
        else:
            return operatorValues[self.operator]([arg.value(model, indexs) for arg in self.args])

    def __repr__(self):
        if not self.sentenceBase:
            values = [" " + repr(arg) + " " for arg in self.args]
            if self.operator in [conjunction, disjunction, implies, equals]:
                return "{}".format(self.operator).join(values)
            else:
                return self.operator + repr(self.args[0]) if self.operator is negative else repr(self.args[0])
        else:
            return " %s " % self.operator.join([repr(arg) for arg in self.args])

    def equals(self, anothersentence):
        assert type(anothersentence) == Sentence
        return repr(self) == repr(anothersentence)


# Cnf sentence class, represent as a set of strings of arguments
class CnfSentence(Sentence):
    def __init__(self, args):
        Sentence.__init__(self, disjunction, args)
        self.args = args
        self.symbols = set([repr(arg) for arg in self.args])

    def __eq__(self, other):
        assert type(other) == CnfSentence or other == empty
        if other == empty:
            return len(self.args) == 0
        return self.reprArgs() == other.reprArgs()

    def __repr__(self):
        return " or ".join(self.symbols)
