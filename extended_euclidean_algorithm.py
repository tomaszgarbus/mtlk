from polynomials import Polynomial as P

def egcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean algorithm.

    Given two numbers a and b, computes their GCD and solves the equation
    ax + by = gcd(a, b). Returns a tuple (gcd, x, y).
    """
    r = [a, b]
    x = [1, 0]
    y = [0, 1]
    while b != 0:
        q = a // b
        r = a % b
        new_x = x[-2] - x[-1] * q
        new_y = y[-2] - y[-1] * q
        x.append(new_x)
        y.append(new_y)
        a, b = b, r
    return a, x[-2], y[-2]


def egcd_polynomial(a: P, b: P) -> tuple[P, P, P]:
    """
    Extended Euclidean algorithm for monic polynomials.
    """
    r = [a, b]
    x = [P([1]), P([0])]
    y = [P([0]), P([1])]
    while b != 0:
        q = a // b
        r = a % b
        new_x = -q * x[-1] + x[-2]
        new_y = -q * y[-1] + y[-2]
        x.append(new_x)
        y.append(new_y)
        a, b = b, r
    u = a.coeffs[-1]
    return (
        a * (1 / u),
        x[-2] * (1 / u),
        y[-2] * (1 / u)
    )
