from .polynomial import Poly
from .differentiation import dd, d


class Quad(Poly):

    def __init__(self, a, b, c):
        if not a:
            ValueError("All 3 coefficients must be non-null values, coefficient of x^2 cannot be zero.")
        super().__init__(a, b, c)

    def delta(self):
        return (self[1]**2)-(4*self[2]*self[0])  # b^2-4ac

    def roots(self):
        if self.delta() < 0:
            return []
        operator = lambda fun: (float(-self[1]).__getattribute__(f'__{fun}__')(self.delta()**0.5))/(2*self[2])
        return [operator('add')] if not self.delta() else [operator('add'), operator('sub')]

    def curve(self):
        return dd(self, 2)[0]  # if positive Minima, if negative Maxima

    def turns_at(self):
        ff = d(self)
        return -(ff[0]/ff[1])

