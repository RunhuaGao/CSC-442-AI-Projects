class Arguments:
    possiblevalues = [True, False]

    def __init__(self, symbol=None, negative=False):
        self.originalsymbol = symbol
        self.possiblevalues = [True, False]
        self.isnegative = negative

    def trueValue(self):
        return self.possiblevalues[0] if not self.isnegative else self.possiblevalues[1]

    def falseValue(self):
        return self.possiblevalues[1] if not self.isnegative else self.possiblevalues[0]

    def __repr__(self):
        return self.originalsymbol if not self.isnegative else "!" + self.originalsymbol

    def isNegative(self, argument):
        assert type(argument) == Arguments
        return self.originalsymbol == argument.originalsymbol and (self.isnegative == (not argument.isnegative))

    def getNegativeArg(self):
        return Arguments(self.originalsymbol, not self.isnegative)

    def equals(self, other):
        return self.originalsymbol == other.originalsymbol and self.isnegative == other.isnegative

    @classmethod
    def setArgument(cls, literals):
        dic = dict.fromkeys([repr(a) for a in literals])
        for i in literals:
            dic[repr(i)] = i
        return list(dic.values())

    @classmethod
    def isNegativeSymbol(cls, symbol1, symbol2):
        return symbol1 == "!" + symbol2 or symbol2 == "!" + symbol1
