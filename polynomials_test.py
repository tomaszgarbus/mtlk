import unittest
import math
from polynomials import Polynomial

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

    def test_derivative(self):
        """Tests for derivative."""
        poly = Polynomial([4, 8, 9, 3])
        self.assertEqual(poly.derivative(), Polynomial([8, 9, 3]))

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

if __name__ == '__main__':
    unittest.main()
