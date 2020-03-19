# -*- coding: utf-8 -*-

'''Python script to calculate the angle a light ray is reflected
    to in a perfect sphere if it enters at an angle - assuming
    1 internal reflection only.'''

from matplotlib import pyplot as plt
from math import floor
from os import mkdir
from Angle import Angle
from FresnelCoefficients import FresnelCoefficients, Medium
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


if __name__ == '__main__':
    numberOfPoints = 201
    numberOfWavelengths = 5

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

    plotDirectory = 'calculations2'
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

        # powers and eta0 dependent on incidence hieght
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
        del raindropCalculations

        # use linear interpolator to reverse this relation height -> eta0 [is not bijective!]
        heightsAuEta0sRadiansPoints = []
        for heightAu, eta0 in zip(heights, eta0s):
            heightsAuEta0sRadiansPoints.append(Point(x=heightAu, y=eta0.radians))
        linearInterpolatorHeightsAuEta0sRadians = StepwiseLinearFunctionInterpolator(listOfPoints=heightsAuEta0sRadiansPoints)

        # determine output angles as new dependent parameter
        eta0Min = min(eta0s)
        eta0Max = max(eta0s)
        eta0sRadiansForCalculation = linspace(eta0Min.radians, eta0Max.radians, numberOfPoints)

        powersTEinternal = list()
        powersTMinternal = list()
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
            powerTEinternal = 0.
            powerTMinternal = 0.
            for correspondingHeight in correspondingHeights:
                raindropCalculations = RaindropCalculations(refractiveIndexInner=refractiveIndexInner,
                                                            refractiveIndexOuter=refractiveIndexOuter,
                                                            incidenceHeight=correspondingHeight)
                powerTEinternal += raindropCalculations.transmittedPowerTransversalElectric
                powerTMinternal += raindropCalculations.transmittedPowerTransversalMagnetic
                del raindropCalculations

            powersTEinternal.append(powerTEinternal)
            powersTMinternal.append(powerTMinternal)
            del powerTEinternal, powerTMinternal


        # also take into account the reflections on the outside of the raindrop
        powersTEexternal = list()
        powersTMexternal = list()
        for eta0Radians in eta0sRadiansForCalculation:
            fresnelIn = RaindropCalculations(refractiveIndexInner=refractiveIndexInner,
                                             refractiveIndexOuter=refractiveIndexOuter,
                                             incidenceHeight=0.).fresnelIn
            powerTEexternal = fresnelIn.reflectanceTransversalElectric(incidenceAngle=Angle(radians=eta0Radians/2.))
            powerTMexternal = fresnelIn.reflectanceTransversalMagnetic(incidenceAngle=Angle(radians=eta0Radians/2.))

            powersTEexternal.append(powerTEexternal)
            powersTMexternal.append(powerTMexternal)
            del fresnelIn


        # superposition of internal and external once-reflected light
        powersTEinExternal = tuple(powerTEexternal + powerTEinternal for powerTEexternal, powerTEinternal in zip(powersTEexternal, powersTEinternal))
        powersTMinExternal = tuple(powerTMexternal + powerTMinternal for powerTMexternal, powerTMinternal in zip(powersTMexternal, powersTMinternal))

        # assume even mix of TE and TM polrization [non-polarized light]
        powersTeTmInternal = tuple((powerTEinternal + powerTMinternal) / 2. for powerTEinternal, powerTMinternal in zip(powersTEinternal, powersTMinternal))
        powersTeTmExternal = tuple((powerTEexternal + powerTMexternal) / 2. for powerTEexternal, powerTMexternal in zip(powersTEexternal, powersTMexternal))
        powersTeTmInExternal = tuple((powerTEinExternal + powerTMinExternal) / 2. for powerTEinExternal, powerTMinExternal in zip(powersTEinExternal, powersTMinExternal))


        # plot all relations
        figure, ((axis0, axis1), (axis2, axis3), (axis4, axis5)) = plt.subplots(3,2)

        figure.suptitle('Refractive indices inner / outer = {relation}'.format(
            relation=refractiveIndexInner / refractiveIndexOuter
        ))

        axis = axis0
        eta0sDegree = tuple(eta0.degrees for eta0 in eta0s)
        axis.plot(heights, eta0sDegree, color=ObjectColor.Lightray)
        axis.set_xlabel('height [nu]')  # normalize unit
        axis.set_ylabel('eta0 [degrees]')

        axis = axis2
        axis.plot(heights, powersTEheights, color=ObjectColor.PowerTE, label='TE-i')
        axis.plot(heights, powersTMheights, color=ObjectColor.PowerTM, label='TM-i')
        axis.plot(heights, tuple((te + tm)/2 for te, tm in zip(powersTEheights, powersTMheights)), color=ObjectColor.PowerTETMmixed, label='(TE-i+TM-i)/2')
        axis.set_xlabel('height [nu]')  # normalize unit
        axis.set_ylabel('transmitted power [nu]')
        legend1 = axis.legend(loc='upper center')

        axis = axis1
        axis.plot(eta0sRadiansForCalculation, powersTEinternal, color=ObjectColor.PowerTE, label='TE-i')
        axis.plot(eta0sRadiansForCalculation, powersTMinternal, color=ObjectColor.PowerTM, label='TM-i')
        axis.plot(eta0sRadiansForCalculation, powersTeTmInternal, color=ObjectColor.PowerTETMmixed, label='(TE-i+TM-i)/2')
        axis.set_xlabel('eta0 [radians]')
        axis.set_ylabel('transmitted power [nu]')  # normalize unit
        legend4 = axis.legend(loc='upper right')

        axis = axis3
        axis.plot(eta0sRadiansForCalculation, powersTEexternal, color=ObjectColor.PowerTE, label='TE-e')
        axis.plot(eta0sRadiansForCalculation, powersTMexternal, color=ObjectColor.PowerTM, label='TM-e')
        axis.plot(eta0sRadiansForCalculation, powersTeTmExternal, color=ObjectColor.PowerTETMmixed, label='(TE-e+TM-e)/2')
        axis.set_xlabel('eta0 [radians]')
        axis.set_ylabel('transmitted power [nu]')  # normalize unit
        legend5 = axis.legend(loc='upper right')

        axis = axis5
        axis.plot(eta0sRadiansForCalculation, powersTEinExternal, color=ObjectColor.PowerTE, label='TE-ie')
        axis.plot(eta0sRadiansForCalculation, powersTMinExternal, color=ObjectColor.PowerTM, label='TM-ie')
        axis.plot(eta0sRadiansForCalculation, powersTeTmInExternal, color=ObjectColor.PowerTETMmixed, label='(TE-ie+TM-ie)/2')
        axis.set_xlabel('eta0 [radians]')
        axis.set_ylabel('transmitted power [nu]')  # normalize unit
        legend5 = axis.legend(loc='upper right')

        plt.savefig(fname='{directory}/results_{wavelength:.2F}.png'.format(
            wavelength=wavelength.nanometers,
            directory=plotDirectory
        ), dpi=300)
        plt.close(figure)
        # plt.show()

        # geometric local extremum of eta0 relative to incidence height
        eta0sExtrema['geometrical'].append(min(eta0s))
        eta0sExtrema['TEinternal'].append(Angle(radians=eta0sRadiansForCalculation[powersTEinternal.index(max(powersTEinternal[0:floor(len(powersTEinternal)/2)]))]))
        eta0sExtrema['TMinternal'].append(Angle(radians=eta0sRadiansForCalculation[powersTMinternal.index(max(powersTMinternal[0:floor(len(powersTMinternal)/2)]))]))
        eta0sExtrema['TeTmInternal'].append(Angle(radians=eta0sRadiansForCalculation[powersTeTmInternal.index(max(powersTeTmInternal[0:floor(len(powersTeTmInternal)/2)]))]))
        eta0sExtrema['TEinExternal'].append(Angle(radians=eta0sRadiansForCalculation[powersTEinExternal.index(max(powersTEinExternal[0:floor(len(powersTEinExternal)/2)]))]))
        eta0sExtrema['TMinExternal'].append(Angle(radians=eta0sRadiansForCalculation[powersTMinExternal.index(max(powersTMinExternal[0:floor(len(powersTMinExternal)/2)]))]))
        eta0sExtrema['TeTmInExternal'].append(Angle(radians=eta0sRadiansForCalculation[powersTeTmInExternal.index(max(powersTeTmInExternal[0:floor(len(powersTeTmInExternal)/2)]))]))

    print('\nFinished calculating.')

    plt.title('Maximum excidence angle depending on wavelength for water.')
    plt.xlabel('wavelength [nm]')
    plt.ylabel('eta0 [degree]')
    wavelengthsNm = tuple(wavlength.nanometers for wavlength in wavelengths)
    for key, value in eta0sExtrema.items():
        plt.plot(wavelengthsNm, tuple(angle.degrees for angle in value), label=key)
    plt.legend(loc='upper right')
    plt.savefig(fname='{directory}/results_overall.png'.format(
        directory=plotDirectory
    ), dpi=300)
    # plt.show()

    print('Finished printing result.')

    exit(0)
