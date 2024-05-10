# This import is needed to postpone type evaluation after the creation of the
# class.
# https://stackoverflow.com/a/42845998
from __future__ import annotations
from functools import reduce

class Polynomial:
    def __init__(self,
                 coeffs: list[float]):
        self._coeffs = coeffs
        while len(self._coeffs) and self._coeffs[-1] == 0:
            self._coeffs.pop()
    
    @staticmethod
    def xpow(a: float, pow: int) -> Polynomial:
        """A helper util creating a polynomial a * x^pow."""
        return Polynomial([0] * pow + [a])

    @property
    def coeffs(self):
        """Getter for coeffs."""
        return self._coeffs.copy()
    
    @property
    def degree(self):
        """Degree of the polynomial."""
        return max(len(self._coeffs) - 1, 0)

    def derivative(self) -> Polynomial:
        """Returns a derivative of self."""
        return Polynomial(self._coeffs[1:])

    def evaluate(self, x0: float) -> float:
        """Evaluates self at `x0`, using Horner method."""
        return reduce(
          lambda acc, coeff: acc * x0 + coeff,
          self._coeffs[::-1],
          0)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Polynomial) and self._coeffs == value.coeffs:
            return True
        # For numeric values:
        if len(self._coeffs) == 1 and self._coeffs[0] == value:
            return True
        if not self._coeffs and value == 0:
            return True
        return False
    
    def __add__(self, other: Polynomial) -> Polynomial:
        new_coeffs = [0 for _ in range(max(self.degree, other.degree) + 1)]
        for i, coeff in enumerate(self.coeffs):
            new_coeffs[i] += coeff
        for i, coeff in enumerate(other.coeffs):
            new_coeffs[i] += coeff
        # Trimming of leading 0 coefficients will be done by constructor.
        return Polynomial(new_coeffs)
    
    def __mul__(self, other: Polynomial) -> Polynomial:
        coeffs = [0 for _ in range(len(self._coeffs) + len(other.coeffs))]
        for i, c1 in enumerate(self._coeffs):
            for j, c2 in enumerate(other.coeffs):
                coeffs[i + j] += c1 * c2
        return Polynomial(coeffs)

    def __neg__(self) -> Polynomial:
        return Polynomial([-c for c in self._coeffs])

    def __sub__(self, other: Polynomial) -> Polynomial:
        return self + -other
    
    def __str__(self) -> str:
        if not self._coeffs:
            return "0"
        s = ""
        for i, c in enumerate(self._coeffs):
            if i == 0:
                s += "%.2f" % c
            elif i == 1:
                s += "%.2f * x" % c
            else:
                 s += "%.2f * x^%d" % (c, i)
        return s

    def __repr__(self) -> str:
        return "Polynomial(%s)" % str(self._coeffs)

    def is_linear(self) -> bool:
        """True iff self is a linear polynomial."""
        return len(self._coeffs) <= 2

    def is_monic(self) -> bool:
        """True iff self is a monic polynomial."""
        return len(self._coeffs) and self._coeffs[-1] == 1

    def is_linear_monic(self) -> bool:
        """True iff self is a linear monic polynomial."""
        return self.is_linear() and self.is_monic()

    def synthetic_division(self, d: Polynomial) -> Polynomial:
        """Performs synthetic division of self by `d`."""
        return NotImplementedError()

    def long_division(self, d: Polynomial) -> tuple[Polynomial, Polynomial]:
        """Performs long division of self by `d`.
        
        Returns a pair (quotient, remainder)."""
        if d == 0:
            # TODO: Reconsider raise vs return.
            # Raise is _slightly_ easier to test.
            raise ValueError("The divisor must be non zero.")
        r = self  # Remainder
        q = Polynomial([])  # Quotient
        while r.degree >= d.degree:
            t = self.xpow(
                r.coeffs[-1] / d.coeffs[-1],
                r.degree - d.degree
            )
            q = q + t
            r = r - t * d
        return (q, r)

    def roots(self) -> list[float]:
        """Finds roots of the polynomial using"""
        return NotImplementedError()
