class Poly:

"""This class is used to create polynomial
objects with x terms."""

    def __init__(self, *coefs):

        """pass in coefficients in the order of x's degree"""

        if coefs[0] and coefs:
            for deg in range(len(coefs)):
                self.__dict__['x'+str(deg)] = coefs[::-1][deg]
            self.__dict__ = {deg: self.__dict__[deg] for deg in sorted(self.__dict__)[::-1]}
        else:
            raise ValueError('Cannot pass empty coefficient for greatest degree of x')

    def expr(self):
        """Raw format(readable) of the polynomial"""
        expr = []
        for deg, cof in self.__dict__.items():
            term = ''
            if cof and cof != 1:
                term = str(cof) + 'x' if deg[1:] == '1' else str(cof) + 'x^' + deg[1:]
            elif cof:
                term = 'x' if deg[1:] == '1' else 'x^' + deg[1:]
            if deg[1:] == '0':
                term = str(cof) if cof else ''
            term = '+' + term if expr and term and '-' not in term else term
            expr.append(term)
        return ''.join(expr)

    def __repr__(self):
        return "<Polynomial([" + "+".join(
            ['(' + str(cof) + 'x^' + deg[1:] + ')' for deg, cof in self.__dict__.items()]
        ) + ")]>"

    def __len__(self):
        """Number of terms"""
        return len(self.__dict__) - 1

    def __add__(self, other):
        x_coefs = self.__dict__.copy()
        if isinstance(other, int):
            x_coefs['x0'] = x_coefs['x0'] + other if 'x0' in x_coefs.keys() else other
        else:
            for deg, cof in other.__dict__.items():
                x_coefs[deg] = x_coefs[deg] + cof if deg in x_coefs.keys() else cof
            x_coefs = {deg: x_coefs[deg] for deg in sorted(x_coefs)[::-1]}
        return Poly(*x_coefs.values())

    def __sub__(self, other):
        x_coefs = self.__dict__.copy()
        if isinstance(other, int):
            x_coefs['x0'] = x_coefs['x0'] - other if 'x0' in x_coefs.keys() else other
        else:
            for deg, cof in other.__dict__.items():
                x_coefs[deg] = x_coefs[deg] - cof if deg in x_coefs.keys() else cof
            x_coefs = {deg: x_coefs[deg] for deg in sorted(x_coefs)[::-1]}
        return Poly(*x_coefs.values())

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __mul__(self, other):
        x_coefs = self.__dict__.copy()
        if isinstance(other, int):
            for deg in x_coefs.keys():
                x_coefs[deg] *= other
            return Poly(*x_coefs.values())
        new_coefs = dict()
        for deg1, cof1 in other.__dict__.items():
            for deg2, cof2 in x_coefs.items():
                deg = 'x' + str(int(deg1[1:]) + int(deg2[1:]))
                new_coefs[deg] = new_coefs[deg] + (cof1 * cof2) if deg in new_coefs.keys() else cof1 * cof2
        new_coefs = {deg: new_coefs[deg] for deg in sorted(new_coefs)[::-1]}
        return Poly(*new_coefs.values())

    def __pow__(self, index):
        if index >= 0:
            if not index:
                return 1
            value = self
            for _ in range(1, index):
                value = value * self
        else:
            raise ValueError('negative index is not allowed')
        return Poly(*value.__dict__.values())

    def __truediv__(self, other):
        x_coefs = self.__dict__.copy()
        if isinstance(other, int):
            for deg in x_coefs.keys():
                x_coefs[deg] /= other
            return Poly(*x_coefs.values())
        if len(self) < len(other):
            raise ArithmeticError("Can't divide lower degree polynomial with higher degree polynomial")
        new_coefs = dict()
        for deg1, cof1 in other.__dict__.items():
            for deg2, cof2 in x_coefs.items():
                deg = 'x' + str(int(deg2[1:]) - int(deg1[1:]))
                new_coefs[deg] = new_coefs[deg] + (cof1 / cof2) if deg in new_coefs.keys() else cof1 / cof2
        new_coefs = {deg: new_coefs[deg] for deg in sorted(new_coefs)[::-1]}
        return Poly(*new_coefs.values())

    def __floordiv__(self, other):
        x_coefs = self.__dict__.copy()
        if isinstance(other, int):
            new_coefs = dict()
            for deg in x_coefs.keys():
                val = x_coefs[deg] // other
                if val or new_coefs:
                    new_coefs[deg] = val
            return Poly(*new_coefs.values()) if new_coefs else 0
        if len(self) < len(other) and type(self) == type(other):
            raise ArithmeticError("Can't divide lower degree polynomial with higher degree polynomial")
        print("coming soon...")

    def __mod__(self, other):
        x_coefs = self.__dict__.copy()
        if isinstance(other, int):
            new_coefs = dict()
            for deg in x_coefs.keys():
                val = x_coefs[deg] % other
                if val or new_coefs:
                    new_coefs[deg] = val
            return Poly(*new_coefs.values()) if new_coefs else 0
        else:
            print("coming soon...")

    def __getitem__(self, pos):
        if pos in self.__dict__.keys() or pos in range(len(self.__dict__.keys())):
            if isinstance(pos, str):
                return self.__dict__[pos]
            else:
                return self.__dict__['x' + str(pos)]
        else:
            raise KeyError("coefficient for the given degree of x doesn't exist")

    def __call__(self, x):
        return sum([(x ** deg) * self[cof] for deg, cof in enumerate(sorted(self.__dict__))])

