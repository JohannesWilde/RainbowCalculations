# -*- coding: utf-8 -*-

'''Class for storing a 2D point.'''

from TypeHelpers import TypeChecker
from Vector import Vector2D

class Point2D(TypeChecker):

    def __init__(self, x, y):
        TypeChecker.__init__(self)
        self.x = x
        self.y = y
        return

    def __str__(self):
        return '({x}, {y})'.format(x=self.x, y = self.y)

    def __repr__(self):
        return '{value} - Point2D at {address}'.format(value=str(self), address = hex(id(self)))

    def __add__(self, other):
        self.checkType(expectedType=Vector2D, value=other, exceptionMessage='Only Vectors can be added to points.')
        return Point2D(x=(self.x + other.x), y=(self.y + other.y))

    def __sub__(self, other):
        self.checkType(expectedType=Vector2D, value=other, exceptionMessage='Only Vectors can be added to points.')
        return self + -other

    def __neg__(self):
        return Point2D(x=(-self.x), y=(-self.y))
