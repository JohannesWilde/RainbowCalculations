# -*- coding: utf-8 -*-

'''Python script to calculate the angle a light ray is reflected
    to in a perfect sphere if it enters at an angle - assuming
    1 internal reflection only.'''

from matplotlib import pyplot as plt
from math import sin, cos, tan, asin, atan


if __name__ == '__main__':
    refractiveIndexOuter = 1.
    refractiveIndexInner = 1.5

    # get plot
    axis = plt.gca()
    axis.cla()

    axis.set_xlim((-1.5, 1.5))
    axis.set_ylim((-1.5, 1.5))
    axis.set_aspect('equal')

    # draw sphere
    colorValue = 5. / (1. + refractiveIndexInner / refractiveIndexOuter)
    sphereBackgroundColor = (colorValue, colorValue, colorValue)

    raindrop = plt.Circle((0, 0), 1, color=sphereBackgroundColor, fill=True)

    axis.add_artist(raindrop)

    # show light ray



    # make plot visible
    plt.show()

    exit(0)
