
from math import cos, sin, sqrt
from Angle import Angle

class Medium(object):

    def __init__(self, refractiveIndex, magneticPermeability):
        self.refractiveIndex = refractiveIndex
        self.magneticPermeability = magneticPermeability
        return


class FresnelCoefficients(object):

    def __init__(self, mediumFrom, mediumTo):
        self.mediumFrom = mediumFrom
        self.mediumTo = mediumTo
        return

    def amplitudeToPowerTransmittance(self, incidenceAngle, transmittance):
        n0 = self.mediumFrom.refractiveIndex
        n1 = self.mediumTo.refractiveIndex
        alpha = incidenceAngle.radians
        powerRatio = (sqrt(n1 ** 2 - (n0 * sin(alpha)) ** 2) / (n0 * cos(alpha))) * (abs(transmittance) ** 2)
        return powerRatio

    def amplitudeToPowerReflectance(self, reflectance):
        return abs(reflectance) ** 2

    def transmittanceTransversalElectricAmplitude(self, incidenceAngel):
        assert(isinstance(incidenceAngel, Angle))
        # refractive indices
        n0 = self.mediumFrom.refractiveIndex
        n1 = self.mediumTo.refractiveIndex

        # relative magnetic permeability
        ur0 = self.mediumFrom.magneticPermeability
        ur1 = self.mediumTo.magneticPermeability

        # relative electric permittivity
        er0 = n0 ** 2
        er1 = n1 ** 2

        alpha = incidenceAngel.radians

        transmittance = (2. * n0 * cos(alpha) / (n0 * cos(alpha) + (ur0 / ur1 * sqrt(er1 - er0 * (sin(alpha) ** 2)))))
        return transmittance

    def transmittanceTransversalElectric(self, incidenceAngel):
        return self.amplitudeToPowerTransmittance(incidenceAngle=incidenceAngel,
                                                  transmittance=self.transmittanceTransversalElectricAmplitude(incidenceAngel=incidenceAngel))

    def reflectanceTransversalElectricAmplitude(self, incidenceAngel):
        assert(isinstance(incidenceAngel, Angle))
        # refractive indices
        n0 = float(self.mediumFrom.refractiveIndex)
        n1 = float(self.mediumTo.refractiveIndex)

        # relative magnetic permeability
        ur0 = float(self.mediumFrom.magneticPermeability)
        ur1 = float(self.mediumTo.magneticPermeability)

        # relative electric permittivity
        er0 = n0 ** 2
        er1 = n1 ** 2

        NAsquared = er0 * (sin(incidenceAngel.radians) ** 2)

        alpha = incidenceAngel.radians

        a = n0 * cos(alpha)
        b = ur0 / ur1 * sqrt(er1 - er0 * (sin(alpha) ** 2))

        reflectance = (a - b) / (a + b)

        return reflectance

    def reflectanceTransversalElectric(self, incidenceAngel):
        return self.amplitudeToPowerReflectance(reflectance=self.reflectanceTransversalElectricAmplitude(incidenceAngel=incidenceAngel))

    def transmittanceTransversalMagneticAmplitude(self, incidenceAngel):
        assert(isinstance(incidenceAngel, Angle))
        # refractive indices
        n0 = float(self.mediumFrom.refractiveIndex)
        n1 = float(self.mediumTo.refractiveIndex)

        # relative electric permittivity
        er0 = n0 ** 2
        er1 = n1 ** 2

        # relative magnetic permeability
        ur0 = float(self.mediumFrom.magneticPermeability)
        ur1 = float(self.mediumTo.magneticPermeability)

        alpha = incidenceAngel.radians#

        transmittance = (2. * n0 * n1 * cos(alpha)/ (er1 * ur0 / ur1 * cos(alpha) + n0 * sqrt(er1 - er0 * (sin(alpha) ** 2))))

        return transmittance

    def transmittanceTransversalMagnetic(self, incidenceAngel):
        return self.amplitudeToPowerTransmittance(incidenceAngle=incidenceAngel,
                                                  transmittance=self.transmittanceTransversalMagneticAmplitude(incidenceAngel=incidenceAngel))

    def reflectanceTransversalMagneticAmplitude(self, incidenceAngel):
        assert(isinstance(incidenceAngel, Angle))
        # refractive indices
        n0 = float(self.mediumFrom.refractiveIndex)
        n1 = float(self.mediumTo.refractiveIndex)

        # relative electric permittivity
        er0 = n0 ** 2
        er1 = n1 ** 2

        # relative magnetic permeability
        ur0 = float(self.mediumFrom.magneticPermeability)
        ur1 = float(self.mediumTo.magneticPermeability)

        alpha = incidenceAngel.radians

        a = er1 * ur0 / ur1 * cos(alpha)
        b = n0 * sqrt(er1 - er0 * (sin(alpha) ** 2))

        reflectance = (a - b) / (a + b)

        return reflectance

    def reflectanceTransversalMagnetic(self, incidenceAngel):
        return self.amplitudeToPowerReflectance(reflectance=self.reflectanceTransversalMagneticAmplitude(incidenceAngel=incidenceAngel))



if __name__ == '__main__':
    from Angle import Angle
    from matplotlib import pyplot as plt
    from numpy import linspace
    from math import asin, pi
    angles = tuple(Angle(degrees=value) for value in linspace(start=0., stop=asin(1/1.5)/pi * 180, num=150))
    fresnel = FresnelCoefficients(mediumFrom=Medium(refractiveIndex=1.5, magneticPermeability=1), mediumTo=Medium(refractiveIndex=1, magneticPermeability=1))
    TEtransmittance = tuple(fresnel.transmittanceTransversalElectric(incidenceAngel=angle) for angle in angles)
    TEreflectance = tuple(fresnel.reflectanceTransversalElectric(incidenceAngel=angle) for angle in angles)
    TMtransmittance = tuple(fresnel.transmittanceTransversalMagnetic(incidenceAngel=angle) for angle in angles)
    TMreflectance = tuple(fresnel.reflectanceTransversalMagnetic(incidenceAngel=angle) for angle in angles)
    anglesDegrees = tuple(angle.degrees for angle in angles)
    plt.plot(anglesDegrees, TEtransmittance)
    plt.plot(anglesDegrees, TEreflectance)
    plt.plot(anglesDegrees, TMtransmittance)
    plt.plot(anglesDegrees, TMreflectance)
    plt.show()
    exit(0)
    