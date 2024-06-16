# This import is needed to postpone type evaluation after the creation of the
# class.
# https://stackoverflow.com/a/42845998
from __future__ import annotations
from functools import reduce
from random import random

class Polynomial:
    """Representation of a Polynomial. Not necessarily efficient."""
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
        return Polynomial([c * (i + 1) for i, c in enumerate(self._coeffs[1:])])

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
        s = []
        for i, c in enumerate(self._coeffs):
            if c == 0.:
                continue
            if i == 0:
                s.append("%.2f" % c)
            elif i == 1:
                s.append("%.2f * x" % c)
            else:
                 s.append("%.2f * x^%d" % (c, i))
        return " + ".join(s)

    def __repr__(self) -> str:
        return "Polynomial(%s)" % str(self._coeffs)
    
    def is_constant(self) -> bool:
        """True iff is a constant value."""
        return len(self._coeffs) <= 1

    def is_linear(self) -> bool:
        """True iff self is a linear polynomial."""
        return len(self._coeffs) <= 2

    def is_monic(self) -> bool:
        """True iff self is a monic polynomial."""
        return len(self._coeffs) and self._coeffs[-1] == 1

    def is_linear_monic(self) -> bool:
        """True iff self is a linear monic polynomial."""
        return self.is_linear() and self.is_monic()

    def synthetic_division(self, d: Polynomial) -> tuple[Polynomial, Polynomial]:
        """Performs synthetic division of self by `d`.

        Returns a pair (quotient, remainder)."""
        if d == 0 or not d.is_linear_monic():
            raise ValueError("%s is not a linear monic polynomial" % d)
        r = [0 for _ in self._coeffs[:-1]] + [self._coeffs[-1]]
        i = len(self._coeffs) - 2
        for c in self._coeffs[-2::-1]:
            r[i] = c - r[i + 1] * d.coeffs[0]
            i -= 1
        return Polynomial(r[1:]), Polynomial([r[0]])

    def long_division(self, d: Polynomial) -> tuple[Polynomial, Polynomial]:
        """Performs long division of self by `d`.
        
        Returns a pair (quotient, remainder)."""
        if d == 0:
            # TODO: Reconsider raise vs return.
            # Raise is slightly easier to test.
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
  
    def __truediv__(self, other: Polynomial) -> Polynomial:
        """Divides self by other.
        
        Uses synthetic division for linear monic polynomials and long
        division for the general case."""
        if other.is_linear_monic():
            return self.synthetic_division(other)
        return self.long_division(other)

    def eval(self, x0: float) -> float:
        """Evaluates self using Horner's method.
        
        TODO: Check if there is a way to overload the () operator,
        i.e. use syntax a(5) instead of a.eval(5)."""
        val = 0.
        for c in self._coeffs[::-1]:
            val = c + val * x0
        return val

    def roots(self, max_steps = 100, eps = 1e-9) -> list[float]:
        """Finds roots of the polynomial using Newton's method."""
        if self == 0:
            raise ValueError("Trying to compute roots for 0 polynomial")
        if self.is_constant():
            return []
        der = self.derivative()
        x = 0.
        while abs(der.eval(x)) < eps:
            x = random()
        for _ in range(max_steps):
            if abs(self.eval(x)) < eps:
                break
            x = x - self.eval(x) / der.eval(x)
        if abs(self.eval(x)) >= eps:
            return []
        if len(self._coeffs) <= 2:
            return [x]
        return [x] + (self / Polynomial([-x, 1]))[0].roots(max_steps, eps)
