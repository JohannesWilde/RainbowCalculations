# -*- coding: utf-8 -*-

'''Class for rotating Vector2D.'''

from math import cos, sin

from Angle import Angle
from TypeHelpers import NumberTypes, TypeChecker
from Vector import Vector2D

class Rotate2D(TypeChecker):

    def __init__(self, angle):
        TypeChecker.__init__(self)
        self.checkType(Angle, angle, 'An Angle must be supplied for the rotation.')
        self.angle = angle
        return

    def __str__(self):
        return '{angle}'.format(angle=self.angle)

    def __repr__(self):
        return '{value} - Rotate2D at {address}'.format(value=str(self), address = hex(id(self)))

    def __mul__(self, other):
        self.checkType(Vector2D, other, 'Rotate2D can only multiply Vector2Ds.')
        cosAngle = cos(self.angle)
        sinAngle = sin(self.angle)
        return Vector2D(x=(cosAngle * other.x - sinAngle * other.y),
                        y=(sinAngle * other.x + cosAngle * other.y))

    def __neg__(self):
        return Rotate2D(angle=-self.angle)