# -*- coding: utf-8 -*-

'''Class for storing an angle.'''

from math import pi

class Angle(object):

    FullCircleTurns = 1.
    FullCircleRadians = 2 * pi
    FullCircleDegrees = 360.

    def __init__(self, degrees=None, radians=None, turns=None):
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
        return '{value} - Angle at {address}'.format(str(self), address = hex(id(self)))
