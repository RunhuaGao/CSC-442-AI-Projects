from Argument import Arguments
from Parameters import *
from Sentence import Sentence, CnfSentence
from ModelCheck import ModelChecking
from PL_Resolution import resolutionTest

B_1_1 = Arguments("B_1_1")  # Symbol B_1_1
B_2_1 = Arguments("B_2_1")  # Symbol B_2_1
P_1_1 = Arguments("P_1_1")  # Symbol B_3_1
P_1_2 = Arguments("P_1_2")  # Symbol P_1_2
P_2_1 = Arguments("P_2_1")  # Symbol P_2_1
P_2_2 = Arguments("P_2_2")  # Symbol P_2_2
P_3_1 = Arguments("P_3_1")  # Symbol P_3_1

#  all propositional symbols, stored in a list
literals = [B_1_1, B_2_1, P_1_1, P_1_2, P_2_1, P_2_2, P_3_1]


def modelchecking():
    # build all propositional symbols

    # build all sentence of knowledge base
    sentence1 = Sentence(disjunction, [P_1_2, P_2_1])  # Sentence: P_1_2 and P_2_1
    sentence2 = Sentence(unit, [B_1_1])  # Sentence: B_1_1
    KB1 = Sentence(equals, [sentence1, sentence2], True)  # Sentence: P_1_2 and P_2_1 equals B_1_1, KB1
    sentence3 = Sentence(unit, [B_2_1])  # Sentence: B_2_1
    sentence4 = Sentence(disjunction, [P_1_2, P_2_2, P_3_1])  # Sentence: P_1_2 and P_2_2 and P_3_1
    KB2 = Sentence(equals, [sentence3, sentence4], True)  # Sentence: B_2_1 equals P_1_2 and P_2_2 and P_3_1, KB2
    KB3 = Sentence(negative, [P_1_1])  # Sentence: negative P_1_1, KB3
    KB4 = Sentence(negative, [B_1_1])  # Sentence: negative B_1_1, KB4
    KB5 = Sentence(unit, [B_2_1])  # Sentence: B_2_1, KB5
    KB = [KB1, KB2, KB3, KB4, KB5]  # Store all knowledge base we have in a list

    # The sentence to prove
    prove = Sentence(negative, [P_1_2])

    #  implement model check processing use check instance method
    check = ModelChecking(literals)  # do model check, pass in all basic symbols
    check.check(KB, prove)  # do model checking, pass in the sentence we wanna prove


def resolutionKB():
    sentences = []
    sentences.append(CnfSentence([P_1_1.getNegativeArg()]))

    sentences.append(CnfSentence([B_1_1.getNegativeArg(), P_1_2, P_2_1]))

    sentences.append(CnfSentence([P_1_2.getNegativeArg(), B_1_1]))

    sentences.append(CnfSentence([P_2_1.getNegativeArg(), B_1_1]))

    sentences.append(CnfSentence([B_2_1.getNegativeArg(), P_1_1, P_2_2, P_3_1]))

    sentences.append(CnfSentence([B_2_1, P_1_1.getNegativeArg()]))

    sentences.append(CnfSentence([B_2_1, P_2_2.getNegativeArg()]))

    sentences.append(CnfSentence([B_2_1, P_3_1.getNegativeArg()]))

    sentences.append(CnfSentence([B_1_1.getNegativeArg()]))

    sentences.append(CnfSentence([B_2_1]))

    return sentences


print("Now do model checking")
modelchecking()  # do model checking, for all model in which knowledge is true, P_1_2 = False

print("Now do PL_Resolution")
resolutionTest(resolutionKB(), "P_1_2")
