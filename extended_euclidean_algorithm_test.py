import unittest
from extended_euclidean_algorithm import egcd

class TestExtendedEuclideanAlgorithm(unittest.TestCase):

    def test_egcd(self):
        self.assertEqual(egcd(15, 11), (1, 3, -4))
        self.assertEqual(egcd(11, 15), (1, -4, 3))
        self.assertEqual(egcd(13, 4), (1, 1, -3))
        self.assertEqual(egcd(4, 13), (1, -3, 1))
        self.assertEqual(egcd(28, 14), (14, 0, 1))
        self.assertEqual(egcd(14, 28), (14, 1, 0))

if __name__ == '__main__':
    unittest.main()
