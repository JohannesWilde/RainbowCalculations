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
    PowerTE = (0,.5,0)
    PowerTM = (.5,0,0)
    PowerTETMmixed = (0,0,.5)

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
    numberOfPoints = 1001

    refractiveIndexOuter = 1.
    refractiveIndexInner = 1.5

    eta0s = list()
    powersTEheights= list()
    powersTMheights= list()
    heights = linspace(-1,1,numberOfPoints)
    for height in heights:
        raindropCalculations = RaindropCalculations(refractiveIndexInner=refractiveIndexInner,
                                                    refractiveIndexOuter=refractiveIndexOuter,
                                                    incidenceHeight=height)
        eta0s.append(raindropCalculations.eta0)
        powersTEheights.append(raindropCalculations.transmittedPowerTransversalElectric)
        powersTMheights.append(raindropCalculations.transmittedPowerTransversalMagnetic)

    # use linear interpolator to reverse this relation height -> eta0 [is not bijective!]
    heightsAuEta0sRadiansPoints = []
    for heightAu, eta0 in zip(heights, eta0s):
        heightsAuEta0sRadiansPoints.append(Point(x=heightAu, y=eta0.radians))

    linearInterpolatorHeightsAuEta0sRadians = StepwiseLinearFunctionInterpolator(listOfPoints=heightsAuEta0sRadiansPoints)

    # determine output angles as new dependend parameter
    eta0Min = min(eta0s)
    eta0Max = max(eta0s)
    eta0sRadiansForCalculation = linspace(eta0Min.radians, eta0Max.radians, numberOfPoints)

    powersTE = list()
    powersTM = list()
    for eta0Radians in eta0sRadiansForCalculation:
        # determine all input heights corresponding to the eta0Radians
        correspondingHeights = list()
        index = -1
        while True:
            index += 1
            correspondingHeight = linearInterpolatorHeightsAuEta0sRadians.where(y=eta0Radians, index=index)
            if correspondingHeight is not None and (-1. <= correspondingHeight <= 1.):
                correspondingHeights.append(correspondingHeight)
            else:
                break

        # now add up all power from potentially different input heights
        powerTE = 0.
        powerTM = 0.
        for correspondingHeight in correspondingHeights:
            raindropCalculations = RaindropCalculations(refractiveIndexInner=refractiveIndexInner,
                                                        refractiveIndexOuter=refractiveIndexOuter,
                                                        incidenceHeight=correspondingHeight)
            powerTE += raindropCalculations.transmittedPowerTransversalElectric
            powerTM += raindropCalculations.transmittedPowerTransversalMagnetic

        powersTE.append(powerTE)
        powersTM.append(powerTM)



    figure, (axis0, axis1, axis2) = plt.subplots(3,1)
    axis0.cla()
    axis1.cla()
    axis2.cla()

    figure.suptitle('Refractive indices inner / outer = {relation}'.format(
        height=height,
        relation=refractiveIndexInner / refractiveIndexOuter
    ))

    eta0sRadians = tuple(eta0.radians for eta0 in eta0s)
    axis0.plot(heights, eta0sRadians, color=ObjectColor.Lightray)
    axis0.set_xlabel('height [nu]')  # normalize unit
    axis0.set_ylabel('eta0 [radians]')

    axis1.plot(heights, powersTEheights, color=ObjectColor.PowerTE, label='TE')
    axis1.plot(heights, powersTMheights, color=ObjectColor.PowerTM, label='TM')
    axis1.plot(heights, tuple((te + tm)/2 for te, tm in zip(powersTEheights, powersTMheights)), color=ObjectColor.PowerTETMmixed, label='(TE+TM)/2')
    axis1.set_xlabel('height [nu]')  # normalize unit
    axis1.set_ylabel('transmitted power [nu]')
    legend1 = axis1.legend(loc='upper center')

    axis2.plot(eta0sRadiansForCalculation, powersTE, color=ObjectColor.PowerTE, label='TE')
    axis2.plot(eta0sRadiansForCalculation, powersTM, color=ObjectColor.PowerTM, label='TM')
    axis2.plot(eta0sRadiansForCalculation, tuple((te + tm)/2 for te, tm in zip(powersTE, powersTM)), color=ObjectColor.PowerTETMmixed, label='(TE+TM)/2')
    axis2.set_xlabel('eta0 [radians]')
    axis2.set_ylabel('transmitted power [nu]')  # normalize unit
    legend2 = axis2.legend(loc='upper right')

    plt.show()

    exit(0)
