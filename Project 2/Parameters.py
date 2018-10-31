# and operator
conjunction = "and"
# or operator
disjunction = "or"
# implies operator
implies = ">"
# equivelant operator
equals = "="
# not operator
negative = "~"
# unit
unit = "Identity"
# empty symbol, used in Resolution clause
empty = "Empty"



def conjunctionValue(args):
    return sum(args) == len(args)


def disconjunctionValue(args):
    return sum(args) > 0


def impliesValue(arg1, arg2):
    if arg1:
        return arg2
    return True


def equalsValue(arg1, arg2):
    return impliesValue(arg1, arg2) and impliesValue(arg2, arg1)


def negativeValue(arg1, arg2=None):
    return not arg1


def unitValue(arg1, arg2=None):
    return arg1

# store all operator evaluation function in a dictionary
# Make it easy for later sentence to call these functions
operatorValues = {}
operatorValues[conjunction] = conjunctionValue
operatorValues[disjunction] = disconjunctionValue
operatorValues[implies] = impliesValue
operatorValues[equals] = equalsValue
operatorValues[negative] = negativeValue
operatorValues[unit] = unitValue





