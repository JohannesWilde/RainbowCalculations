# -*- coding: utf-8 -*-

NumberTypes = (int, float)

class TypeChecker(object):

    @staticmethod
    def checkType(expectedType, value, exceptionMessage):
        if not isinstance(value, expectedType):
            raise TypeError \
                ('Incompatible type supplied [{type}]: {message}.'.format(type=type(value), message=exceptionMessage))
        return

    @staticmethod
    def checkNumber(value):
        return isinstance(value, NumberTypes)
