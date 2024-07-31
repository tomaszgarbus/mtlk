import unittest
from modulo_division import div_inv, div_mod

class ModuloDivisionTest(unittest.TestCase):
    
    def test_div_inv(self):
        self.assertEqual(div_inv(11, 15), 11)
        self.assertEqual(div_inv(4, 11), 3)
        self.assertEqual(div_inv(3, 4), 3)
    
    def test_div_inv_not_invertible(self):
        with self.assertRaises(ValueError):
            div_inv(12, 15)
        with self.assertRaises(ValueError):
            div_inv(0, 15)
        with self.assertRaises(ValueError):
            div_inv(28, 14)
    
    def test_div_mod(self):
        self.assertEqual(div_mod(11, 15, 23), 13)

    def test_div_mod_not_invertible(self):
        with self.assertRaises(ValueError):
            div_mod(11, 15, 30)

if __name__ == '__main__':
    unittest.main()
