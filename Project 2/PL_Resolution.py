from Parameters import empty
from Argument import Arguments


class Resolution:
    """
    All sentecne passed in must be preprocessed, convert it into CNF disjunction format
    In others words, the operator of each sentence must be disjunction or unit or negative(atomic symbols)
    """

    def __init__(self, literals1, literals2):
        self.literals1 = literals1.copy()
        self.literals2 = literals2.copy()

    def getResolved(self):
        complementary = 0
        deleteargs = []
        totalliterals = self.literals2.union(self.literals1)
        for arg1 in self.literals1:
            for arg2 in self.literals2:
                if Arguments.isNegativeSymbol(arg2, arg1):
                    if complementary == 1:
                        return None
                    complementary += 1
                    deleteargs = (arg2, arg1)
        if complementary == 0:
            return None
        else:
            [totalliterals.remove(arg) for arg in deleteargs]
            if not totalliterals:
                return empty
            return totalliterals


class PL_Resolution:
    def __init__(self, clauses, proved):
        assert len(clauses) > 1
        self.clauses = [s.symbols for s in clauses]
        self.proved = proved
        self.new = []

    # used for partial model inference resolution
    def Proved(self, ifPrint=False):
        roundnum = 1
        while True:
            size = len(self.clauses)
            pairs = [(self.clauses[i], self.clauses[j]) for i in range(size) for j in range(i + 1, size)]
            for s1, s2 in pairs:
                resolvents = Resolution(s1, s2).getResolved()
                if not resolvents:
                    continue
                if Resolution(resolvents, self.proved).getResolved() == empty:
                    if ifPrint:
                        self.printResolve(s1, s2, resolvents)
                    return True
                elif resolvents is not None and resolvents not in self.new:
                    if ifPrint:
                        self.printResolve(s1, s2, resolvents)
                    if len(resolvents) <= 2:  # critical optimization
                        self.new.append(resolvents)
            isSubset = True
            for i in self.new:
                if i not in self.clauses:
                    isSubset = False
                    break
            if isSubset:
                return False
            [self.clauses.append(i) for i in self.new if i not in self.clauses]
            # print("Round %d finished. " % roundnum)
            # roundnum += 1

    def printResolve(self, s1, s2, resolvents):
        print(s1, "<< >>", s2, "resolves ", resolvents)
        print("\n")


def resolutionTest(kb, literal):
    print("test object is %s" % literal)
    print("Now add %s to knowledge base" % literal)
    proved = set([literal])
    result1 = PL_Resolution(kb, proved).Proved()
    print("result is: ", result1)
    print("Now add !%s to knowledge base" % literal)
    proved = set(["!" + literal])
    result2 = PL_Resolution(kb, proved).Proved()
    print("result is: ", result2)
    if result1:
        print(literal, "is False")
    elif result2:
        print(literal, "is True")
    else:
        print("Could not decide %s" % literal)
    print("--------------")
