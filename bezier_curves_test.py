import unittest
from bezier_curves import BezierCurve

class TestBezierCurves(unittest.TestCase):

    def test_eval(self):
        bc = BezierCurve([(1, 5), (3, 1), (7, 8)])
        self.assertEqual(bc.evaluate(0), (1, 5))
        self.assertEqual(bc.evaluate(1), (7, 8))
        self.assertEqual(bc.evaluate(0.5), (3.5, 3.75))

if __name__ == '__main__':
    unittest.main()
