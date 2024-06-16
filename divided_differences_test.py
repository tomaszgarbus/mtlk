import unittest
from divided_differences import DividedDifferences

class TestDividedDifferences(unittest.TestCase):

    def test_basic(self):
        """Basic scenario test."""
        # From:
        # https://psu.pb.unizin.org/polynomialinterpretation/chapter/chapter-two-newtons-divided-difference-interpolation/
        dd = DividedDifferences([
            (-2,	25.2),
            (-1, 11.3),
            (0, 2),
            (1, -2.7),
            (2, -2.8)
        ])
        self.assertAlmostEqual(dd.retrieve(0, 0), 25.2)
        self.assertAlmostEqual(dd.retrieve(1, 1), 11.3)
        self.assertAlmostEqual(dd.retrieve(2, 2), 2)
        self.assertAlmostEqual(dd.retrieve(3, 3), -2.7)
        self.assertAlmostEqual(dd.retrieve(4, 4), -2.8)
        self.assertAlmostEqual(dd.retrieve(0, 1), -13.9)
        self.assertAlmostEqual(dd.retrieve(1, 2), -9.3)
        self.assertAlmostEqual(dd.retrieve(2, 3), -4.7)
        self.assertAlmostEqual(dd.retrieve(3, 4), -0.1)
        self.assertAlmostEqual(dd.retrieve(0, 2), 2.3)
        self.assertAlmostEqual(dd.retrieve(1, 3), 2.3)
        self.assertAlmostEqual(dd.retrieve(2, 4), 2.3)
        self.assertAlmostEqual(dd.retrieve(0, 3), 0)
        self.assertAlmostEqual(dd.retrieve(1, 4), 0)
        self.assertAlmostEqual(dd.retrieve(0, 4), 0)

if __name__ == '__main__':
    unittest.main()
