

def powerIncidentDensityProfile(height, ):
    # incident power density [p_h]
    # height - normalized to [-1, +1]
    powerDensity = 0.
    if -1 <= height <= 1:
        powerDensity = .5
    return powerDensity





if __name__ == '__main__':
    from matplotlib import pyplot
    from numpy import fromiter, linspace, diff, multiply, sum

    heights = linspace(-2., 2., 101)
    powerDensity = fromiter((powerIncidentDensityProfile(height) for height in heights),
                            dtype='float')

    averagedPowerDensity = (powerDensity[1:] + powerDensity[:-1]) / 2.
    tmp0 = diff(heights)
    tmp2 = multiply(tmp0, averagedPowerDensity)

    totalPower = sum(multiply(diff(heights), averagedPowerDensity))
    print('Total power: {power}'.format(power=totalPower))

    pyplot.plot(heights, powerDensity, '-o')
    pyplot.show()

    exit(0)



