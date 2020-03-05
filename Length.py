# -*- coding: utf-8 -*-

'''Class for storing an lengths.'''

from TypeHelpers import NumberTypes, TypeChecker
from MetricPrefixes import MetricPrefix
from NoneHelpers import addIfNotNone, subtractIfNotNone, multiplyIfNotNone, divideIfNotNone, compareEqualIfNotNone, \
                        compareNotEqualIfNotNone, compareLessEqualIfNotNone, compareLessThanIfNotNone, \
                        compareGreaterEqualIfNotNone, compareGreaterThanIfNotNone
from PhysicalUnit import PhysicalUnit, checkAtMostOneNonNoneValue



class Length(TypeChecker, PhysicalUnit):

    def __init__(self, meters=None, centimeters=None, millimeters=None, micrometers=None, nanometers=None, kilometers=None):
        TypeChecker.__init__(self)
        PhysicalUnit.__init__(self)

        arguments = (kilometers, meters, centimeters, millimeters, micrometers, nanometers)
        prefixes = (MetricPrefix.Kilo, MetricPrefix.One, MetricPrefix.Centi, MetricPrefix.Milli, MetricPrefix.Micro, MetricPrefix.Nano)

        if not checkAtMostOneNonNoneValue(arguments):
            raise ValueError('At most only one non-None argument.')

        self._value = None
        for argument, prefix in zip(arguments, prefixes):
            if argument is not None:
                self._value = argument * prefix
                break
        return

    @property
    def meters(self):
        return self._value

    @meters.setter
    def meters(self, value):
        self._value = value
        return


    @property
    def centimeters(self):
        return divideIfNotNone(self._value, MetricPrefix.Centi)

    @centimeters.setter
    def centimeters(self, value):
        self._value = multiplyIfNotNone(value, MetricPrefix.Centi)
        return


    @property
    def millimeters(self):
        return divideIfNotNone(self._value, MetricPrefix.Milli)

    @millimeters.setter
    def millimeters(self, value):
        self._value = multiplyIfNotNone(value, MetricPrefix.Milli)
        return


    @property
    def micrometers(self):
        return divideIfNotNone(self._value, MetricPrefix.Micro)

    @micrometers.setter
    def micrometers(self, value):
        self._value = multiplyIfNotNone(value, MetricPrefix.Micro)
        return


    @property
    def nanometers(self):
        return divideIfNotNone(self._value, MetricPrefix.Nano)

    @nanometers.setter
    def nanometers(self, value):
        self._value = multiplyIfNotNone(value, MetricPrefix.Nano)
        return


    @property
    def picometers(self):
        return divideIfNotNone(self._value, MetricPrefix.Pico)

    @picometers.setter
    def picometers(self, value):
        self._value = multiplyIfNotNone(value, MetricPrefix.Pico)
        return


    @property
    def kilometers(self):
        return divideIfNotNone(self._value, MetricPrefix.Kilo)

    @kilometers.setter
    def kilometers(self, value):
        self._value = multiplyIfNotNone(value, MetricPrefix.Kilo)
        return


    def __str__(self):
        return '{value}m'.format(value=self.meters)

    def __repr__(self):
        return '{value} - Length at {address}'.format(value=str(self), address = hex(id(self)))

    def __add__(self, other):
        self.checkType(expectedType=Length, value=other, exceptionMessage='Only Lengths can be added to Lengths.')
        return Length(meters=addIfNotNone(self.meters, other.meters))

    def __sub__(self, other):
        self.checkType(expectedType=Length, value=other, exceptionMessage='Only Lengths can be subtracted from Lengths.')
        return Length(meters=subtractIfNotNone(self.meters, other.meters))

    def __neg__(self):
        return Length(meters=multiplyIfNotNone(self.meters, -1))

    def __mul__(self, other):
        self.checkType(expectedType=NumberTypes, value=other, exceptionMessage='Lengths can only be multiplied by numbers.')
        return Length(meters=multiplyIfNotNone(self.meters, other))

    def __truediv__(self, other):
        self.checkType(expectedType=NumberTypes, value=other, exceptionMessage='Lengths can only be multiplied by numbers.')
        return divideIfNotNone(self.meters, other.meters)

    def __lt__(self, other):
        self.checkType(expectedType=Length, value=other, exceptionMessage='Lengths can only be multiplied by numbers.')
        return compareLessThanIfNotNone(self, other.meters)

    def __le__(self, other):
        self.checkType(expectedType=Length, value=other, exceptionMessage='Lengths can only be multiplied by numbers.')
        return compareLessEqualIfNotNone(self.meters, other.meters)

    def __gt__(self, other):
        self.checkType(expectedType=Length, value=other, exceptionMessage='Lengths can only be multiplied by numbers.')
        return compareGreaterThanIfNotNone(self.meters, other.meters)

    def __ge__(self, other):
        self.checkType(expectedType=Length, value=other, exceptionMessage='Lengths can only be multiplied by numbers.')
        return compareGreaterEqualIfNotNone(self.meters, other.meters)

    def __eq__(self, other):
        self.checkType(expectedType=Length, value=other, exceptionMessage='Lengths can only be multiplied by numbers.')
        return compareEqualIfNotNone(self.meters, other.meters)

    def __ne__(self, other):
        self.checkType(expectedType=Length, value=other, exceptionMessage='Lengths can only be multiplied by numbers.')
        return compareNotEqualIfNotNone(self.meters, other.meters)

    def truth(self):
        return self._value is not None
