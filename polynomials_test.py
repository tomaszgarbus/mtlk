import unittest
import math
from polynomials import Polynomial, interpolate, newton_interpolation
import numpy as np

class TestPolynomials(unittest.TestCase):

    def test_eq(self):
        """Tests for equality operator."""
        poly1 = Polynomial([1, 2, 3])
        poly2 = Polynomial([1, 2, 3])
        poly3 = Polynomial([1, 2, 3, 0])
        poly4 = Polynomial([0, 1, 2, 3])
        poly5 = Polynomial([1, 5, 6])
        self.assertEqual(poly1, poly2)
        self.assertEqual(poly2, poly3)
        self.assertNotEqual(poly1, poly4)
        self.assertNotEqual(poly1, poly5)
        self.assertEqual(Polynomial([0]), Polynomial([]))
        self.assertEqual(Polynomial([]), 0)
        self.assertEqual(Polynomial([0]), 0)
        self.assertEqual(Polynomial([5]), 5)
        self.assertNotEqual(Polynomial([5]), 0)

    def test_derivative(self):
        """Tests for derivative."""
        self.assertEqual(
            Polynomial([4, 8, 9, 3]).derivative(), Polynomial([8, 18, 9]))
        self.assertEqual(
            Polynomial([0, 0, 7, 90, 100]).derivative(), Polynomial([0, 14, 270, 400]))

    def test_evaluate(self):
        """Tests for evaluation."""
        poly = Polynomial([4, 8, 9, 3])
        self.assertAlmostEqual(poly.evaluate(1), 4 + 8 + 9 + 3)
        self.assertAlmostEqual(
            poly.evaluate(math.pi),
            4 + 8 * math.pi + 9 * math.pi ** 2 + 3 * math.pi ** 3)

    def test_properties(self):
        """Test for miscellaneous properties."""
        self.assertTrue(Polynomial([]).is_linear())
        self.assertFalse(Polynomial([]).is_monic())
        self.assertFalse(Polynomial([]).is_linear_monic())
        self.assertTrue(Polynomial([1]).is_linear())
        self.assertTrue(Polynomial([1]).is_monic())
        self.assertTrue(Polynomial([1]).is_linear_monic())
        self.assertTrue(Polynomial([9, 1]).is_linear())
        self.assertTrue(Polynomial([9, 1]).is_monic())
        self.assertTrue(Polynomial([9, 1]).is_linear_monic())
        self.assertFalse(Polynomial([2, 9, 1]).is_linear())
        self.assertTrue(Polynomial([2, 9, 1]).is_monic())
        self.assertFalse(Polynomial([2, 9, 1]).is_linear_monic())
        self.assertFalse(Polynomial([2, 9]).is_monic())
        self.assertEqual(Polynomial([]).degree, 0)
        self.assertEqual(Polynomial([1]).degree, 0)
        self.assertEqual(Polynomial([1, 1]).degree, 1)
        self.assertEqual(Polynomial([1, 1, 1]).degree, 2)
        self.assertTrue(Polynomial([]).is_constant())
        self.assertTrue(Polynomial([0]).is_constant())
        self.assertTrue(Polynomial([18]).is_constant())
        self.assertTrue(Polynomial([18, 0]).is_constant())
        self.assertFalse(Polynomial([18, 1]).is_constant())
    
    def test_add(self):
        self.assertEqual(Polynomial([0, 3, 9, -1]) + Polynomial([2, 4, -9, -5, 4]),
                         Polynomial([2, 7, 0, -6, 4]))
    
    def test_neg(self):
        self.assertEqual(-Polynomial([0, 3, 9, -1]), Polynomial([0, -3, -9, 1]))
    
    def test_sub(self):
        self.assertEqual(Polynomial([0, 3, 9, -1]) - Polynomial([2, 4, -9, -5, 4]),
                         Polynomial([-2, -1, 18, 4, -4]))

    def test_xpow(self):
        self.assertEqual(Polynomial.xpow(5, 0), Polynomial([5]))
        self.assertEqual(Polynomial.xpow(5, 1), Polynomial([0, 5]))
        self.assertEqual(Polynomial.xpow(5, 3), Polynomial([0, 0, 0, 5]))
    
    def test_mul(self):
        self.assertEqual(Polynomial([1, 2, 3]) * Polynomial([5]), Polynomial([5, 10, 15]))
        self.assertEqual(Polynomial([1, 2, 3]) * Polynomial([0]), Polynomial([]))
        self.assertEqual(Polynomial([1, 2, 3]) * 5, Polynomial([5, 10, 15]))
        self.assertEqual(Polynomial([1, 2, 3]) * 5.0, Polynomial([5, 10, 15]))
        self.assertEqual(Polynomial([1, 2, 3]) * 0, Polynomial([]))
        self.assertEqual(Polynomial([1, 2, 3]) * Polynomial([]), Polynomial([]))
        self.assertEqual(Polynomial([1, 1, 1, 1]) * Polynomial([1, 1, 1, 1]), Polynomial([1, 2, 3, 4, 3, 2, 1]))
    
    def test_long_division(self):
        self.assertEqual(
            Polynomial([-4, 0, -2, 1]).long_division(Polynomial([-3, 1])),
            (Polynomial([3, 1, 1]), Polynomial([5]))
        )
        self.assertEqual(
            Polynomial([-42, 0, -12, 1]).long_division(Polynomial([-3, 1])),
            (Polynomial([-27, -9, 1]), Polynomial([-123]))
        )
        self.assertEqual(
            Polynomial([-42, 0, -12, 1]).long_division(Polynomial([-3, 1, 1])),
            (Polynomial([-13, 1]), Polynomial([-81, 16]))
        )
        with self.assertRaises(ValueError):
            Polynomial([5, 4, 1]).long_division(0),
        with self.assertRaises(ValueError):
            Polynomial([5, 4, 1]).long_division(Polynomial([]))
    
    def test_short_division(self):
        self.assertEqual(
            Polynomial([-42, 0, -12, 1]).synthetic_division(Polynomial([-3, 1])),
            (Polynomial([-27, -9, 1]), Polynomial([-123]))
        )
        self.assertEqual(
            Polynomial([-4, 0, -2, 1]).synthetic_division(Polynomial([-3, 1])),
            (Polynomial([3, 1, 1]), Polynomial([5]))
        )
        with self.assertRaises(ValueError):
            Polynomial([5, 4, 1]).synthetic_division(0)
        with self.assertRaises(ValueError):
            Polynomial([5, 4, 1]).synthetic_division(Polynomial([]))
        with self.assertRaises(ValueError):
            Polynomial([5, 4, 1]).synthetic_division(Polynomial([1, 3]))
        with self.assertRaises(ValueError):
            Polynomial([5, 4, 1]).synthetic_division(Polynomial([1, 3, 0, 9]))
    
    def test_eval(self):
        np.testing.assert_almost_equal(
            Polynomial([1, 1, 1, 0, 1]).eval(2),
            1 + 2 + 4 + 16
        )
        np.testing.assert_almost_equal(
            Polynomial([5, 9, -1, 8, 4]).eval(17),
            5 + 9 * 17 - 1 * 17**2 + 8 * 17 ** 3 + 4 * 17 ** 4
        )
    
    def test_roots(self):
        np.testing.assert_almost_equal(
            Polynomial([-3, 1]).roots(),
            [3]
        )
        np.testing.assert_almost_equal(
            Polynomial([3, 0, 1]).roots(),
            []
        )
        np.testing.assert_almost_equal(
            sorted(Polynomial([-1, 0, 1]).roots()),
            [-1, 1]
        )
        np.testing.assert_almost_equal(
            sorted(Polynomial([18]).roots()),
            []
        )
        with self.assertRaises(ValueError):
            Polynomial([]).roots()
    
    def test_interpolation_validates_input(self):
        for method in ["newton", "lagrange"]:
            with self.subTest(method):
                with self.assertRaises(ValueError):
                    interpolate([
                        (5, 1),
                        (5, 2),
                        (8, 4)
                    ], method)
    
    def test_interpolation_sorts_input(self):
        for method in ["newton", "lagrange"]:
            with self.subTest(method):
                self.assertEqual(
                    interpolate([
                        (0, 4),
                        (9, 5),
                        (-13.5, 2.71),
                        (-0.99, 12.3)
                    ], method),
                    interpolate([
                        (-13.5, 2.71),
                        (-0.99, 12.3),
                        (0, 4),
                        (9, 5)
                    ], method)
                )
    
    def test_interpolation(self):
        # Test from https://en.wikipedia.org/wiki/Newton_polynomial
        for method in ["newton", "lagrange"]:
            with self.subTest(method):
                self.assertEqual(
                    interpolate([
                        (-3/2, -14.1014),
                        (-3/4, -0.931596),
                        (0, 0),
                        (3/4, 0.931596),
                        (3/2, 14.1014)
                    ], method),
                    Polynomial([
                        -0.00005, -1.4775, -0.00001, 4.83484
                    ])
                )

if __name__ == '__main__':
    unittest.main()
