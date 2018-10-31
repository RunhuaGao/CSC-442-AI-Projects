from Argument import Arguments
from Parameters import *
from Sentence import Sentence, CnfSentence
from ModelCheck import ModelChecking
from PL_Resolution import PL_Resolution, resolutionTest

# all basic symbols
mythical = Arguments("mythical")
immortal = Arguments("immortal")
horned = Arguments("horned")
magical = Arguments("magical")
mammal = Arguments("mammal")
# literals
literals = [mythical, immortal, horned, magical, mammal]


def modelchecking():
    # construct sentence
    # part a goal sentence
    sentence_1 = Sentence(unit, [mythical])
    sentence_2 = Sentence(unit, [immortal])
    KB1 = Sentence(implies, [sentence_1, sentence_2], sentenceBase=True)

    sentence_3 = Sentence(negative, [mythical])
    sentence_3_2 = Sentence(negative, [immortal])
    sentence_3_3 = Sentence(unit, [mammal])
    sentence_3_4 = Sentence(conjunction, [sentence_3_2, sentence_3_3], True)
    KB2 = Sentence(implies, [sentence_3, sentence_3_4], True)

    # part b goal sentence
    sentence_5 = Sentence(disjunction, [immortal, mammal])
    sentence_6 = Sentence(unit, [horned])
    KB3 = Sentence(implies, [sentence_5, sentence_6], sentenceBase=True)
    # part b goal sentence
    sentence_7 = Sentence(unit, [magical])
    KB4 = Sentence(implies, [sentence_6, sentence_7], sentenceBase=True)

    KB = [KB1, KB2, KB3, KB4]
    check = ModelChecking(literals)

    # # part a: to prove mythical, sentence1
    # print(check.check(KB, sentence_1))
    #
    # # part b: to prove magical, sentence7
    # print(check.check(KB, sentence_7))
    #
    # # part c:to prove horned,sentence6
    # print(check.check(KB, sentence_6))

    check.check(KB)


# modelchecking()


def resolutionKB():
    # The resolution cnfsentences knowledge base
    cnfsentences = []

    cnfsentences.append(CnfSentence([mythical.getNegativeArg(), immortal]))

    cnfsentences.append(CnfSentence([mythical, mammal]))

    cnfsentences.append(CnfSentence([mythical, immortal.getNegativeArg()]))

    cnfsentences.append(CnfSentence([horned, immortal.getNegativeArg()]))

    cnfsentences.append(CnfSentence([horned, mammal.getNegativeArg()]))

    cnfsentences.append(CnfSentence([horned.getNegativeArg(), magical]))
    return cnfsentences


def testResolution():
    kb = resolutionKB()
    resolutionTest(kb, "magical")
    resolutionTest(kb, "horned")
    resolutionTest(kb, "mythical")


modelchecking()
testResolution()
