# -*- coding: utf-8 -*-

from math import cos, sin

from Point import Point2D

def unitCirclePointFromAngle(angle):
    return Point2D(x=cos(angle.radians), y=sin(angle.radians))