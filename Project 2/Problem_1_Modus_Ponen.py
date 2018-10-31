from Argument import Arguments
from Parameters import *
from Sentence import Sentence, CnfSentence
from ModelCheck import ModelChecking
from PL_Resolution import resolutionTest

# all propositional symbols
P_symbol = Arguments("P")  # P symbol
Q_symbol = Arguments("Q")  # Q symbol


def modelchecking():
    # construct sentences and the sentence to be proved
    args = [P_symbol, Q_symbol]  # all symbols, stored in a list

    P = Sentence(unit, [P_symbol])  # Use P to establish a sentence, atomic sentence
    Q = Sentence(unit, [Q_symbol])  # Use Q to establish a sentence, atomic sentence
    P_implies_Q = Sentence(implies, args)  # Sentence: P implies Q
    KB = [P, P_implies_Q]  # The knowledge base we have, P and P implies Q

    # implement model checking
    check = ModelChecking(args)  # The instance of class - model checking , pass in all basic symbols
    check.check(KB, Q)  # do model check, pass in Knowledge base and the sentence we wanna prove


def resolutionKB():
    nP = Arguments("P", negative=True)

    nQ = Arguments("Q", negative=True)

    Sentence1 = CnfSentence([nP, Q_symbol])
    Sentence2 = CnfSentence([P_symbol])

    return [Sentence1, Sentence2]


print("Now do model checking")
modelchecking()
print("Now do PL_Resolution")
resolutionTest(resolutionKB(), "Q")
