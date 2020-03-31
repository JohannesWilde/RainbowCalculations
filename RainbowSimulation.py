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



if __name__ == '__main__':
    numberOfPoints = 201
    numberOfWavelengths = 1

    eta0sExtrema = \
        {'geometrical': list(),
         'TEinternal': list(),
         'TMinternal': list(),
         'TeTmInternal': list(),
         'TEinExternal': list(),
         'TMinExternal': list(),
         'TeTmInExternal': list(),}

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
        # eta0sExternalSupersampled = list()
        powerIncidenceDensityHeight = list()
        for height in heightsSupersampled:
            raindropCalculations = RaindropCalculations(refractiveIndexInner=refractiveIndexInner,
                                                        refractiveIndexOuter=refractiveIndexOuter,
                                                        incidenceHeight=height)
            eta0sInternalSupersampled.append(raindropCalculations.eta0Internal.radians)
            # eta0sExternalSupersampled.append(raindropCalculations.eta0External.radians)
            powerIncidenceDensityHeight.append(powerIncidentDensityProfile(height))

        heights = list()
        powerIncidenceDensityEtaInternal = list()
        powerIncidenceDensityEtaExternal = list()
        dH = heightsSupersampled[1] - heightsSupersampled[0]
        deltaH = supersampling * dH
        for index in range(numberOfPoints):
            tmpHeights = heightsSupersampled[index*supersampling:(index+1)*supersampling]
            tmpPowerIncidenceDensityHeight = powerIncidenceDensityHeight[index*supersampling:(index+1)*supersampling]

            integratedPower = dH * sum(tmpPowerIncidenceDensityHeight)

            tmpEta0sInternal = eta0sInternalSupersampled[index*supersampling:(index+1)*supersampling]
            deltaEtaInternal = max(tmpEta0sInternal) - min(tmpEta0sInternal)
            powerIncidenceDensityEtaInternal.append(integratedPower/deltaEtaInternal)

            # tmpEta0sExternal = eta0sExternalSupersampled[index*supersampling:(index+1)*supersampling]
            # deltaEtaExternal = max(tmpEta0sExternal) - min(tmpEta0sExternal)
            # powerIncidenceDensityEtaExternal.append(integratedPower/deltaEtaExternal)

            heights.append(sum(tmpHeights) / supersampling)  # use average

        # fig, (plt0, plt1) = plt.subplots(2,1)
        # plot = plt0
        # plot.plot(heightsSupersampled, eta0sInternalSupersampled)
        # plot.plot(heightsSupersampled, eta0sExternalSupersampled)
        # plot.plot(heightsSupersampled, powerIncidenceDensityHeight)
        # plot = plt1
        # plot.plot(heights, powerIncidenceDensityEtaInternal)
        # plot.plot(heights, powerIncidenceDensityEtaExternal)
        # plt.show()

        del dH, deltaH, heightsSupersampled, eta0sInternalSupersampled, powerIncidenceDensityHeight, \
            integratedPower, tmpEta0sInternal, deltaEtaInternal, \
            # eta0sExternalSupersampled, tmpEta0sExternal, deltaEtaExternal


        # powers and eta0 dependent on incidence height
        eta0s = list()
        powersTEheightsInternal= list()
        powersTMheightsInternal= list()
        for height in heights:
            raindropCalculations = RaindropCalculations(refractiveIndexInner=refractiveIndexInner,
                                                        refractiveIndexOuter=refractiveIndexOuter,
                                                        incidenceHeight=height)
            eta0s.append(raindropCalculations.eta0Internal)
            powersTEheightsInternal.append(raindropCalculations.transmittedPowerTransversalElectric)
            powersTMheightsInternal.append(raindropCalculations.transmittedPowerTransversalMagnetic)
        del raindropCalculations


        # combine height->eta0 and power-transmittance
        powerExcidenceDensityHeightsInternalTE = tuple(powerDensity * transmittancePercentage for powerDensity, transmittancePercentage in zip(powerIncidenceDensityEtaInternal, powersTEheightsInternal))
        powerExcidenceDensityHeightsInternalTM = tuple(powerDensity * transmittancePercentage for powerDensity, transmittancePercentage in zip(powerIncidenceDensityEtaInternal, powersTMheightsInternal))

        eta0sRadians, (powerExcidenceDensityEta0sInternalTE, powerExcidenceDensityEta0sInternalTM) = \
            transformSurjectiveRelation(
                oldXs=heights,
                newXsOldXs=tuple(eta0.radians for eta0 in eta0s),
                oldYsOldXsList=(powerExcidenceDensityHeightsInternalTE, powerExcidenceDensityHeightsInternalTM),
                numberOfPoints=numberOfPoints,
                newXValidityCheck=lambda x: (-1. <= x <= 1.))

        fig, (plt0, plt1) = plt.subplots(2,1)
        plot = plt0
        plot.plot(heights, powerExcidenceDensityHeightsInternalTE, label='TE-i(h)')
        plot.plot(heights, powerExcidenceDensityHeightsInternalTM, label='TM-i(h)')
        plot.set_xlabel('height')
        plot.set_ylabel('power excidence')
        plot.legend(loc='upper center')
        plot = plt1
        plot.plot(eta0sRadians, powerExcidenceDensityEta0sInternalTE, label='TE-i(eta)')
        plot.plot(eta0sRadians, powerExcidenceDensityEta0sInternalTM, label='TM-i(eta)')
        plot.set_xlabel('eta')
        plot.set_ylabel('power excidence')
        plot.legend(loc='upper center')
        plt.show()

        # # For 380nm here was a maximum of around 2 at around +/-2rad - it is assumed that this can be neglected
        # # compared to the once-internally reflected with a max of arnd 5 at +/-.7rad.
        # # Also take into account the reflections on the outside of the raindrop.
        # eta0s = list()
        # powersTEheightsExternal = list()
        # powersTMheightsExternal = list()
        # for height in heights:
        #     raindropCalculations = RaindropCalculations(refractiveIndexInner=refractiveIndexInner,
        #                                                 refractiveIndexOuter=refractiveIndexOuter,
        #                                                 incidenceHeight=height)
        #     eta0s.append(raindropCalculations.eta0External)
        #     powersTEheightsExternal.append(raindropCalculations.reflectedPowerTransversalElectric)
        #     powersTMheightsExternal.append(raindropCalculations.reflectedPowerTransversalMagnetic)
        # del raindropCalculations
        #
        # # combine height->eta0 and power-transmittance
        # powerExcidenceDensityHeightsExternalTE = tuple(powerDensity * transmittancePercentage for powerDensity, transmittancePercentage in zip(powerIncidenceDensityEtaInternal, powersTEheightsExternal))
        # powerExcidenceDensityHeightsExternalTM = tuple(powerDensity * transmittancePercentage for powerDensity, transmittancePercentage in zip(powerIncidenceDensityEtaInternal, powersTMheightsExternal))
        #
        # eta0sRadians, (powerExcidenceDensityEta0sExternalTE, powerExcidenceDensityEta0sExternalTM) = \
        #     transformSurjectiveRelation(
        #         oldXs=heights,
        #         newXsOldXs=tuple(eta0.radians for eta0 in eta0s),
        #         oldYsOldXsList=(powerExcidenceDensityHeightsExternalTE, powerExcidenceDensityHeightsExternalTM),
        #         numberOfPoints=numberOfPoints,
        #         newXValidityCheck=lambda x: (-1. <= x <= 1.))
        #
        # fig, (plt0, plt1) = plt.subplots(2,1)
        # plot = plt0
        # plot.plot(heights, powerExcidenceDensityHeightsExternalTE, label='TE-e(h)')
        # plot.plot(heights, powerExcidenceDensityHeightsExternalTM, label='TM-e(h)')
        # plot.set_xlabel('height')
        # plot.set_ylabel('power excidence')
        # plot.legend(loc='upper center')
        # plot = plt1
        # plot.plot(eta0sRadians, powerExcidenceDensityEta0sExternalTE, label='TE-e(eta)')
        # plot.plot(eta0sRadians, powerExcidenceDensityEta0sExternalTM, label='TM-e(eta)')
        # plot.set_xlabel('eta [rad]')
        # plot.set_ylabel('power excidence')
        # plot.legend(loc='upper center')
        # plt.show()


        # # superposition of internal and external once-reflected light
        # powerExcidenceDensityEta0sTE = tuple(powerTEexternal + powerTEinternal for powerTEexternal, powerTEinternal in zip(powerExcidenceDensityEta0sInternalTE, powerExcidenceDensityEta0sExternalTE))
        # powerExcidenceDensityEta0sTM = tuple(powerTMexternal + powerTMinternal for powerTMexternal, powerTMinternal in zip(powerExcidenceDensityEta0sInternalTM, powerExcidenceDensityEta0sExternalTM))
        #
        # # assume even mix of TE and TM polrization [non-polarized light]
        # powerExcidenceDensityEta0sTETMInternal = tuple((powerTEinternal + powerTMinternal) / 2. for powerTEinternal, powerTMinternal in zip(powerExcidenceDensityEta0sInternalTE, powerExcidenceDensityEta0sInternalTM))
        # powerExcidenceDensityEta0sTETMExternal = tuple((powerTEexternal + powerTMexternal) / 2. for powerTEexternal, powerTMexternal in zip(powerExcidenceDensityEta0sExternalTE, powerExcidenceDensityEta0sExternalTM))
        # powersTeTmInExternal = tuple((powerTEinExternal + powerTMinExternal) / 2. for powerTEinExternal, powerTMinExternal in zip(powerExcidenceDensityEta0sTE, powerExcidenceDensityEta0sTM))
        #
        #
        # # plot all relations
        # figure, ((axis0, axis1), (axis2, axis3), (axis4, axis5)) = plt.subplots(3,2)
        #
        # figure.suptitle('Refractive indices inner / outer = {relation}'.format(
        #     relation=refractiveIndexInner / refractiveIndexOuter
        # ))
        #
        # axis = axis0
        # eta0sDegree = tuple(eta0.degrees for eta0 in eta0s)
        # axis.plot(heights, eta0sDegree, color=ObjectColor.Lightray)
        # axis.set_xlabel('height [nu]')  # normalize unit
        # axis.set_ylabel('eta0 [degrees]')
        #
        # axis = axis2
        # axis.plot(heights, powersTEheightsInternal, color=ObjectColor.PowerTE, label='TE-i')
        # axis.plot(heights, powersTMheightsInternal, color=ObjectColor.PowerTM, label='TM-i')
        # axis.plot(heights, tuple((te + tm)/2 for te, tm in zip(powersTEheightsInternal, powersTMheightsInternal)), color=ObjectColor.PowerTETMmixed, label='(TE-i+TM-i)/2')
        # axis.set_xlabel('height [nu]')  # normalize unit
        # axis.set_ylabel('transmitted power [nu]')
        # legend1 = axis.legend(loc='upper center')
        #
        # axis = axis1
        # axis.plot(eta0sRadiansForCalculation, powersPercentageTEinternal, color=ObjectColor.PowerTE, label='TE-i')
        # axis.plot(eta0sRadiansForCalculation, powersPercentageTMinternal, color=ObjectColor.PowerTM, label='TM-i')
        # axis.plot(eta0sRadiansForCalculation, powerExcidenceDensityEta0sTETMInternal, color=ObjectColor.PowerTETMmixed, label='(TE-i+TM-i)/2')
        # axis.set_xlabel('eta0 [radians]')
        # axis.set_ylabel('transmitted power [nu]')  # normalize unit
        # legend4 = axis.legend(loc='upper right')
        #
        # axis = axis3
        # axis.plot(eta0sRadiansForCalculation, powersTEexternal, color=ObjectColor.PowerTE, label='TE-e')
        # axis.plot(eta0sRadiansForCalculation, powersTMexternal, color=ObjectColor.PowerTM, label='TM-e')
        # axis.plot(eta0sRadiansForCalculation, powerExcidenceDensityEta0sTETMExternal, color=ObjectColor.PowerTETMmixed, label='(TE-e+TM-e)/2')
        # axis.set_xlabel('eta0 [radians]')
        # axis.set_ylabel('transmitted power [nu]')  # normalize unit
        # legend5 = axis.legend(loc='upper right')
        #
        # axis = axis5
        # axis.plot(eta0sRadiansForCalculation, powerExcidenceDensityEta0sTE, color=ObjectColor.PowerTE, label='TE-ie')
        # axis.plot(eta0sRadiansForCalculation, powerExcidenceDensityEta0sTM, color=ObjectColor.PowerTM, label='TM-ie')
        # axis.plot(eta0sRadiansForCalculation, powersTeTmInExternal, color=ObjectColor.PowerTETMmixed, label='(TE-ie+TM-ie)/2')
        # axis.set_xlabel('eta0 [radians]')
        # axis.set_ylabel('transmitted power [nu]')  # normalize unit
        # legend5 = axis.legend(loc='upper right')
        #
        # # plt.savefig(fname='{directory}/results_{wavelength:.2F}.png'.format(
        # #     wavelength=wavelength.nanometers,
        # #     directory=plotDirectory
        # # ), dpi=300)
        # # plt.close(figure)
        # plt.show()
        #
        # # geometric local extremum of eta0 relative to incidence height
        # eta0sExtrema['geometrical'].append(min(eta0s))
        # eta0sExtrema['TEinternal'].append(Angle(radians=eta0sRadiansForCalculation[powersPercentageTEinternal.index(max(powersPercentageTEinternal[0:floor(len(powersPercentageTEinternal) / 2)]))]))
        # eta0sExtrema['TMinternal'].append(Angle(radians=eta0sRadiansForCalculation[powersPercentageTMinternal.index(max(powersPercentageTMinternal[0:floor(len(powersPercentageTMinternal) / 2)]))]))
        # eta0sExtrema['TeTmInternal'].append(Angle(radians=eta0sRadiansForCalculation[powerExcidenceDensityEta0sTETMInternal.index(max(powerExcidenceDensityEta0sTETMInternal[0:floor(len(powerExcidenceDensityEta0sTETMInternal) / 2)]))]))
        # eta0sExtrema['TEinExternal'].append(Angle(radians=eta0sRadiansForCalculation[powerExcidenceDensityEta0sTE.index(max(powerExcidenceDensityEta0sTE[0:floor(len(powerExcidenceDensityEta0sTE) / 2)]))]))
        # eta0sExtrema['TMinExternal'].append(Angle(radians=eta0sRadiansForCalculation[powerExcidenceDensityEta0sTM.index(max(powerExcidenceDensityEta0sTM[0:floor(len(powerExcidenceDensityEta0sTM) / 2)]))]))
        # eta0sExtrema['TeTmInExternal'].append(Angle(radians=eta0sRadiansForCalculation[powersTeTmInExternal.index(max(powersTeTmInExternal[0:floor(len(powersTeTmInExternal)/2)]))]))

    print('\nFinished calculating.')

    # plt.title('Maximum excidence angle depending on wavelength for water.')
    # plt.xlabel('wavelength [nm]')
    # plt.ylabel('eta0 [degree]')
    # wavelengthsNm = tuple(wavlength.nanometers for wavlength in wavelengths)
    # for key, value in eta0sExtrema.items():
    #     plt.plot(wavelengthsNm, tuple(angle.degrees for angle in value), label=key)
    # plt.legend(loc='upper right')
    # plt.savefig(fname='{directory}/results_overall.png'.format(
    #     directory=plotDirectory
    # ), dpi=300)
    # plt.show()

    print('Finished printing result.')

    exit(0)
