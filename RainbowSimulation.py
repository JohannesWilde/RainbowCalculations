# -*- coding: utf-8 -*-

'''Python script to calculate the angle a light ray is reflected
    to in a perfect sphere if it enters at an angle - assuming
    1 internal reflection only.'''

from matplotlib import pyplot as plt
from math import asin
from os import mkdir, path
from Angle import Angle
from LinearInterpolation import StepwiseLinearFunctionInterpolator
from Point import Point2D as Point
from RaindropCalculations import RaindropCalculations
from numpy import linspace


class ObjectZorder(object):
    # bigger values are to the front
    Raindrop = 1
    MeetingPoints = 2
    Lightray = 3

class ObjectColor(object):
    MeetingPoints = (0.,.8,0.)
    Lightray = (.8,0.,0.)

def createFigure(calculation,
                 directory):

    # get plot
    axis = plt.gca()
    axis.cla()

    axis.set_xlim((-1.5, 1.5))
    axis.set_ylim((-1.5, 1.5))
    axis.set_aspect('equal')

    plt.title('Incident height = {height}, refractive indices inner / outer = {relation}'.format(
        height=calculation.incidenceHeight,
        relation=refractiveIndexInner / refractiveIndexOuter
    ))

    # draw sphere
    colorValue = 2. / (1. + refractiveIndexInner / refractiveIndexOuter)
    sphereBackgroundColor = (colorValue, colorValue, colorValue)

    raindrop = plt.Circle((0, 0), 1, color=sphereBackgroundColor, fill=True, zorder=ObjectZorder.Raindrop)

    axis.add_artist(raindrop)

    # show light ray - incident
    pointBeta = calculation.pointBeta
    plt.scatter(pointBeta.x, pointBeta.y, marker='.', zorder=ObjectZorder.MeetingPoints,
                color=ObjectColor.MeetingPoints)
    plt.plot((2, pointBeta.x), (pointBeta.y, pointBeta.y), color=ObjectColor.Lightray)

    # refracted
    pointGamma = calculation.pointGamma
    plt.scatter(pointGamma.x, pointGamma.y, marker='.', zorder=ObjectZorder.MeetingPoints,
                color=ObjectColor.MeetingPoints)
    plt.plot((pointBeta.x, pointGamma.x), (pointBeta.y, pointGamma.y), color=ObjectColor.Lightray)

    # mirrored
    pointDelta = calculation.pointDelta
    plt.scatter(pointDelta.x, pointDelta.y, marker='.', zorder=ObjectZorder.MeetingPoints,
                color=ObjectColor.MeetingPoints)
    plt.plot((pointGamma.x, pointDelta.x), (pointGamma.y, pointDelta.y), color=ObjectColor.Lightray)

    # emerging
    directionEmerging = calculation.direction3
    temp = (2. - pointDelta.x) / directionEmerging.x  # assure it goes until x = 2
    pointEnd = pointDelta + directionEmerging * temp
    plt.plot((pointDelta.x, pointEnd.x), (pointDelta.y, pointEnd.y), color=ObjectColor.Lightray)

    # make plot visible
    plt.savefig(fname='{directory}/result_i{indicesRelation:.2F}_h{height:.2F}.png'.format(
        indicesRelation=(refractiveIndexInner / refractiveIndexOuter),
        height=calculation.incidenceHeight,
        directory=directory
    ))

    return


if __name__ == '__main__':
    wavelengthNm = 600
    numberOfPoints = 101


    refractiveIndexOuter = 1.
    refractiveIndexInner = 1.5

    # subdirectory = 'calculations/{wavelengthNm:04F}'.format(wavelengthNm=123.234)
    # if not path.exists(subdirectory):
    #     mkdir(subdirectory)

    eta0s = list()
    powerTE = list()
    powerTM = list()
    heights = linspace(0,1,numberOfPoints)
    for height in heights:

        raindropCalculations = RaindropCalculations(refractiveIndexInner=refractiveIndexInner,
                                                    refractiveIndexOuter=refractiveIndexOuter,
                                                    incidenceHeight=height)

        eta0s.append(raindropCalculations.eta0)

    heightsAuEta0sRadiansPoints = []
    for heightAu, eta0 in zip(heights, eta0s):
        heightsAuEta0sRadiansPoints.append(Point(x=heightAu, y=eta0.degrees))

    linearInterpolatorHeightsAuEta0sRadians = StepwiseLinearFunctionInterpolator(listOfPoints=heightsAuEta0sRadiansPoints)
    bla = []
    blub = []
    for h in linspace(0,1,301):
        bla.append(h)
        blub.append(linearInterpolatorHeightsAuEta0sRadians.at(x=h))

        # powerTE.append(raindropCalculations.transmittedPowerTransversalElectric)
        # powerTM.append(raindropCalculations.transmittedPowerTransversalMagnetic)
        #
        # # createFigure(calculation=raindropCalculations,
        # #              directory='calculations')



    figure, (axis0, axis1) = plt.subplots(2,1, sharex=True)
    axis0.cla()
    axis1.cla()

    figure.suptitle('Incident height = {height}, refractive indices inner / outer = {relation}'.format(
        height=height,
        relation=refractiveIndexInner / refractiveIndexOuter
    ))

    eta0sDegrees = tuple(eta0.degrees for eta0 in eta0s)
    axis0.plot(heights, eta0sDegrees, color=ObjectColor.Lightray)
    axis0.plot(bla, blub, 'o')
    # axis0.set_xlabel('height')
    axis0.set_ylabel('eta0')

    # axis1.plot(heights, powerTE, color=(.5,0,0))
    # axis1.plot(heights, powerTM, color=(0,.5,0))
    # axis1.plot(heights, tuple((te + tm)/2 for te, tm in zip(powerTE, powerTM)))
    # axis1.set_xlabel('height')
    # axis1.set_ylabel('transmitted power')

    plt.show()

    exit(0)
