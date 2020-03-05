# -*- coding: utf-8 -*-

class LinearInterpolator(object):

    def __init__(self, point0, point1):
        if point0.x == point1.x:
            raise ValueError('Can\'t linearly interpolate between points from the same x-value [{point0}, {point1}]'.format(point0=point0, point1=point1))
        self._acclivity = (point1.y - point0.y) / (point1.x - point0.x)
        self._offset = (point1.x * point0.y - point0.x * point1.y) / (point1.x - point0.x)
        return

    @property
    def acclivity(self):
        return self._acclivity

    @property
    def offset(self):
        return self._offset

    def at(self, x):
        return self.acclivity * x + self.offset

    def where(self, y):
        if self.acclivity == 0:
            raise ValueError('Can\'t determine a unique x for a constant function [{function}]'.format(function=self))
        return ((y - self.offset) / self.acclivity)

    def __str__(self):
        return 'y = {acclivity} * x + {offset}'.format(acclivity=self.acclivity, offset=self.offset)

    def __repr__(self):
        return '{value} - LinearInterpolator at {address}'.format(value=str(self), address = hex(id(self)))
