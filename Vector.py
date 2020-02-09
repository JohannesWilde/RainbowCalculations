# -*- coding: utf-8 -*-

'''Class for storing a 2D vector.'''

from TypeHelpers import NumberTypes

class Vector2D(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        return

    @staticmethod
    def _checkType(expectedType, value, exceptionMessage):
        if not isinstance(value, expectedType):
            raise TypeError('Incompatible type supplied [{type}]: {message}.'.format(type=type(value), message=exceptionMessage))
        return

    def __str__(self):
        return '({x}, {y})'.format(x=self.x, y = self.y)

    def __repr__(self):
        return '{value} - Vector2D at {address}'.format(str(self), address = hex(id(self)))

    def __add__(self, other):
        self._checkType(Vector2D, other, 'Only Vectors can be added to Vectors.')
        return Vector2D(x=(self.x + other.x), y=(self.y + other.y))

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        self._checkType(NumberTypes, other, 'Vectors can only be multiplied by scalars.')
        return Vector2D(x=(self.x * other), y=(self.y * other))

    def __truediv__(self, other):
        self._checkType(NumberTypes, other, 'Vectors can only be multiplied by scalars.')
        return self.__mul__(1. / other)

    def __neg__(self):
        return ((-1) * self)