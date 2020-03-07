
from math import asin, cos, sin, sqrt
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

    def _getTotalInternalReflexionThresholdAngle(self):
        if self.mediumFrom.refractiveIndex > self.mediumTo.refractiveIndex:
            threshold = asin(self.mediumTo.refractiveIndex / self.mediumFrom.refractiveIndex)
        else:
            threshold = float('inf')
        return Angle(radians=threshold)


    def amplitudeToPowerTransmittance(self, incidenceAngle, transmittance):
        if incidenceAngle > self._getTotalInternalReflexionThresholdAngle():
            powerRatio = 0.
        else:
            n0 = self.mediumFrom.refractiveIndex
            n1 = self.mediumTo.refractiveIndex
            alpha = incidenceAngle.radians
            powerRatio = (sqrt(n1 ** 2 - (n0 * sin(alpha)) ** 2) / (n0 * cos(alpha))) * (abs(transmittance) ** 2)
        return powerRatio

    def amplitudeToPowerReflectance(self, reflectance):
        return abs(reflectance) ** 2

    def transmittanceTransversalElectricAmplitude(self, incidenceAngle):
        assert(isinstance(incidenceAngle, Angle))
        if incidenceAngle > self._getTotalInternalReflexionThresholdAngle():
            transmittance = 0.
        else:
            # refractive indices
            n0 = self.mediumFrom.refractiveIndex
            n1 = self.mediumTo.refractiveIndex

            # relative magnetic permeability
            ur0 = self.mediumFrom.magneticPermeability
            ur1 = self.mediumTo.magneticPermeability

            # relative electric permittivity
            er0 = n0 ** 2
            er1 = n1 ** 2

            alpha = incidenceAngle.radians

            transmittance = (2. * n0 * cos(alpha) / (n0 * cos(alpha) + (ur0 / ur1 * sqrt(er1 - er0 * (sin(alpha) ** 2)))))
        return transmittance

    def transmittanceTransversalElectric(self, incidenceAngle):
        return self.amplitudeToPowerTransmittance(incidenceAngle=incidenceAngle,
                                                  transmittance=self.transmittanceTransversalElectricAmplitude(incidenceAngle=incidenceAngle))

    def reflectanceTransversalElectricAmplitude(self, incidenceAngle):
        assert(isinstance(incidenceAngle, Angle))
        if incidenceAngle > self._getTotalInternalReflexionThresholdAngle():
            reflectance = 1.
        else:
            # refractive indices
            n0 = float(self.mediumFrom.refractiveIndex)
            n1 = float(self.mediumTo.refractiveIndex)

            # relative magnetic permeability
            ur0 = float(self.mediumFrom.magneticPermeability)
            ur1 = float(self.mediumTo.magneticPermeability)

            # relative electric permittivity
            er0 = n0 ** 2
            er1 = n1 ** 2

            alpha = incidenceAngle.radians

            a = n0 * cos(alpha)
            b = ur0 / ur1 * sqrt(er1 - er0 * (sin(alpha) ** 2))

            reflectance = (a - b) / (a + b)

        return reflectance

    def reflectanceTransversalElectric(self, incidenceAngle):
        return self.amplitudeToPowerReflectance(reflectance=self.reflectanceTransversalElectricAmplitude(incidenceAngle=incidenceAngle))

    def transmittanceTransversalMagneticAmplitude(self, incidenceAngle):
        assert(isinstance(incidenceAngle, Angle))
        if incidenceAngle > self._getTotalInternalReflexionThresholdAngle():
            transmittance = 0.
        else:
            # refractive indices
            n0 = float(self.mediumFrom.refractiveIndex)
            n1 = float(self.mediumTo.refractiveIndex)

            # relative electric permittivity
            er0 = n0 ** 2
            er1 = n1 ** 2

            # relative magnetic permeability
            ur0 = float(self.mediumFrom.magneticPermeability)
            ur1 = float(self.mediumTo.magneticPermeability)

            alpha = incidenceAngle.radians#

            transmittance = (2. * n0 * n1 * cos(alpha)/ (er1 * ur0 / ur1 * cos(alpha) + n0 * sqrt(er1 - er0 * (sin(alpha) ** 2))))

        return transmittance

    def transmittanceTransversalMagnetic(self, incidenceAngle):
        return self.amplitudeToPowerTransmittance(incidenceAngle=incidenceAngle,
                                                  transmittance=self.transmittanceTransversalMagneticAmplitude(incidenceAngle=incidenceAngle))

    def reflectanceTransversalMagneticAmplitude(self, incidenceAngle):
        assert(isinstance(incidenceAngle, Angle))
        if incidenceAngle > self._getTotalInternalReflexionThresholdAngle():
            reflectance = 1.
        else:
            # refractive indices
            n0 = float(self.mediumFrom.refractiveIndex)
            n1 = float(self.mediumTo.refractiveIndex)

            # relative electric permittivity
            er0 = n0 ** 2
            er1 = n1 ** 2

            # relative magnetic permeability
            ur0 = float(self.mediumFrom.magneticPermeability)
            ur1 = float(self.mediumTo.magneticPermeability)

            alpha = incidenceAngle.radians

            a = er1 * ur0 / ur1 * cos(alpha)
            b = n0 * sqrt(er1 - er0 * (sin(alpha) ** 2))

            reflectance = (a - b) / (a + b)

        return reflectance

    def reflectanceTransversalMagnetic(self, incidenceAngle):
        return self.amplitudeToPowerReflectance(reflectance=self.reflectanceTransversalMagneticAmplitude(incidenceAngle=incidenceAngle))



if __name__ == '__main__':
    from matplotlib import pyplot as plt
    from numpy import linspace
    angles = tuple(Angle(degrees=value) for value in linspace(start=0., stop=90, num=150))
    fresnel = FresnelCoefficients(mediumFrom=Medium(refractiveIndex=1.5, magneticPermeability=1), mediumTo=Medium(refractiveIndex=1., magneticPermeability=1))
    # amplitude
    TEtransmittanceAmplitude = tuple(fresnel.transmittanceTransversalElectricAmplitude(incidenceAngle=angle) for angle in angles)
    TEreflectanceAmplitude = tuple(fresnel.reflectanceTransversalElectricAmplitude(incidenceAngle=angle) for angle in angles)
    TMtransmittanceAmplitude = tuple(fresnel.transmittanceTransversalMagneticAmplitude(incidenceAngle=angle) for angle in angles)
    TMreflectanceAmplitude = tuple(fresnel.reflectanceTransversalMagneticAmplitude(incidenceAngle=angle) for angle in angles)
    # power
    TEtransmittance = tuple(fresnel.transmittanceTransversalElectric(incidenceAngle=angle) for angle in angles)
    TEreflectance = tuple(fresnel.reflectanceTransversalElectric(incidenceAngle=angle) for angle in angles)
    TMtransmittance = tuple(fresnel.transmittanceTransversalMagnetic(incidenceAngle=angle) for angle in angles)
    TMreflectance = tuple(fresnel.reflectanceTransversalMagnetic(incidenceAngle=angle) for angle in angles)
    # plotting
    anglesDegrees = tuple(angle.degrees for angle in angles)
    subplot0 = plt.subplot(1,2,1)
    subplot0.plot(anglesDegrees, TEtransmittance)
    subplot0.plot(anglesDegrees, TEreflectance)
    subplot0.plot(anglesDegrees, TMtransmittance)
    subplot0.plot(anglesDegrees, TMreflectance)
    subplot1 = plt.subplot(1,2,2)
    subplot1.plot(anglesDegrees, TEtransmittanceAmplitude)
    subplot1.plot(anglesDegrees, TEreflectanceAmplitude)
    subplot1.plot(anglesDegrees, TMtransmittanceAmplitude)
    subplot1.plot(anglesDegrees, TMreflectanceAmplitude)
    plt.show()
    exit(0)
