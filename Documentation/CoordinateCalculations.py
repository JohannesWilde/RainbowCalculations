
from math import asin, pi

def average(x1, x2):
    return (x1 + x2) / 2.

if __name__ == '__main__':
    n = 1.3347
    xmin = .75

    method = lambda x: 2 * (2*asin(x/n) - asin(x)) / pi * 180.
    ymin = method(xmin)

    for x2 in ((.765, .78,), (.855, .87,),):
        for x in x2:
            print('\\draw (axis cs: {x}, {ymin}) -- (axis cs: {x},{y}) -- (axis cs: {xmin},{y});'.format(x=x, y=method(x), xmin=xmin, ymin=ymin))
        print('\\draw (axis cs: {x}, {y}) node {{$\\Delta h_{{}}$}};'.format(x=average(x2[0], x2[1]), y=ymin))
        print('\\draw (axis cs: {x}, {y}) node {{$\\Delta \\gamma_{{}}$}};'.format(x=xmin, y=average(method(x2[0]), method(x2[1]))))

    exit(0)