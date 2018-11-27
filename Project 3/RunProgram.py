import sys
import os
from xmlParser import parseFile
def processInput(args):
    assert len(args) >=3
    filename = args[1]
    assert filename in os.listdir('.'),"Could not find the xml file"
    net = parseFile(filename)
    queryname = args[2]
    index = 3
    evidence = {}
    while index < len(args):
        key,value = str(args[index]),True if args[index+1]=="T" else False
        evidence[key] = value
        index+=2
    return net,queryname,evidence


