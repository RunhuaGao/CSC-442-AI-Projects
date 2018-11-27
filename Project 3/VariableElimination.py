from EnumerateInference import extend
from functools import reduce
from RandomVariables import rv
from RunProgram import processInput
import sys

class Factor:
    """
    Store Probability distribution for variable elimination algorithm
    """

    def __init__(self, variables, cpt):
        self.variables = variables
        self.cpt = cpt

    def pointwiseproduct(self, otherfactor, bn):
        """Do production between factors"""
        assert isinstance(otherfactor, Factor)
        variables = list(set(self.variables).union(set(otherfactor.variables)))
        cpt = {eventvalues(variables,e): self.p(e) * otherfactor.p(e)
               for e in allevents(variables, bn, {})}
        return Factor(variables, cpt)

    def sumout(self, var, bayesnet):
        variables = [X for X in self.variables if X != var]
        cpt = {}
        for event in allevents(variables,bayesnet,{}):
            key = eventvalues(variables,event)
            value = sum([self.p(extend(event,var,value)) for value in bayesnet[var].domain])
            cpt[key] = value
        return Factor(variables, cpt)

    def normalize(self):
        """Return my probabilities; must be down to one variable."""
        assert len(self.variables) == 1
        probdistribution = {k: v for k, v in self.cpt.items()}
        rv.normalize(probdistribution)
        return probdistribution

    def p(self, e):
        """Look up my value tabulated for e."""
        return self.cpt[eventvalues(self.variables,e)]


def elimination(query, evidence, bayesnet):
    """Compute variable elimination."""
    assert query not in evidence
    factors = []
    for node in bayesnet.nodes[::-1]:  # from right to left order
        factors.append(makefactor(node, evidence, bayesnet))
        if ishidden(node.name, query, evidence):
            factors = sumout(node.name, factors, bayesnet)
    return pointwiseproduct(factors, bayesnet).normalize()


def ishidden(var, X, e):
    return var != X and var not in e


def makefactor(query, evidence, bayesnet):
    variables = [n for n in [query.name] + list(query.parents) if n not in evidence]
    cpt = {eventvalues(variables, e): query.calProba(e[query.name], e)
           for e in allevents(variables, bayesnet, evidence)}
    return Factor(variables, cpt)


def pointwiseproduct(factors, bayesnet):
    return reduce(lambda f, g: f.pointwiseproduct(g, bayesnet), factors)


def sumout(query, factors, bayesnet):
    """Summation of query variable """
    result, varfactors = [], []
    for f in factors:
        if query in f.variables:
            varfactors.append(f)
        else:
            result.append(f)
    result.append(pointwiseproduct(varfactors, bayesnet).sumout(query, bayesnet))
    return result


def allevents(variables, bayesnet, event):
    """Create All possibile event by extending variables to event """
    if not variables:
        yield event
    else:
        first, rest = variables[0], variables[1:]
        for e1 in allevents(rest, bayesnet, event):
            for x in bayesnet[first].domain:
                yield extend(e1, first, x)


def eventvalues(variables, event):
    if isinstance(event, tuple) and len(event) == len(variables):
        return event
    return tuple([event[var] for var in variables])

if __name__ == "__main__":
    net,query,evidence = processInput(sys.argv)
    distribution = elimination(query,evidence,net)
    print(distribution)
