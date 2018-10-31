from Argument import Arguments
from Parameters import *
from Sentence import Sentence, CnfSentence
from ModelCheck import ModelChecking
from PL_Resolution import resolutionTest

Doors = ["X", "Y", "W", "Z"]
Door = {key: Arguments(key) for key in Doors}
priests = ["A", "B", "C", "D", "E", "F", "G", "H"]
priest = {key: Arguments(key) for key in priests}
lits = list(Door.values()) + list(priest.values())
T = Arguments("T")
Q = Arguments("Q")


# model checking knowledge base
def modelcheckingKBParta():
    KB = []

    # sentence 0: at leats one of doors is good
    KB.append(Sentence(disjunction, Door.values()))

    # sentence 1: A says X is a good door
    KB.append(Sentence(equals, [priest["A"], Door["X"]]))

    # sentence 2: B says at least one of Y and Z is good
    KB.append(Sentence(equals, [Sentence(unit, [priest["B"]]),
                                Sentence(disjunction, [Door["Y"], Door["Z"]])], True))
    # sentence 3: C says A and B are knight
    KB.append(Sentence(equals, [Sentence(unit, [priest["C"]]),
                                Sentence(conjunction, [priest["A"], priest["B"]])], True))

    # sentence 4: D says X any Y are both good doors
    KB.append(Sentence(equals, [Sentence(unit, [priest["D"]]),
                                Sentence(conjunction, [Door["X"], Door["Y"]])], True))

    # sentence 5: E says X and Z are both good doors
    KB.append(Sentence(equals, [Sentence(unit, [priest["E"]]),
                                Sentence(conjunction, [Door["X"], Door["Z"]])], True))

    # sentenc 6: F says either D or E is knight
    KB.append(Sentence(equals, [Sentence(unit, [priest["F"]]),
                                Sentence(disjunction, [priest["D"], priest["E"]])], True))

    # sentence 7: G says if c is knight, so it is F
    # process the sentence, convert it to CNF: !G or C, !G or !F
    sentencesource = Sentence(unit, [priest["G"]])
    sentenceconclusion = Sentence(implies, [priest["C"], priest["F"]])
    KB.append(Sentence(equals, [sentencesource, sentenceconclusion], True))

    # sentence 8: H says If G and H are knights, so is A.
    # process the sentence, convert it into CNF:
    # Cnf clause: !G or !H or A
    source = Sentence(unit, [priest["H"]])
    conclusionSource = Sentence(conjunction, [priest["H"], priest["G"]])
    conclusionConclusion = Sentence(unit, [priest["A"]])
    conlusion = Sentence(implies, [conclusionSource, conclusionConclusion], True)
    KB.append(Sentence(equals, [source, conlusion], True))

    return KB


# do model checking, show all models that satisfies the knowledge base
def modelcheckingParta():
    ModelChecking(lits).check(modelcheckingKBParta(),prove=Sentence(unit,[Door["X"]]))


# resolution knowledge base, in format of clause
def resolutionKBParta():
    KB = []

    # sentence0
    KB.append(CnfSentence(Door.values()))

    # sentence1
    KB.append(CnfSentence([priest["A"].getNegativeArg(), Door["X"]]))
    KB.append(CnfSentence([priest["A"], Door["X"].getNegativeArg()]))

    # sentence2
    KB.append(CnfSentence([priest["B"].getNegativeArg(), Door["Y"], Door["Z"]]))
    KB.append(CnfSentence([priest["B"], Door["Y"].getNegativeArg()]))
    KB.append(CnfSentence([priest["B"], Door["Z"].getNegativeArg()]))

    # sentence3
    C = priest["C"]
    A = priest["A"]
    B = priest["B"]
    KB.append(CnfSentence([C.getNegativeArg(), A]))
    KB.append(CnfSentence([C.getNegativeArg(), B]))
    KB.append(CnfSentence([A.getNegativeArg(), B.getNegativeArg(), C]))

    # sentence4
    D = priest["D"]
    X = Door["X"]
    Y = Door["Y"]
    KB.append(CnfSentence([D.getNegativeArg(), X]))
    KB.append(CnfSentence([D.getNegativeArg(), Y]))
    KB.append(CnfSentence([D, X.getNegativeArg(), Y.getNegativeArg()]))

    # sentence5
    Z = Door["Z"]
    E = priest["E"]
    KB.append(CnfSentence([E.getNegativeArg(), X]))
    KB.append(CnfSentence([E.getNegativeArg(), Z]))
    KB.append(CnfSentence([E, X.getNegativeArg(), Z.getNegativeArg()]))

    # sentence6
    F = priest["F"]
    KB.append(CnfSentence([F.getNegativeArg(), D, E]))
    KB.append(CnfSentence([F, D.getNegativeArg()]))
    KB.append(CnfSentence([F, E.getNegativeArg()]))

    # sentence7
    G = priest["G"]
    KB.append(CnfSentence([G.getNegativeArg(), C.getNegativeArg(), F]))
    KB.append(CnfSentence([G, C]))
    KB.append(CnfSentence([G, F.getNegativeArg()]))

    # sentence8
    H = priest["H"]
    KB.append(CnfSentence([G.getNegativeArg(), H.getNegativeArg(), A]))
    KB.append(CnfSentence([H, G]))
    KB.append(CnfSentence([H]))
    KB.append(CnfSentence([H, A.getNegativeArg()]))

    return KB


def modelcheckingKBPartb():
    kba = modelcheckingKBParta()
    # fragment 1:
    conlusion1 = Sentence(conjunction, [T, priest["A"]])
    premise1 = Sentence(unit, [priest["C"]])
    sentence1 = Sentence(equals, [premise1, conlusion1], True)
    # fragment 2:
    k1 = Sentence(implies, [priest["C"], Q])
    k2 = Sentence(unit, [priest["G"]])
    sentence2 = Sentence(equals, [k2, k1], True)
    return [kba[0], kba[1], kba[-1], sentence1, sentence2]


def modelcheckingPartb():
    lit = lits + [T, Q]
    ModelChecking(lit).check(modelcheckingKBPartb(), prove=Sentence(unit, [Door["X"]]))


def resolutionKBPartb():
    KB = []

    # sentence0
    KB.append(CnfSentence(Door.values()))

    # sentence1
    A = priest["A"]
    G = priest["G"]
    KB.append(CnfSentence([priest["A"].getNegativeArg(), Door["X"]]))
    KB.append(CnfSentence([priest["A"], Door["X"].getNegativeArg()]))

    # sentence8
    H = priest["H"]
    KB.append(CnfSentence([G.getNegativeArg(), H.getNegativeArg(), A]))
    KB.append(CnfSentence([H, G]))
    KB.append(CnfSentence([H]))
    KB.append(CnfSentence([H, A.getNegativeArg()]))

    # fragment1
    C = priest["C"]
    KB.append(CnfSentence([C.getNegativeArg(), A]))
    KB.append(CnfSentence([C.getNegativeArg(), T]))
    KB.append(CnfSentence([A.getNegativeArg(), T.getNegativeArg(), C]))

    # fragment2
    KB.append(CnfSentence([G.getNegativeArg(), C.getNegativeArg(), Q]))
    KB.append(CnfSentence([C, G]))
    KB.append(CnfSentence([Q.getNegativeArg(), G]))
    return KB


def testParta():
    kba = resolutionKBParta()
    for i in Doors:
        resolutionTest(kba, i)


def testPartb():
    kbb = resolutionKBPartb()
    for door in Doors:
        resolutionTest(kbb, door)


