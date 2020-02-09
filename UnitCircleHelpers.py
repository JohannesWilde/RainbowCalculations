# -*- coding: utf-8 -*-

from math import cos, sin

from Point import Point2D

def unitCirclePointFromAngle(angle):
    return Point2D(x=cos(angle.radians), y=sin(angle.radians))

def otherIntersectionOf(pointFrom, direction):
    '''pointFrom must lie on the unit cirecle and direction must be normalized.'''
    tempVal = 2 * (pointFrom.x * direction.x + pointFrom.y * direction.y)
    return Point2D(x=(pointFrom.x - direction.x * tempVal),
                   y=(pointFrom.y - direction.y * tempVal))