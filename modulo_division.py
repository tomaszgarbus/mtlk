from extended_euclidean_algorithm import egcd

def inv_mod(a: int, m: int):
    """Modular inversion.
    
    Returns a^(-1) in modular arithmetic modulo m."""
    d, x, _ = egcd(a, m)
    if d > 1:
        raise ValueError(f"{a} is not invertible mod {m}")
    if x < 0:
        x += m
    return x


def div_mod(a: int, b: int, m: int):
    """Returns a / b in modular arithmetic modulo m."""
    return a * inv_mod(b, m) % m