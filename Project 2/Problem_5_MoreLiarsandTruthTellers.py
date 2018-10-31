from Argument import Arguments
from Parameters import *
from Sentence import Sentence, CnfSentence
from ModelCheck import ModelChecking
from PL_Resolution import resolutionTest

names = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]

# get all basic arguments/symbols, stored in a dictionary
literals = {key: Arguments(key) for key in names}
lits = list(literals.values())

# truth implies group
truthful1 = [["a", "h", "i"], ["b", "a", "l"], ["c", "b", "g"]]
truthful2 = [["d", "e", "l"], ["e", "c", "h"], ["f", "d", "i"]]
truthful = truthful1 + truthful2
# liars implies group
liars1 = [["g", "e", "j"], ["h", "f", "k"], ["i", "g", "k"]]
liars2 = [["j", "a", "c"], ["k", "d", "f"], ["l", "b", "j"]]
liars = liars1 + liars2
check = ModelChecking(list(literals.values()))


def createSentecne(people, isLiar=False):
    impliesSentences = []
    sourceArgument = literals[people[0]]
    premise = Sentence(unit, [sourceArgument])
    for p in people[1:]:
        impliesSentences.append(Sentence(unit if not isLiar else negative, [literals[p]]))

    conclusion = Sentence(conjunction, impliesSentences, True)

    return Sentence(equals, [premise, conclusion], True)


# create Propositional logic sentence by group
# Do model checking work
def createKB():
    KB = []
    for i in truthful1 + truthful2:
        KB.append(createSentecne(i))

    for i in liars1 + liars2:
        KB.append(createSentecne(i, True))
    # [print(k) for k in KB]
    return KB


# create Cnf sentence by group
def createCnfSentence(people, isLiar=False):
    argument1 = literals[people[0]].getNegativeArg()
    sentences = []
    for p in people[1:]:
        lit = literals[p]
        sentences.append(CnfSentence([argument1, lit if not isLiar else lit.getNegativeArg()]))
    sourcePeople = literals[people[0]]
    if not isLiar:
        p2, p3 = literals[people[1]].getNegativeArg(), literals[people[2]].getNegativeArg()
        sentences.append(CnfSentence([sourcePeople, p2, p3]))
    else:
        p2, p3 = literals[people[1]], literals[people[2]]
        sentences.append(CnfSentence([sourcePeople, p2, p3]))
    return sentences


# create resolution KB
def resolutionKB():
    KB = []
    for i in truthful1 + truthful2:
        KB.extend(createCnfSentence(i, isLiar=False))
    for v in liars1 + liars2:
        KB.extend(createCnfSentence(v, isLiar=True))
    return KB


# do model checking
def modelchecking():
    ModelChecking(lits).check(createKB())


def testResolution():
    kb = resolutionKB()
    for i in names:
        resolutionTest(kb, i)


# execute model checking
modelchecking()
testResolution()
