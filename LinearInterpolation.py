# -*- coding: utf-8 -*-

from Range import Range

class LinearInterpolator(object):

    def __init__(self, point0, point1):
        if point0.x == point1.x:
            raise ValueError('Can\'t linearly interpolate between points from the same x-value [{point0}, {point1}]'.format(point0=point0, point1=point1))
        self._point0 = point0
        self._point1 = point1
        self._acclivity = (point1.y - point0.y) / (point1.x - point0.x)
        self._offset = (point1.x * point0.y - point0.x * point1.y) / (point1.x - point0.x)
        return

    @property
    def acclivity(self):
        return self._acclivity

    @property
    def offset(self):
        return self._offset

    def at(self, x):
        return self.acclivity * x + self.offset

    def where(self, y):
        if self.acclivity == 0:
            raise ValueError('Can\'t determine a unique x for a constant function [{function}]'.format(function=self))
        return ((y - self.offset) / self.acclivity)

    @staticmethod
    def valueInUnorderedRange(value, maxOrMin, minOrMax):
        if maxOrMin > minOrMax:
            range = Range(min=minOrMax, max=maxOrMin)
        else:
            range = Range(min=maxOrMin, max=minOrMax)
        return range.checkValueInRange(value=value)

    def xInRange(self, x):
        return self.valueInUnorderedRange(value=x, maxOrMin=self._point0.x, minOrMax=self._point1.x)

    def yInRange(self, y):
        return self.valueInUnorderedRange(value=y, maxOrMin=self._point0.y, minOrMax=self._point1.y)

    def __str__(self):
        return 'y = {acclivity} * x + {offset}'.format(acclivity=self.acclivity, offset=self.offset)

    def __repr__(self):
        return '{value} - LinearInterpolator at {address}'.format(value=str(self), address = hex(id(self)))


class StepwiseLinearFunctionInterpolator(object):

    def __init__(self, listOfPoints):
        self.checkAtLeastTwoPoints(listOfPoints=listOfPoints)
        self.checkMonotonity(listOfPoints=listOfPoints)
        self._listOfPoints = listOfPoints
        self._listOfInterpolators = self._createListOfInterpolators(listOfPoints=listOfPoints)
        return

    @staticmethod
    def checkAtLeastTwoPoints(listOfPoints):
        if len(listOfPoints) < 2:
            ValueError('At least 2 points required for interpolation, however only {count} provided.'.format(count=len(listOfPoints)))
        return

    @staticmethod
    def checkMonotonity(listOfPoints):
        previousPoint = None
        currentPoint = None
        for point in listOfPoints:
            previousPoint = currentPoint
            currentPoint = point
            if previousPoint is not None:
                if currentPoint.x <= previousPoint.x:
                    raise ValueError('x-values are not strictly monotonously increasing [{point0}, {point1}].'.format(point0=previousPoint, point1=currentPoint))
        return

    @staticmethod
    def _createListOfInterpolators(listOfPoints):
        listOfInterpolators = list()
        previousPoint = None
        currentPoint = None
        for point in listOfPoints:
            previousPoint = currentPoint
            currentPoint = point
            if previousPoint is not None:
                listOfInterpolators.append(LinearInterpolator(point0=previousPoint, point1=currentPoint))
        return listOfInterpolators

    def xInRange(self, x):
        return Range(min=self._listOfPoints[0].x, max=self._listOfPoints[-1].x).checkValueInRange(value=x)

    def yInRange(self, y):
        yMin = min((point.y for point in self._listOfPoints))
        yMax = max((point.y for point in self._listOfPoints))
        return Range(min=yMin, max=yMax).checkValueInRange(value=y)

    def at(self, x):
        # assume uniqueness in x [for every x-value exactly one y-value]
        y = None
        for linearInterpolator in self._listOfInterpolators:
            if linearInterpolator.xInRange(x=x):
                y = linearInterpolator.at(x=x)
                break
        return y

    def where(self, y, index=0):
        # non-uniqueness in y [one y-value for potentially more than one x-value]
        xValues = list()
        x = None
        for linearInterpolator in self._listOfInterpolators:
            if linearInterpolator.yInRange(y=y):
                tempX = linearInterpolator.where(y=y)
                if (len(xValues) == 0) or ((len(xValues) > 0) and (xValues[-1] != tempX)):
                    xValues.append(tempX)
                if len(xValues) == (index + 1):
                    x = xValues[index]
                    break
        return x



if __name__ == '__main__':
    from Point import Point2D
    listOfPoints = (Point2D(0, 0), Point2D(1, 1), Point2D(2, 0))
    bla = StepwiseLinearFunctionInterpolator(listOfPoints)
    print(bla.at(-.5))
    print(bla.at(0.))
    print(bla.at(.5))
    print(bla.at(1.))
    print(bla.at(1.5))
    print(bla.at(2.))
    print(bla.at(2.5))

    print('    ----    ')

    print(bla.where(-.5))
    print(bla.where(0.))
    print(bla.where(.5))
    print(bla.where(1.))

    print(bla.where(1.5))

    print(bla.where(1., 1))
    print(bla.where(.5, 1))
    print(bla.where(0., 1))
    print(bla.where(-.5, 1))

    exit(0)
