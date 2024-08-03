import unittest
from crt_solver import crt_solve

class CrtSolverTest(unittest.TestCase):

    def test_crt_solve(self):
        self.assertEqual(
            crt_solve([5, 7, 11], [2, 3, 10]),
            87
        )

if __name__ == '__main__':
    unittest.main()
