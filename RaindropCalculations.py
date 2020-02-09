# -*- coding: utf-8 -*-

from math import sin, cos, tan, asin, atan
from Angle import Angle
from UnitCircleHelpers import unitCirclePointFromAngle

class RaindropCalculations(object):

    def __init__(self, refractiveIndexOuter, refractiveIndexInner, incidenceHeight):
        self.refractiveIndexOuter = refractiveIndexOuter
        self.refractiveIndexInner = refractiveIndexInner
        self.incidenceHeigth = incidenceHeight
        return

    def getIncidencePoint(self):
        alpha0 = Angle(radians=asin(self.incidenceHeigth))
        return unitCirclePointFromAngle(alpha0)
