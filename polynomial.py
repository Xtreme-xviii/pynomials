class Poly:

    """
    This class creates polynomial objects with x terms.
    Create a polynomial expression/object by passing in coefficients in to 'Poly' class,
       Eg:-  f = Poly(3, 2, 1)     -->   f(x) = 3x^2 + 2x + 1
             f = Poly(1, 0, 0, 9)  -->   f(x) = x^3 + 9
    by Kavienan J
    ©Copyrights 2019 xtreme™
    """

    def __init__(self, *coefs):

        """Pass the coefficients in the order of x term's degree"""

        if coefs[0] and coefs:
            for deg in range(len(coefs)):
                self.__dict__['x'+str(deg)] = coefs[::-1][deg]
            self.__dict__ = self._ordering(self.__dict__)
        else:
            raise ValueError('Cannot pass empty coefficient for greatest degree of x')

    def expr(self):

        """Raw format/Readable expression of the polynomial"""

        expr = []
        for deg, cof in self.__dict__.items():
            term = ''
            if cof and cof != 1:
                term = str(cof) + 'x' if (deg[1:] == '1') else str(cof) + 'x^' + deg[1:]
            elif cof:
                term = 'x' if deg[1:] == '1' else 'x^' + deg[1:]
            if deg[1:] == '0':
                term = str(cof) if cof else ''
            term = '+' + term if ((expr and term) and ('-' not in term)) else term
            expr.append(term)
        return ''.join(expr)

    def _ordering(self, fun):
        """ Returns a dict object with keys ordered to highest degree to the lowest """
        return {deg: fun[deg] for deg in sorted(fun)[::-1]}

    def _divisor(self, other):
        """ Returns quotient and remainder of division """
        remainder = self
        term_deg = len(remainder)
        quotient = 0
        while term_deg > 0:
            term_cof = remainder[len(remainder)]/other[len(other)]
            term_deg = len(remainder) - len(other)
            term = Poly(*[0 if i else term_cof for i in range(term_deg + 1)]) if term_deg else Poly(term_cof)
            quotient = term + quotient
            remainder = remainder - (term * other)
        return quotient, remainder

    def __repr__(self):
        return "<Polynomial[" + "+".join(
            ['(' + str(cof) + 'x^' + deg[1:] + ')' for deg, cof in self.__dict__.items()]
        ) + "]>"

    def __len__(self):
        """Degree of Polynomial"""
        return len(self.__dict__) - 1

    def __add__(self, other):
        x_coefs = self.__dict__.copy()
        if isinstance(other, (int, float)):
            x_coefs['x0'] = x_coefs['x0'] + other if 'x0' in x_coefs.keys() else other
        else:  # if Poly object,
            new_coefs = dict()
            for deg, cof in other.__dict__.items():
                n_coef = x_coefs[deg] + cof if deg in x_coefs.keys() else cof
                if n_coef != 0 or new_coefs:
                    x_coefs[deg] = n_coef
                    new_coefs[deg] = new_coefs
                else:
                    del x_coefs[deg]
        return Poly(*self._ordering(x_coefs).values()) if len(x_coefs) else 0

    def __sub__(self, other):
        x_coefs = self.__dict__.copy()
        if isinstance(other, (int, float)):
            x_coefs['x0'] = x_coefs['x0'] - other if 'x0' in x_coefs.keys() else -other
        else:  # if Poly object,
            new_coefs = dict()
            for deg, cof in other.__dict__.items():
                n_coef = x_coefs[deg] - cof if deg in x_coefs.keys() else -cof
                if n_coef != 0 or new_coefs:
                    x_coefs[deg] = n_coef
                    new_coefs[deg] = new_coefs
                else:
                    del x_coefs[deg]
        return Poly(*self._ordering(x_coefs).values()) if len(x_coefs) else 0

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ if isinstance(other, Poly) else False

    def __mul__(self, other):
        x_coefs = self.__dict__.copy()
        if isinstance(other, (int, float)):
            return Poly(*(cof*other for cof in x_coefs.values()))
        # if Poly object,
        new_coefs = dict()
        for deg1, cof1 in other.__dict__.items():
            for deg2, cof2 in x_coefs.items():
                deg = 'x' + str(int(deg1[1:]) + int(deg2[1:]))
                new_coefs[deg] = new_coefs[deg] + (cof1 * cof2) if deg in new_coefs.keys() else cof1 * cof2
        return Poly(*self._ordering(new_coefs).values())

    def __pow__(self, index):
        if not index:
            return 1
        elif index > 0:
            value = self
            for _ in range(1, index):
                value *= self  # n^3 ===> for _ in range(1, 3): answer_n *= n;
        else:
            raise ValueError('negative index is not allowed for polynomials')
        return Poly(*value.__dict__.values())

    def __truediv__(self, other):
        x_coefs = self.__dict__.copy()
        if isinstance(other, (int, float)):
            # TODO: filter non float values into integers
            return Poly(*(cof / other for cof in x_coefs.values()))
        # if Poly object,
        if len(self) < len(other) and type(self) == type(other):
            raise ArithmeticError("Can't divide lower degree polynomial with higher degree polynomial")
        return self._divisor(other)[0]

    def __floordiv__(self, other):
        x_coefs = self.__dict__.copy()
        if isinstance(other, (int, float)):
            new_coefs = dict()
            for deg in x_coefs.keys():
                val = x_coefs[deg] // other
                if val or new_coefs:
                    new_coefs[deg] = val
            return Poly(*new_coefs.values()) if new_coefs else 0
        if len(self) < len(other) and type(self) == type(other):
            raise ArithmeticError("Can't divide lower degree polynomial with higher degree polynomial")
        return self._divisor(other)[0]

    def __mod__(self, other):
        x_coefs = self.__dict__.copy()
        if isinstance(other, (int, float)):
            new_coefs = dict()
            for deg in x_coefs.keys():
                val = x_coefs[deg] % other
                if val or new_coefs:
                    new_coefs[deg] = val
            return Poly(*new_coefs.values()) if new_coefs else 0
        if len(self) < len(other) and type(self) == type(other):
            raise ArithmeticError("Can't divide lower degree polynomial with higher degree polynomial")
        return self._divisor(other)[1]

    def __getitem__(self, pos):
        if pos in self.__dict__.keys():
            return self.__dict__[pos]  # item accessed through key/variable
        elif pos in range(len(self.__dict__)):
            return self.__dict__['x' + str(pos)]  # item accessed through index of coefficient
        else:
            if isinstance(pos, str):
                raise KeyError("coefficient for the given variable doesn't exist")
            else:
                raise IndexError("coefficient for the given x degree doesn't exist")

    def __call__(self, x):
        return sum([(x ** deg) * self[cof] for deg, cof in enumerate(sorted(self.__dict__))])
