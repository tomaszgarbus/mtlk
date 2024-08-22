import unittest
from polynomials_modulo import PolynomialModulo, lagrange_interpolation

class PolynomialModuloTest(unittest.TestCase):

    def test_eq(self):
        self.assertEqual(
            PolynomialModulo([10000, 23, 19, -1], 10),
            PolynomialModulo([0, 3, 9, 9], 10)
        )
    
    def test_degree(self):
        self.assertEqual(
            PolynomialModulo([8, 4, 0, 0, 0, 10000], 10).degree,
            1
        )
        self.assertEqual(
            PolynomialModulo([8, 4, 0, 0, 0, 10001], 10).degree,
            5
        )

    def test_add(self):
        self.assertEqual(
            (PolynomialModulo([0, 3, 9, 9], 10)
             + PolynomialModulo([2, 4, -9, -5, 4], 10)),
             PolynomialModulo([2, 7, 0, -6, 4], 10))
    
    def test_interpolation(self):
        # From https://math.stackexchange.com/questions/621406/lagrange-interpolating-polynomial-using-modulo
        self.assertEqual(
            lagrange_interpolation(
                [(1, 200), (2, 500), (3, 1000)],
                251
            ),
            PolynomialModulo([100, 0, 100], 251)
        )

if __name__ == '__main__':
    unittest.main()