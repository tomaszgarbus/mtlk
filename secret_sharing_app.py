"""
A web app implementing task 2.12 from the book.

Specifically, it implements a distribution and reconstruction of secret
protocol in a modulo arithmetic with 32-bit modulus p.
"""
from functools import reduce

class PolynomialModulo:
    def __init__(self, coeffs: list[int], modulo: int):
        self._coeffs = coeffs
        self._modulo = modulo
    
    def eval(self, x):
        """Evaluates self at `x`, using Horner method."""
        return reduce(
          lambda acc, coeff: (acc * x + coeff) % self._modulo,
          self._coeffs[::-1],
          0)

if __name__ == '__main__':
    pass