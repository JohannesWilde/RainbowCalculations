# -*- coding: utf-8 -*-

'''Class for storing a 2D point.'''

from Vector import Vector2D

class Point2D(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        return

    def __str__(self):
        return '({x}, {y})'.format(x=self.x, y = self.y)

    def __repr__(self):
        return '{value} - Point2D at {address}'.format(str(self), address = hex(id(self)))

    def __add__(self, other):
        if isinstance(other, Vector2D):
            addition = Point2D(x=(self.x + other.x), y=(self.y + other.y))
        else:
            raise TypeError('Incompatible type supplied - only Vectors can be added to points [type].'.format(type=type(other)))
        return addition

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            addition = Point2D(x=(self.x + other.x), y=(self.y + other.y))
        else:
            raise TypeError('Incompatible type supplied - only Vectors can be added to points [type].'.format(type=type(other)))
        return addition

    def __neg__(self):
        return Point2D(x=(-self.x), y=(-self.y))
