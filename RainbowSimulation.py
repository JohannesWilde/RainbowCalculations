# -*- coding: utf-8 -*-

'''Python script to calculate the angle a light ray is reflected
    to in a perfect sphere if it enters at an angle - assuming
    1 internal reflection only.'''

from matplotlib import pyplot as plt
from math import floor
from os import mkdir
from Angle import Angle
from FresnelCoefficients import FresnelCoefficients, Medium
from IncidentPowerProfile import powerIncidentDensityProfile
from Length import Length
from LinearInterpolation import StepwiseLinearFunctionInterpolator
from Point import Point2D as Point
from RaindropCalculations import RaindropCalculations
from RefractiveIndex import RefractiveIndex2007DaimonMasumura20CWater as RefractiveIndexWater
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

def stepwiseLinearInterpolatorFromArrays(xList, yList):
    listOfPoints = list()
    for x, y in zip(xList, yList):
        listOfPoints.append(Point(x=x, y=y))
    return StepwiseLinearFunctionInterpolator(listOfPoints=listOfPoints)


def transformSurjectiveRelation(oldXs, newXsOldXs, oldYsOldXsList, numberOfPoints, newXValidityCheck):
    # use linear interpolator to reverse the relation oldXs -> newXs [which is potentially surjective!]
    linearInterpolatorOldXsNewXs = stepwiseLinearInterpolatorFromArrays(xList=oldXs, yList=newXsOldXs)
    linearInterpolatorsOldXsOldYs = tuple(stepwiseLinearInterpolatorFromArrays(xList=oldXs, yList=oldYsOldXs) for oldYsOldXs in oldYsOldXsList)

    # determine output angles as new dependent parameter
    newXsMin = min(newXsOldXs)
    newXsMax = max(newXsOldXs)
    newXs = linspace(newXsMin, newXsMax, numberOfPoints)

    newYsNewXsList = tuple(list() for _ in oldYsOldXsList)  # create as many empty lists as there are lists in oldYsOldXsList
    for newX in newXs:
        # determine all input heights corresponding to the eta0Radians
        correspondingOldXs = list()
        index = -1
        while True:
            index += 1
            correspondingOldX = linearInterpolatorOldXsNewXs.where(y=newX, index=index)
            if correspondingOldX is not None and newXValidityCheck(correspondingOldX):
                correspondingOldXs.append(correspondingOldX)
            else:
                break

        for newYsNewXs, linearInterpolatorOldXsOldYs in zip(newYsNewXsList, linearInterpolatorsOldXsOldYs):
            # now add up all power density from potentially different input heights saled by their respective transmittance/reflectance
            newYNewX = 0.
            for correspondingOldX in correspondingOldXs:
                newY = linearInterpolatorOldXsOldYs.at(x=correspondingOldX)
                if newY is not None:
                    newYNewX += newY

            newYsNewXs.append(newYNewX)

    return newXs, newYsNewXsList

def findMaxInFirstHalf(xs, ys):
    maxY = max(ys[0:floor(len(ys) / 2)])
    xMaxY = xs[ys.index(maxY)]
    return Point(x=xMaxY, y=maxY)

if __name__ == '__main__':
    numberOfPoints = 1001
    numberOfWavelengths = 1

    eta0sExtrema = \
        {'geometrical': list(),
         'TEinternal': list(),
         'TMinternal': list(),
         'TeTmInternal': list(),}

    # visible spectrum
    wavelengths = tuple(Length(nanometers=value) for value in linspace(start=380, stop=740, num=numberOfWavelengths))

    plotDirectory = 'calculations3'
    try:
        mkdir(plotDirectory)
    except FileExistsError:
        # directory already exists
        pass

    print('Calculating for wavelength:')
    for wavelength in wavelengths:
        print('\r{wavelength}'.format(wavelength=wavelength), end='')

        refractiveIndexOuter = 1.
        refractiveIndexInner = RefractiveIndexWater().refractiveIndex(wavelength=wavelength)

        # scale power from dH to deta
        supersampling = 5 # must be grater than 1
        heightsSupersampled = linspace(-1, 1, numberOfPoints*supersampling)
        eta0sInternalSupersampled = list()
        powerIncidenceDensityHeight = list()
        for height in heightsSupersampled:
            raindropCalculations = RaindropCalculations(refractiveIndexInner=refractiveIndexInner,
                                                        refractiveIndexOuter=refractiveIndexOuter,
                                                        incidenceHeight=height)
            eta0sInternalSupersampled.append(raindropCalculations.eta0Internal.radians)
            powerIncidenceDensityHeight.append(powerIncidentDensityProfile(height))

        heights = list()
        powerIncidenceDensityEtaInternal = list()
        dH = heightsSupersampled[1] - heightsSupersampled[0]
        deltaH = supersampling * dH
        for index in range(numberOfPoints):
            tmpHeights = heightsSupersampled[index*supersampling:(index+1)*supersampling]
            tmpPowerIncidenceDensityHeight = powerIncidenceDensityHeight[index*supersampling:(index+1)*supersampling]

            integratedPower = dH * sum(tmpPowerIncidenceDensityHeight)

            tmpEta0sInternal = eta0sInternalSupersampled[index*supersampling:(index+1)*supersampling]
            deltaEtaInternal = max(tmpEta0sInternal) - min(tmpEta0sInternal)
            powerIncidenceDensityEtaInternal.append(integratedPower/deltaEtaInternal)

            heights.append(sum(tmpHeights) / supersampling)  # use average

        # fig, (plt0, plt1) = plt.subplots(2,1)
        # plot = plt0
        # plot.plot(heightsSupersampled, eta0sInternalSupersampled)
        # plot.plot(heightsSupersampled, powerIncidenceDensityHeight)
        # plot = plt1
        # plot.plot(heights, powerIncidenceDensityEtaInternal)
        # plt.show()

        del dH, deltaH, heightsSupersampled, eta0sInternalSupersampled, powerIncidenceDensityHeight, \
            integratedPower, tmpEta0sInternal, deltaEtaInternal


        # powers and eta0 dependent on incidence height
        eta0sInitial = list()
        powersTEheightsInternal= list()
        powersTMheightsInternal= list()
        for height in heights:
            raindropCalculations = RaindropCalculations(refractiveIndexInner=refractiveIndexInner,
                                                        refractiveIndexOuter=refractiveIndexOuter,
                                                        incidenceHeight=height)
            eta0sInitial.append(raindropCalculations.eta0Internal)
            powersTEheightsInternal.append(raindropCalculations.transmittedPowerTransversalElectric)
            powersTMheightsInternal.append(raindropCalculations.transmittedPowerTransversalMagnetic)
        del raindropCalculations


        # combine height->eta0 and power-transmittance
        powerExcidenceDensityHeightsInternalTE = tuple(powerDensity * transmittancePercentage for powerDensity, transmittancePercentage in zip(powerIncidenceDensityEtaInternal, powersTEheightsInternal))
        powerExcidenceDensityHeightsInternalTM = tuple(powerDensity * transmittancePercentage for powerDensity, transmittancePercentage in zip(powerIncidenceDensityEtaInternal, powersTMheightsInternal))

        eta0sExcidenceRadians, (powerExcidenceDensityEta0sInternalTE, powerExcidenceDensityEta0sInternalTM) = \
            transformSurjectiveRelation(
                oldXs=heights,
                newXsOldXs=tuple(eta0.radians for eta0 in eta0sInitial),
                oldYsOldXsList=(powerExcidenceDensityHeightsInternalTE, powerExcidenceDensityHeightsInternalTM),
                numberOfPoints=numberOfPoints,
                newXValidityCheck=lambda x: (-1. <= x <= 1.))

        # fig, (plt0, plt1) = plt.subplots(2,1)
        # plot = plt0
        # plot.plot(heights, powerExcidenceDensityHeightsInternalTE, label='TE-i(h)')
        # plot.plot(heights, powerExcidenceDensityHeightsInternalTM, label='TM-i(h)')
        # plot.set_xlabel('height')
        # plot.set_ylabel('power excidence')
        # plot.legend(loc='upper center')
        # plot = plt1
        # plot.plot(eta0sRadians, powerExcidenceDensityEta0sInternalTE, label='TE-i(eta)')
        # plot.plot(eta0sRadians, powerExcidenceDensityEta0sInternalTM, label='TM-i(eta)')
        # plot.set_xlabel('eta')
        # plot.set_ylabel('power excidence')
        # plot.legend(loc='upper center')
        # plt.show()

        # assume even mix of TE and TM polrization [non-polarized light]
        powerExcidenceDensityEta0sInternalTETM = tuple((tmp0 + tmp1) / 2. for tmp0, tmp1 in zip(powerExcidenceDensityEta0sInternalTE, powerExcidenceDensityEta0sInternalTM))
        powersTETMheightsInternal = tuple((tmp0 + tmp1) / 2. for tmp0, tmp1 in zip(powersTEheightsInternal, powersTMheightsInternal))

        # plot all relations
        figure, (axis0, axis1, axis2) = plt.subplots(3, 1)

        figure.suptitle('Refractive indices inner / outer = {relation}'.format(
            relation=refractiveIndexInner / refractiveIndexOuter
        ))

        axis = axis0
        eta0sInitialDegree = tuple(eta0.degrees for eta0 in eta0sInitial)
        axis.plot(heights, eta0sInitialDegree, color=ObjectColor.Lightray)
        axis.set_xlabel('height [nu]')  # normalize unit
        axis.set_ylabel('eta0 [°]')

        axis = axis1
        axis.plot(heights, powersTEheightsInternal, color=ObjectColor.PowerTE, label='TE-i')
        axis.plot(heights, powersTMheightsInternal, color=ObjectColor.PowerTM, label='TM-i')
        axis.plot(heights, powersTETMheightsInternal, color=ObjectColor.PowerTETMmixed, label='(TE-i+TM-i)/2')
        axis.set_xlabel('height [nu]')  # normalize unit
        axis.set_ylabel('transmitted power [nu]')
        legend1 = axis.legend(loc='upper center')

        axis = axis2
        eta0sExcidenceDegree = tuple(Angle.radiansToDegrees(angle) for angle in eta0sExcidenceRadians)
        axis.plot(eta0sExcidenceDegree, powerExcidenceDensityEta0sInternalTE, color=ObjectColor.PowerTE, label='TE-i')
        axis.plot(eta0sExcidenceDegree, powerExcidenceDensityEta0sInternalTM, color=ObjectColor.PowerTM, label='TM-i')
        axis.plot(eta0sExcidenceDegree, powerExcidenceDensityEta0sInternalTETM, color=ObjectColor.PowerTETMmixed, label='(TE-i+TM-i)/2')
        axis.set_xlabel('eta0 [°]')
        axis.set_ylabel('transmitted power [nu]')  # normalize unit
        legend4 = axis.legend(loc='upper right')

        plt.savefig(fname='{directory}/results_{wavelength:.2F}.png'.format(
            wavelength=wavelength.nanometers,
            directory=plotDirectory
        ), dpi=300)
        plt.close(figure)
        # plt.show()

        # geometric local extremum of eta0 relative to incidence height
        eta0sExtrema['geometrical'].append(min(eta0sInitial))
        eta0sExtrema['TEinternal'].append(Angle(radians=findMaxInFirstHalf(xs=eta0sExcidenceRadians, ys=powerExcidenceDensityEta0sInternalTE).x))
        eta0sExtrema['TMinternal'].append(Angle(radians=findMaxInFirstHalf(xs=eta0sExcidenceRadians, ys=powerExcidenceDensityEta0sInternalTM).x))
        eta0sExtrema['TeTmInternal'].append(Angle(radians=findMaxInFirstHalf(xs=eta0sExcidenceRadians, ys=powerExcidenceDensityEta0sInternalTETM).x))

    print('\nFinished calculating.')

    plt.title('Maximum excidence angle depending on wavelength for water.')
    plt.xlabel('wavelength [nm]')
    plt.ylabel('eta0 [°]')
    wavelengthsNm = tuple(wavlength.nanometers for wavlength in wavelengths)
    for key, value in eta0sExtrema.items():
        plt.plot(wavelengthsNm, tuple(angle.degrees for angle in value), label=key)
    plt.legend(loc='upper right')
    plt.savefig(fname='{directory}/results_overall.png'.format(
        directory=plotDirectory
    ), dpi=300)
    plt.show()

    print('Finished printing result.')

    exit(0)
