class Poly:

    """
    This class creates polynomial objects with x terms.
    Create a polynomial expression/object by passing in coefficients in to 'Poly' class,
       Eg:-  f = Poly(3, 2, 1)     -->   f(x) = 3x^2 + 2x + 1
             f = Poly(1, 0, 0, 9)  -->   f(x) = x^3 + 9

    Possible Operations,
        - Addition (+)
        - Subtraction (-)
        - Multiplication (✕)
        - Division (÷)
        - Powers (x^n)

    Function values --> f(x); x=n

    by Kavienan J
    ©Copyrights 2019 Xtreme™ Solutions
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

    @staticmethod
    def _ordering(fx):
        """ Returns a dict object with keys ordered to highest degree to the lowest """
        return {deg: int(fx[deg]) if float(fx[deg]).is_integer() else float(fx[deg]) for deg in sorted(fx)[::-1]}

    def _division(self, divisor, operator):
        """ Returns quotient and remainder of division """
        x_coefs = self.__dict__.copy()
        if isinstance(divisor, Poly):
            if len(self) < len(divisor):
                raise ArithmeticError("Can't divide lower degree polynomial with higher degree polynomial")
            elif not len(divisor):
                divisor = divisor[0]
            else:
                remainder = self
                quotient = 0
                while len(remainder) >= len(divisor):
                    _cof = remainder[len(remainder)] / divisor[len(divisor)]
                    _deg = len(remainder) - len(divisor)
                    _product = Poly(*[_cof] + [0 for _ in range(_deg)])
                    quotient = _product + quotient
                    remainder = remainder - (_product * divisor)
                return remainder if operator == '__mod__' else quotient
        operation = lambda val1, val2: type(val1)(val1).__getattribute__(operator)(val2)
        new_coefs = dict()
        for deg in x_coefs.keys():
            val = operation(x_coefs[deg], divisor)
            if val or new_coefs:
                new_coefs[deg] = val
        return Poly(*new_coefs.values()) if new_coefs else 0

    def _addition_and_subtraction(self, other, operator):
        x_coefs = self.__dict__.copy()
        operation = lambda val1, val2: type(val1)(val1).__getattribute__(operator)(val2)
        if isinstance(other, (int, float)):
            if other:
                other = Poly(other)
            else:
                return self
        new_coefs = dict()
        for deg, cof in other.__dict__.items():
            _coef = operation(x_coefs[deg], cof) if deg in x_coefs.keys() else operation(0, cof)
            if _coef != 0 or new_coefs:
                x_coefs[deg] = _coef
                new_coefs[deg] = new_coefs
            else:
                del x_coefs[deg]
        return Poly(*self._ordering(x_coefs).values()) if len(x_coefs) else 0

    def __repr__(self):
        return "<Polynomial[" + "+".join(
            ['(' + str(cof) + 'x^' + deg[1:] + ')' for deg, cof in self.__dict__.items()]
        ) + "]>"

    def __len__(self):
        """Degree of Polynomial"""
        return len(self.__dict__) - 1

    def __add__(self, other):
        return self._addition_and_subtraction(other, '__add__')

    def __sub__(self, other):
        return self._addition_and_subtraction(other, '__sub__')

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
        elif index >= 1:
            value = self
            for _ in range(1, index):
                value *= self  # n^3 ===> for _ in range(1, 3): answer_n *= n;
        else:
            raise ValueError('negative or decimal index is not allowed for polynomials')
        return Poly(*value.__dict__.values())

    def __truediv__(self, other):
        return self._division(other, '__truediv__')

    def __floordiv__(self, other):
        return self._division(other, '__floordiv__')

    def __mod__(self, other):
        return self._division(other, '__mod__')

    def __getitem__(self, pos):
        if pos in self.__dict__.keys():
            return self.__dict__[pos]  # item accessed through key/variable
        elif pos in range(len(self.__dict__)):
            return self.__dict__['x' + str(pos)]  # item accessed through index of coefficient
        if isinstance(pos, str):
            raise KeyError("coefficient for the given variable doesn't exist")
        else:
            raise IndexError("coefficient for the given x degree doesn't exist")

    def __call__(self, x):
        return sum([(x ** deg)*self[deg] for deg in range(len(self)+1)])
