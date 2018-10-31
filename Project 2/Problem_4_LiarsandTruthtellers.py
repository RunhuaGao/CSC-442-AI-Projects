from Argument import Arguments
from Parameters import *
from Sentence import Sentence, CnfSentence
from ModelCheck import ModelChecking
from PL_Resolution import PL_Resolution, resolutionTest

# All three people symbols, global variables
Amy = Arguments("Amy");
Bob = Arguments("Bob");
Cal = Arguments("Cal");
names = ["Amy", "Bob", "Cal"]
# literals list to use,global variables
literals = [Amy, Bob, Cal]

# Part Model Check Class, passin all basic symbols
check = ModelChecking(literals)

# All Three atomic Propositional sentences
Sentence_Amy = Sentence(unit, [Amy])
Sentence_Bob = Sentence(unit, [Bob])
Sentence_Cal = Sentence(unit, [Cal])


def modelCheckKBParta():
    """
    :return: The Knowledge base sentences of modelchecking of part a
    """
    sentence_2 = Sentence(conjunction, [Cal, Amy])
    KB1 = Sentence(equals, [Sentence_Amy, sentence_2], sentenceBase=True)

    sentence_3 = Sentence(unit, [Bob])
    sentence_4 = Sentence(negative, [Cal])
    KB2 = Sentence(equals, [Sentence_Bob, sentence_4], sentenceBase=True)

    sentence_6 = Sentence(negative, [Amy])
    sentence_7 = Sentence(disjunction, [sentence_3, sentence_6], sentenceBase=True)
    KB3 = Sentence(equals, [Sentence_Cal, sentence_7], sentenceBase=True)

    KB = [KB1, KB2, KB3]
    return KB


def modelCheckingParta():
    """
    :return: Do model checking on part a, find a model that satisfies knowledge base
    """
    check.check(modelCheckKBParta())


def modelCheckKBPartb():
    """
    :return knowledge base sentences of model checking of part b
    """
    sentecne_1 = Sentence(negative, [Cal])
    KB1 = Sentence(equals, [Sentence_Amy, sentecne_1], True)

    sentence_2 = Sentence(conjunction, [Amy, Cal])
    KB2 = Sentence(equals, [Sentence_Bob, sentence_2], True)

    KB3 = Sentence(equals, [Sentence_Cal, sentence_2], True)
    return [KB1, KB2, KB3]


def modelCheckingPartb():
    """
    :return: Do model checking on part b, find a model that satisfies knowledge base
    """
    check.check(modelCheckKBPartb())


def resolutionKBParta():
    """
    :return: Cnf sentences knowledge base for part a
    """
    cnfsentences = []

    cnfsentences.append(CnfSentence([Cal, Amy.getNegativeArg()]))

    cnfsentences.append(CnfSentence([Bob.getNegativeArg(), Cal.getNegativeArg()]))

    cnfsentences.append(CnfSentence([Bob, Cal]))

    cnfsentences.append(CnfSentence([Cal.getNegativeArg(), Bob, Amy.getNegativeArg()]))

    cnfsentences.append(CnfSentence([Cal, Bob.getNegativeArg()]))

    cnfsentences.append(CnfSentence([Cal, Amy]))

    return cnfsentences


def resolutionKBPartb():
    """
    :return: CNF sentences knowledge base of part b
    """
    cnfsentences = list()
    cnfsentences.append(CnfSentence([Amy.getNegativeArg(), Cal.getNegativeArg()]))
    cnfsentences.append(CnfSentence([Cal, Amy]))
    cnfsentences.append(CnfSentence([Bob.getNegativeArg(), Amy]))
    cnfsentences.append(CnfSentence([Bob.getNegativeArg(), Cal]))
    cnfsentences.append(CnfSentence([Amy.getNegativeArg(), Bob, Cal.getNegativeArg()]))
    cnfsentences.append(CnfSentence([Cal.getNegativeArg(), Bob]))
    cnfsentences.append(CnfSentence([Cal, Bob.getNegativeArg()]))
    return cnfsentences


def testParta():
    kb = resolutionKBParta()
    for name in names:
        resolutionTest(kb, name)


def testPartb():
    kb = resolutionKBPartb()
    for name in names:
        resolutionTest(kb, name)


modelCheckingParta()
testParta()
modelCheckingPartb()
testPartb()
