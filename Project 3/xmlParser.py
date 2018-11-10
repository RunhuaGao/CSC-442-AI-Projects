file1 = "aima-alarm.xml"
file2 = "aima-wet-grass.xml"
file3 = "dog-problem.xml"
va = "VARIABLE"
name = "NAME"
outcome = "OUTCOME"
state = "FOR"
give = "GIVEN"
table = "TABLE"
files = [file1, file2, file3]
import xml.dom.minidom
from RandomVariables import rv, Table


# return a parser document root element
def parser(file):
    return xml.dom.minidom.parse(file).documentElement


# return all the random variables in class rv
def getVariables(root):
    # parse variable tag
    def parseVariableTag(tag):
        global name
        variablename = tag.getElementsByTagName(name)[0].firstChild.data
        domain = []
        for k in tag.getElementsByTagName(outcome):
            domain.append(k.firstChild.data)
        return variablename, rv(variablename, domain)

    vas = {}
    for tag in root.getElementsByTagName(va):
        name, randomvariable = parseVariableTag(tag)
        vas[name] = randomvariable
    return vas


def getDefinitions(root, rvs):
    def parseDefinitionTag(tag):
        statename = tag.getElementsByTagName(state)[0].firstChild.data
        evidencerv = []
        for k in tag.getElementsByTagName(give):
            evidencerv.append(k.firstChild.data)
        tableitems = parseTableTag(tag.getElementsByTagName(table)[0])
        curtable = Table(rvs[statename], [rvs[n] for n in evidencerv], tableitems)
        rvs[statename].addproba(curtable)
        [rvs[statename].addParentNode(rvs[n]) for n in evidencerv]

    definitions = []
    for i in root.getElementsByTagName("DEFINITION"):
        definitions.append(parseDefinitionTag(i))
    return definitions


# parse the Table tag
def parseTableTag(tag):
    tableitems = []
    for node in tag.childNodes:
        tableitems.append(node.data)
    return parseTable(tableitems)


# parse the Table()
def parseTable(tableitems):
    result = []
    for item in tableitems:
        value = item.strip()
        if value:
            result.append(value)
    return result


# main function, build the node graph from xml file,return all nodes
def parseFile(filename):
    root = parser(filename)
    rvs = getVariables(root)
    getDefinitions(root, rvs)
    return rvs


for file in files:
    rvs = parseFile(file)
    for r in rvs.values():
        print(r.name)
        print(r.parentNodes)
        for q in r.table.query:
            print(q)
    print("%s has been parsed\n\n"%file)