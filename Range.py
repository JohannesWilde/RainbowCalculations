

class Range(object):

    def __init__(self, min, max):
        self.min = min
        self.max = max
        return

    def checkValueInRange(self, value):
        return (value <= self.max) and (value >= self.min)

    def __str__(self):
        return '({min}, {max})'.format(min=self.min, max=self.max)
