

def checkAtMostOneNonNoneValue(valueList):
    noneOccurences = valueList.count(None)
    nonNoneOccurences = len(valueList) - noneOccurences
    return nonNoneOccurences <= 1


class PhysicalUnit(object):
    def __init__(self):
        return


# create getter and setter properties
if __name__ == '__main__':
    default = '''
    @property
    def {prefix}{unit}(self):
        return divideIfNotNone(self._value, MetricPrefix.{Prefix})

    @{prefix}{unit}.setter
    def {prefix}{unit}(self, value):
        self._value = multiplyIfNotNone(value, MetricPrefix.{Prefix})
        return
    '''
    unitname = 'meters'
    for prefix in ('', 'centi', 'milli', 'micro', 'nano', 'pico', 'kilo'):
        print(default.format(unit=unitname,
                             prefix=prefix,
                             Prefix=prefix.capitalize()))

    exit(0)