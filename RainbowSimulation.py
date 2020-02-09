# -*- coding: utf-8 -*-

'''Python script to calculate the angle a light ray is reflected
    to in a perfect sphere if it enters at an angle - assuming
    1 internal reflection only.'''

from matplotlib import pyplot as plt
from RaindropCalculations import RaindropCalculations


class ObjectZorder(object):
    # bigger values are to the front
    Raindrop = 1
    MeetingPoints = 2
    Lightray = 3

class ObjectColor(object):
    MeetingPoints = (0.,.8,0.)
    Lightray = (.8,0.,0.)


if __name__ == '__main__':
    refractiveIndexOuter = 1.
    refractiveIndexInner = 1.5

    height0 = .4  # normalized height [0,1]

    raindropCalculations = RaindropCalculations(refractiveIndexInner=refractiveIndexInner,
                                                refractiveIndexOuter=refractiveIndexOuter,
                                                incidenceHeight=height0)

    # get plot
    axis = plt.gca()
    axis.cla()

    axis.set_xlim((-1.5, 1.5))
    axis.set_ylim((-1.5, 1.5))
    axis.set_aspect('equal')

    # draw sphere
    colorValue = 2. / (1. + refractiveIndexInner / refractiveIndexOuter)
    sphereBackgroundColor = (colorValue, colorValue, colorValue)

    raindrop = plt.Circle((0, 0), 1, color=sphereBackgroundColor, fill=True, zorder=ObjectZorder.Raindrop)

    axis.add_artist(raindrop)

    # show light ray - incident
    pointBeta = raindropCalculations.pointBeta
    plt.scatter(pointBeta.x, pointBeta.y, marker='.', zorder=ObjectZorder.MeetingPoints, color=ObjectColor.MeetingPoints)
    plt.plot((2, pointBeta.x), (pointBeta.y, pointBeta.y), color=ObjectColor.Lightray)

    pointGamma = raindropCalculations.pointGamma
    plt.scatter(pointGamma.x, pointGamma.y, marker='.', zorder=ObjectZorder.MeetingPoints, color=ObjectColor.MeetingPoints)
    plt.plot((pointBeta.x, pointGamma.x), (pointBeta.y, pointGamma.y), color=ObjectColor.Lightray)

    pointDelta = raindropCalculations.pointDelta
    plt.scatter(pointDelta.x, pointDelta.y, marker='.', zorder=ObjectZorder.MeetingPoints, color=ObjectColor.MeetingPoints)
    plt.plot((pointGamma.x, pointDelta.x), (pointGamma.y, pointDelta.y), color=ObjectColor.Lightray)

    # make plot visible
    plt.show()


    exit(0)
