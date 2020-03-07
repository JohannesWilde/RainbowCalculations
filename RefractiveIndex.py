# -*- coding: utf-8 -*-

from math import sqrt
from Range import Range
from Length import Length

class RefractiveIndex(object):

    def __init__(self):
        return

    def permittivity(self, wavelength):
        raise NotImplemented('Child-classes shall override this.')

    def refractiveIndex(self, wavelength):
        temp2 = self.permittivity(wavelength=wavelength)
        temp = sqrt(temp2)
        return temp


class RefractiveIndexSellmeier(RefractiveIndex):

    def __init__(self, wavelengthRange, sellmeierCoefficientPairs):
        # Sellmeier coefficient pair in (1, micrometers^2)
        RefractiveIndex.__init__(self)
        self.wavelengthRange = wavelengthRange
        self.sellmeierCoefficientPairs = sellmeierCoefficientPairs
        return

    def permittivity(self, wavelength):
        if not self.wavelengthRange.checkValueInRange(value=wavelength):
            raise ValueError('Wavlength [{wavelength}] out of range [{range}].'.format(wavelength=wavelength,
                                                                                       range=self.wavelengthRange))
        wavelengthSquaredMicrometers = wavelength.micrometers ** 2
        permittivity = 1
        for sellmeierCoefficientPair in self.sellmeierCoefficientPairs:
            permittivity += sellmeierCoefficientPair[0] / (1 - (sellmeierCoefficientPair[1] / wavelengthSquaredMicrometers))
        return permittivity


class RefractiveIndex2007DaimonMasumura20CWater(RefractiveIndexSellmeier):
    '''https://refractiveindex.info/?shelf=main&book=H2O&page=Daimon-20.0C'''
    def __init__(self):
        wavelengthRange = Range(min=Length(nanometers=180), max=Length(nanometers=1130))
        sellmeierCoefficientPairs = ((5.684027565e-1, 5.101829712e-3),
                                          (1.726177391e-1, 1.821153936e-2),
                                          (2.086189578e-2, 2.620722293e-2),
                                          (1.130748688e-1, 1.069792721e1))
        RefractiveIndexSellmeier.__init__(self,
                                          wavelengthRange=wavelengthRange,
                                          sellmeierCoefficientPairs=sellmeierCoefficientPairs)
        return




if __name__ == '__main__':
    from Length import Length
    from matplotlib import pyplot as plt
    wavelengths = tuple(Length(nanometers=value) for value in range(180, 1130, 5))
    refractiveIndexWater = tuple(RefractiveIndex2007DaimonMasumura20CWater().refractiveIndex(wavelength=wavelength) for wavelength in wavelengths)
    wavelengthsNanometer = tuple(wavelength.nanometers for wavelength in wavelengths)
    plt.plot(wavelengthsNanometer, refractiveIndexWater)
    plt.show()
    exit(0)
