"""
A web app implementing task 2.12 from the book.

Specifically, it implements a distribution and reconstruction of secret
protocol in a modulo arithmetic with 32-bit modulus p.
"""
# This import is needed to postpone type evaluation after the creation of the
# class.
# https://stackoverflow.com/a/42845998
from __future__ import annotations
from functools import reduce
from modulo_division import div_mod

class PolynomialModulo:
    def __init__(self, coeffs: list[int], modulo: int):
        self._modulo = modulo
        self._coeffs = list(map(lambda c: c % modulo, coeffs))
        while len(self._coeffs) and self._coeffs[-1] == 0:
            self._coeffs.pop()
    
    @property
    def coeffs(self):
        """Getter for coeffs."""
        return self._coeffs.copy()
    
    @property
    def modulus(self):
        """Getter for modulo."""
        return self._modulo
    
    @property
    def degree(self):
        """Degree of the polynomial."""
        return max(len(self._coeffs) - 1, 0)
    
    def __str__(self) -> str:
        if not self._coeffs:
            return "0"
        s = []
        for i, c in enumerate(self._coeffs):
            if c == 0.:
                continue
            if i == 0:
                s.append("%d" % c)
            elif i == 1:
                s.append("%d * x" % c)
            else:
                 s.append("%d * x^%d" % (c, i))
        return "(" + " + ".join(s) + ") mod %d" % self.modulus

    def __repr__(self) -> str:
        return "PolynomialModulo(%s, %d)" % (str(self._coeffs), self.modulus)

    def eval(self, x):
        """Evaluates self at `x`, using Horner method."""
        return reduce(
          lambda acc, coeff: (acc * x + coeff) % self._modulo,
          self._coeffs[::-1],
          0)
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, PolynomialModulo):
            if len(self._coeffs) != len(value.coeffs):
                return False
            for (c1, c2) in zip(self._coeffs, value.coeffs):
                if c1 != c2:
                    return False
            return True
        # For numeric values:
        return self.__eq__(PolynomialModulo([value], self.modulus))
    
    def __add__(self, other: PolynomialModulo) -> PolynomialModulo:
        if self.modulus != other.modulus:
            raise ValueError("Both arguments of + operation must have the \
                             same modulus")
        new_coeffs = [0 for _ in range(max(self.degree, other.degree) + 1)]
        for i, coeff in enumerate(self.coeffs):
            new_coeffs[i] += coeff
        for i, coeff in enumerate(other.coeffs):
            new_coeffs[i] += coeff
            new_coeffs[i] %= self._modulo
        # Trimming of leading 0 coefficients will be done by constructor.
        return PolynomialModulo(new_coeffs, self.modulus)

    def __mul__(self, other: PolynomialModulo | int) -> PolynomialModulo:
        if type(other) == int:
            return PolynomialModulo(
                [(other * c) % self._modulo for c in self._coeffs],
                self.modulus
            )
        if self.modulus != other.modulus:
            raise ValueError("Both arguments of * operation must have the \
                             same modulus")
        coeffs = [0 for _ in range(len(self._coeffs) + len(other.coeffs))]
        for i, c1 in enumerate(self._coeffs):
            for j, c2 in enumerate(other.coeffs):
                coeffs[i + j] += c1 * c2 % self._modulo
                coeffs[i + j] %= self._modulo
        return PolynomialModulo(coeffs, self._modulo)
        

def lagrange_interpolation(
        points: list[tuple[int, int]], m: int) -> PolynomialModulo:
    """Lagrange interpolation of a polynomial in modular arithmetic modulo `m`.

    Returns a polynomial of degree n going through all n+1 provided points.

    Points must be in format [x, y]."""
    points = sorted(points)
    xs, _ = zip(*points)
    if len(set(xs)) != len(xs):
        raise ValueError("xs must be unique")
    
    lagrange = PolynomialModulo([], m)

    for i in range(len(points)):
        denominator = 1
        numerator = PolynomialModulo([1], m)
        for j in range(len(points)):
            if i != j:
                numerator *= PolynomialModulo([-points[j][0], 1], m)
                denominator *= (points[i][0] - points[j][0]) % m
        lagrange += numerator * div_mod(points[i][1], denominator, m)

    return lagrange

if __name__ == '__main__':
    pass