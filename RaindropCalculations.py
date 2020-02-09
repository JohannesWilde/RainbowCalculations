# -*- coding: utf-8 -*-

from math import sin, cos, tan, asin, atan
from Angle import Angle
from UnitCircleHelpers import unitCirclePointFromAngle

class RaindropCalculations(object):

    def __init__(self, refractiveIndexOuter, refractiveIndexInner, incidenceHeight):
        self.refractiveIndexOuter = refractiveIndexOuter
        self.refractiveIndexInner = refractiveIndexInner
        self.incidenceHeight = incidenceHeight
        return

    @property
    def n0(self):
        return self.refractiveIndexOuter

    @property
    def n1(self):
        return self.refractiveIndexInner

    @property
    def h0(self):
        return self.incidenceHeight

    @property
    def alpha0(self):
        return Angle(radians=asin(self.h0))

    # beta
    @property
    def pointBeta(self):
        '''Incidence.'''
        return unitCirclePointFromAngle(self.alpha0)

    @property
    def beta0(self):
        return self.alpha0

    @property
    def beta1(self):
        return Angle(radians=asin(self.n0/self.n1*self.h0))

    @property
    def epsilon0(self):
        return (self.beta0 - self.beta1)


    # gamma
    @property
    def pointGamma(self):
        '''Reflection.'''

        return

    # delta
    @property
    def pointDelta(self):
        '''Emergence.'''

        return
