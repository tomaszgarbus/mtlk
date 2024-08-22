from modulo_division import inv_mod
from polynomials_modulo import PolynomialModulo

def print_matrix(m):
    print("matrix: ")
    for row in m:
        print(row)
    print()
    

def gauss_elimination(matrix: list[list[int]]):
    """Performs the Gauss elimination on the given matrix."""

    def swap_rows(m, r1, r2):
        """Swaps row `r1` with row `r2`."""
        m[r1], m[r2] = m[r2], m[r1]
    
    def mult_row(m, r, x):
        """Multiplies row `r` by factor of `x`."""
        m[r] = list(map(lambda e: e * x, m[r]))
    
    def add_mult_row(m, r1, r2, x):
        """Adds `r1` multiplied by `x1` to `r2`."""
        for i in range(len(m[r2])):
            m[r2][i] += m[r1][i] * x

    n = len(matrix)
    m = len(matrix[0])
    # matrix = np.asarray(matrix)
    # print_matrix(matrix)
    for i in range(m - 1):
        if matrix[i][i] == 0:
            j = i + 1
            while j < n and matrix[j][i] != 0:
                j += 1
            if j < n:
                swap_rows(matrix, i, j)
        if matrix[i][i] != 0:
            mult_row(matrix, i, 1 / matrix[i][i])
            for j in range(i + 1, n):
                add_mult_row(matrix, i, j, -matrix[j][i])
        # print_matrix(matrix)
    
    for i in range(m - 2, -1, -1):
        if matrix[i][i] != 0:
            for j in range(i - 1, -1, -1):
                add_mult_row(matrix, i, j, -matrix[j][i])
        # print_matrix(matrix)


def gauss_elimination_mod(matrix: list[list[int]], mod: int):
    """Gaussian elimination modulo `mod`."""

    def print_matrix(m):
        print("matrix: ")
        for row in m:
            print(row)
        print()

    def swap_rows(m, r1, r2):
        """Swaps row `r1` with row `r2`."""
        m[r1], m[r2] = m[r2], m[r1]
    
    def mult_row(m, r, x):
        """Multiplies row `r` by factor of `x`."""
        m[r] = list(map(lambda e: (e * x) % mod, m[r]))
    
    def add_mult_row(m, r1, r2, x):
        """Adds `r1` multiplied by `x1` to `r2`."""
        for i in range(len(m[r2])):
            m[r2][i] += m[r1][i] * x
            m[r2][i] %= mod

    n = len(matrix)
    m = len(matrix[0])
    # matrix = np.asarray(matrix)
    # print_matrix(matrix)
    for i in range(m - 1):
        if matrix[i][i] == 0:
            j = i + 1
            while j < n and matrix[j][i] != 0:
                j += 1
            if j < n:
                swap_rows(matrix, i, j)
        if matrix[i][i] != 0:
            mult_row(matrix, i, inv_mod(matrix[i][i], mod))
            for j in range(i + 1, n):
                add_mult_row(matrix, i, j, -matrix[j][i])
        # print_matrix(matrix)
    
    for i in range(m - 2, -1, -1):
        if matrix[i][i] != 0:
            for j in range(i - 1, -1, -1):
                add_mult_row(matrix, i, j, -matrix[j][i])
        # print_matrix(matrix)


def polynomial_interpolation(
        points: list[tuple[int, int]], m: int) -> PolynomialModulo:
    """Interpolates a polynomial in modular arithmetic modulo `m`.

    Uses Gauss elimination.

    Returns a polynomial of degree n going through all n+1 provided points.

    Points must be in format [x, y]."""
    matrix = []
    deg = len(points) - 1
    for p in points:
        x, y = p
        matrix.append([
            x ** j for j in range(deg + 1)
        ] + [y])

    gauss_elimination_mod(matrix, m)

    return PolynomialModulo([
        matrix[i][deg + 1] for i in range(deg + 1)
    ], m)


if __name__ == '__main__':
    print(polynomial_interpolation(
        [(1, 200), (2, 500), (3, 1000)],
        251
    ))
