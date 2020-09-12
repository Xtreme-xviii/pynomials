from .polynomial import Poly


def d(fx):
    """ Used to differentiate Poly object polynomials """
    if not isinstance(fx, (int, float, Poly)):
        return TypeError("Only Poly objects acn be differentiated")
    if not isinstance(fx, Poly):
        return 0
    dfx = [fx[deg+1]*(deg+1) for deg in range(len(fx))]
    return Poly(*dfx[::-1]) if dfx else 0


def dd(fx, n):
    """ Used to differentiate Poly object polynomials n times ( n -> |R )"""
    for _ in range(n):
        fx = d(fx)
    return fx
