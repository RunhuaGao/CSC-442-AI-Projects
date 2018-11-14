from random import uniform


def probability(p):
    """
    :param p: The probability
    :return: True or False, the value of for a random variable
    """
    return p > uniform(0.0, 1.0)


# class bayes net
# only a data abstraction to store all random variables
class baysnet:
    def __init__(self, rvs=None):
        self.variablesroom = {}
        if rvs:
            for r in rvs:
                self.addvariable(r)

    def addvariable(self, va):
        assert isinstance(va, rv)
        self.variablesroom[va.name] = va

    def __getitem__(self, item):
        assert item in self.variablesroom
        return self.variablesroom[item]

    @property
    def nodes(self):
        currlevel = [r.name for r in self.variablesroom.values() if len(r.parents) == 0]
        size = len(self.variablesroom)
        result = []
        while len(result) < size:
            result.extend(currlevel)
            if len(currlevel) > 0:
                nodes = set()
                for node in currlevel:
                    nodes = nodes.union(self.variablesroom[node].children)
                currlevel = nodes
        return [self.variablesroom[key] for key in result]


class rv:
    def __init__(self, name, domain):
        self.name = name
        self.domain = [self.evaluate(k) for k in domain]
        self.parentNodes = []
        self.parents = set()
        self.childNodes = []
        self.children = set()

    def __eq__(self, other):
        return other.name == self.name

    def __repr__(self):
        return self.name

    def addParentNode(self, parentnode):
        self.parentNodes.append(parentnode)
        self.parents.add(parentnode.name)

    def addChildNode(self, childNode):
        self.childNodes.append(childNode)
        self.children.add(childNode.name)

    # get kth probability of random variable's domain
    def kthproba(self, k):
        if k > len(self.domain):
            raise IndexError("Out of variable's domain size")
        return self.domain[k]

    # add the Table(probability of the random variable in bayes network)
    def addproba(self, table):
        self.table = table

    # return the size of random variable's domain
    def domainsize(self):
        return len(self.domain)

    # evaluate the state and return its correspond status in domain
    def evaluate(self, state):
        if state == self.name:
            return True
        elif state[1:] == self.name:
            return False
        elif state == "true":
            return True
        elif state == "false":
            return False

    def calProba(self, value, evidence):
        event = self.evidence_values(evidence)
        assert len(event) == len(self.parentNodes), "The evidence offered is not legal"
        for query in self.table.query:
            currvalue = query["state"]
            currevidence = query["evidence"]
            if currvalue == value and currevidence == event:
                return query["probability"]
        print("The evidence offered is not legal")

    def evidence_values(self, event):
        result = {}
        for key in self.parents:
            if key not in event:
                raise KeyError("Key absent in parentnodes")
            result[key] = event[key]
        return result

    def sample(self, event):
        """
        :param event: the observable evidence
        :return: the True or False randomly based on the event
        """
        return probability(self.calProba(True, event))

    @classmethod
    def normalize(cls, probdict):
        assert probdict
        summation = sum(probdict.values())
        for key in probdict:
            probdict[key] /= summation


# offer the Probability distribution of A
class Table:
    def __init__(self, state, given, items):
        self.state = state
        self.given = given
        self.processItem(items)

    # Process the data from xml file
    def processItem(self, items):
        if len(self.given) == 0:
            self.query = []
            for i, v in enumerate([eval(k) for k in items[0].split()]):
                currquery = {}
                currquery["state"] = self.state.kthproba(i)
                currquery["evidence"] = {}
                currquery["probability"] = v
                self.query.append(currquery)
        elif len(items) == 1:
            self.processOneLineItem(items)
        else:
            self.processNormalItems(items)

    # Process online item in xml file, like the definition tag in dog-problem-file
    # create the query
    def processOneLineItem(self, items):
        permutations = Table.getPermutation(self.given)
        values = [eval(i) for i in items[0].split()]
        size = len(values)
        assert size % self.state.domainsize() == 0
        self.query = []
        for i in range(len(permutations)):
            es = permutations[i]
            for v in range(self.state.domainsize()):
                self.query.append(createquery(self.state, v, self.given, es,
                                              values[i * self.state.domainsize() + v]))

    # process normal item, for example the definition tags in aima-alarm file
    # create the query
    def processNormalItems(self, items):
        items = [i.split() for i in items[1:]]
        self.query = []
        index = 0
        while index < len(items):
            evidence = items[index]
            probas = items[index + 1]
            for i in range(len(probas)):
                currquery = {}
                currquery["state"] = self.state.kthproba(i)
                currquery["probability"] = eval(probas[i])
                currquery["evidence"] = {str(self.given[v].name): self.given[v].evaluate(evidence[v])
                                         for v in range(len(evidence))}
                self.query.append(currquery)
            index += 2

        return 0

    @staticmethod
    # Get full permutation for the given evidence
    def getPermutation(argument):
        if len(argument) == 1:
            return [[i, ] for i in range(argument[0].domainsize())]
        start = argument[0]
        result = Table.getPermutation(argument[1:])
        newresult = []
        for i in range(start.domainsize()):
            for r in result:
                newresult.append([i, ] + r)
        return newresult

    def __repr__(self):
        return str(self.query)


# create a query data structure: in format:
# {"node":currentnode,"Evidence:evidence and their states,"probability":the probability}
def createquery(node, nodestate, evidence, evidencestate, proba):
    # for r in evidence:
    #     assert type(r) == rv
    nodestate = node.kthproba(nodestate)
    assert len(evidence) == len(evidencestate)
    newevidence = {}
    for i in range(len(evidence)):
        currnode = evidence[i]
        state = currnode.kthproba(evidencestate[i])
        newevidence[str(currnode.name)] = state
    query = {"state": nodestate, "evidence": newevidence, "probability": proba}
    return query
