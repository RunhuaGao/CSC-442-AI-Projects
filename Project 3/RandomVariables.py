class rv:
    def __init__(self, name, domain):
        self.name = name
        self.domain = [self.evalstate(k) for k in domain]
        self.netproba = None
        self.parentNodes = []

    def __eq__(self, other):
        return other.name == self.name

    def __repr__(self):
        return self.name

    def addParentNode(self, parentnode):
        assert type(parentnode) == rv
        self.parentNodes.append(parentnode)

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

    # return a query component by k
    def state(self, k):
        return {self.name: self.kthproba(k)}

    # evaluate the state and return its correspond status in domain
    def evalstate(self, state):
        if state == self.name:
            return True
        elif state[1:] == self.name:
            return False
        elif state == "true":
            return True
        elif state == "false":
            return False


# Table Item, for a specific variable A, Given evidence,
# offer the Probability distribution of A
class Table:
    def __init__(self, state, given, items):
        self.state = state
        self.given = given
        self.processItem(items)

    def addItem(self, evidence, proba):
        currentitem = [evidence, proba]
        self.item.append(currentitem)

    # Process the data from xml file
    def processItem(self, items):
        if len(self.given) == 0:
            self.query = []
            for i, v in enumerate([eval(k) for k in items[0].split()]):
                currquery = {}
                currquery["node"] = self.state.state(i)
                currquery["evidence"] = None
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
                currquery["node"] = self.state.state(i)
                currquery["probability"] = eval(probas[i])
                currquery["evidence"] = {self.given[v].name: self.given[v].evalstate(evidence[v])
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
    assert type(node) == rv, "node is %s" % node
    for r in evidence:
        assert type(r) == rv
    node = node.state(nodestate)
    assert len(evidence) == len(evidencestate)
    newevidence = {}
    for i in range(len(evidence)):
        currnode = evidence[i]
        state = currnode.kthproba(evidencestate[i])
        newevidence[currnode.name] = state
    query = {"node": node, "evidence": newevidence, "probability": proba}
    return query
