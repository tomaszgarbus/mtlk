"""CRT (Chinese Remainder Theorem) solver.

https://www.math.cmu.edu/~mradclif/teaching/127S19/Notes/ChineseRemainderTheorem.pdf
"""
import itertools
import operator
from modulo_division import inv_mod

def crt_solve(x: list[int], y: list[int]) -> int:
    """Solves a system of congruencies of form $z \equiv y_i mod x_i$.
    
    Assumes that x_0 * ... * x_n fits in 32 bit int."""
    if len(x) != len(y):
        raise ValueError("x and y must be of equal length!")
    X = 1
    for e in x:
        X *= e
    z = 0
    for i in range(len(x)):
        m = X // x[i]
        m_inv = inv_mod(m, x[i])
        z += m * y[i] * m_inv
        z %= X
    return z

if __name__ == '__main__':
    print(crt_solve([5, 7, 11], [2, 3, 10]))