# -*- coding: utf-8 -*-

'''Class for storing an angle.'''

from math import pi

from TypeHelpers import NumberTypes, TypeChecker

class Angle(TypeChecker):

    FullCircleTurns = 1.
    FullCircleRadians = 2 * pi
    FullCircleDegrees = 360.

    def __init__(self, degrees=None, radians=None, turns=None):
        TypeChecker.__init__(self)
        arguments = (degrees, radians, turns)
        numberOfNonNoneArguments = len(arguments) - arguments.count(None)
        if numberOfNonNoneArguments != 1:
            raise ValueError('Expected exactly one non-None argument, got {numberOfNonNoneArguments}.'.format(numberOfNonNoneArguments=numberOfNonNoneArguments))

        if degrees is not None:
            self.degrees = degrees
        elif radians is not None:
            self.radians = radians
        elif turns is not None:
            self.turns = turns
        return

    @staticmethod
    def _convertFromTo(value, fromUnit, toUnit):
        return value / fromUnit * toUnit

    @staticmethod
    def radiansToDegrees(value):
        return Angle._convertFromTo(value=value, fromUnit=Angle.FullCircleRadians, toUnit=Angle.FullCircleDegrees)

    @staticmethod
    def degreesToRadians(value):
        return Angle._convertFromTo(value=value, fromUnit=Angle.FullCircleDegrees, toUnit=Angle.FullCircleRadians)

    @staticmethod
    def radiansToTurns(value):
        return Angle._convertFromTo(value=value, fromUnit=Angle.FullCircleRadians, toUnit=Angle.FullCircleTurns)

    @staticmethod
    def turnsToRadians(value):
        return Angle._convertFromTo(value=value, fromUnit=Angle.FullCircleTurns, toUnit=Angle.FullCircleRadians)

    @staticmethod
    def degreesToTurns(value):
        return Angle._convertFromTo(value=value, fromUnit=Angle.FullCircleDegrees, toUnit=Angle.FullCircleTurns)

    @staticmethod
    def turnsToDegrees(value):
        return Angle._convertFromTo(value=value, fromUnit=Angle.FullCircleTurns, toUnit=Angle.FullCircleDegrees)

    @property
    def degrees(self):
        return self.radiansToDegrees(self.radians)

    @degrees.setter
    def degrees(self, value):
        self.radians = self.degreesToRadians(value=value)
        return

    @property
    def radians(self):
        return self._value

    @radians.setter
    def radians(self, value):
        self._value = value
        return

    @property
    def turns(self):
        return self.radiansToTurns()

    @turns.setter
    def turns(self, value):
        self.radians = self.turnsToRadians(value=value)
        return

    def __str__(self):
        return '{degrees}°'.format(degrees=self.degrees)

    def __repr__(self):
        return '{value} - Angle at {address}'.format(value=str(self), address = hex(id(self)))

    def __add__(self, other):
        self.checkType(expectedType=Angle, value=other, exceptionMessage='Only Angles can be added to Angles.')
        return Angle(radians=(self.radians + other.radians))

    def __sub__(self, other):
        self.checkType(expectedType=Angle, value=other, exceptionMessage='Only Angles can be subtracted from Angles.')
        return (self + (-other))

    def __neg__(self):
        return Angle(radians=-self.radians)

    def __mul__(self, other):
        self.checkType(expectedType=NumberTypes, value=other, exceptionMessage='Angles can only be multiplied by numbers.')
        return Angle(radians=(self.radians * other))

    def __truediv__(self, other):
        self.checkType(expectedType=NumberTypes, value=other, exceptionMessage='Angles can only be multiplied by numbers.')
        return self * (1. / other)

    def __gt__(self, other):
        return self._value > other._value

    def __lt__(self, other):
        return self._value < other._value

    def __ge__(self, other):
        return self._value >= other._value

    def __le__(self, other):
        return self._value <= other._value

    def __ne__(self, other):
        return self._value != other._value

    def __eq__(self, other):
        return self._value == other._value

    def __bool__(self):
        return self._value is not None
