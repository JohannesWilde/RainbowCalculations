

def lambdaIfNotNone(lambdaFunction, **kwargs):
    result = None
    if not any(value is None for value in kwargs.values()):
        result = lambdaFunction(**kwargs)
    return result


def addIfNotNone(value0, value1):
    return lambdaIfNotNone(lambdaFunction=lambda value0, value1: value0 + value1, value0=value0, value1=value1)

def subtractIfNotNone(value0, value1):
    return lambdaIfNotNone(lambdaFunction=lambda value0, value1: value0 - value1, value0=value0, value1=value1)

def multiplyIfNotNone(value0, value1):
    return lambdaIfNotNone(lambdaFunction=lambda value0, value1: value0 * value1, value0=value0, value1=value1)

def divideIfNotNone(value0, value1):
    return lambdaIfNotNone(lambdaFunction=lambda value0, value1: value0 / value1, value0=value0, value1=value1)

def compareLessEqualIfNotNone(value0, value1):
    return lambdaIfNotNone(lambdaFunction=lambda value0, value1: value0 <= value1, value0=value0, value1=value1)

def compareLessThanIfNotNone(value0, value1):
    return lambdaIfNotNone(lambdaFunction=lambda value0, value1: value0 < value1, value0=value0, value1=value1)

def compareGreaterEqualIfNotNone(value0, value1):
    return lambdaIfNotNone(lambdaFunction=lambda value0, value1: value0 >= value1, value0=value0, value1=value1)

def compareGreaterThanIfNotNone(value0, value1):
    return lambdaIfNotNone(lambdaFunction=lambda value0, value1: value0 > value1, value0=value0, value1=value1)

def compareEqualIfNotNone(value0, value1):
    return lambdaIfNotNone(lambdaFunction=lambda value0, value1: value0 == value1, value0=value0, value1=value1)

def compareNotEqualIfNotNone(value0, value1):
    return lambdaIfNotNone(lambdaFunction=lambda value0, value1: value0 != value1, value0=value0, value1=value1)


