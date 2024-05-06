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

    @property
    def coeffs(self):
        """Getter for coeffs."""
        return self._coeffs.copy()

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
        return isinstance(value, Polynomial) and self._coeffs == value.coeffs

    def is_linear(self) -> bool:
        """True iff self is a linear polynomial."""
        return len(self._coeffs) <= 2

    def is_monic(self) -> bool:
        """True iff self is a monic polynomial."""
        return len(self._coeffs) and self._coeffs[-1] == 1

    def is_linear_monic(self) -> bool:
        """True iff self is a linear monic polynomial."""
        return self.is_linear() and self.is_monic()

    def synthetic_division(self) -> Polynomial:
        """Performs synthetic division of self."""
        return NotImplementedError()

    def long_division(self) -> Polynomial:
        """Performs long division of self."""
        return NotImplementedError()

    def roots(self) -> list[float]:
        """Finds roots of the polynomial using"""
        return NotImplementedError()
