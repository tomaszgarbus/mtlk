import unittest
from stable_marriages import stable_marriages, stable_marriages_with_capacity, validate_marriages, validate_marriages_with_capacity
import itertools as it

class TestStableMarriages(unittest.TestCase):

    def test_validation_wrong(self):
        """Tests that the validation function will detect unstable marriage."""
        m_prefs = [
            [3, 5, 4, 2, 1, 0],
            [2, 3, 1, 0, 4, 5],
            [5, 2, 1, 0, 3, 4],
            [0, 1, 2, 3, 4, 5],
            [4, 5, 1, 2, 0, 3],
            [0, 1, 2, 3, 4, 5],
        ]
        w_prefs = [
            [3, 5, 4, 2, 1, 0],
            [2, 3, 1, 0, 4, 5],
            [5, 2, 1, 0, 3, 4],
            [0, 1, 2, 3, 4, 5],
            [4, 5, 1, 2, 0, 3],
            [0, 1, 2, 3, 4, 5],
        ]
        m_to_w = [3, 5, 1, 4, 0, 2]
        assert not validate_marriages(m_to_w, m_prefs, w_prefs)
    
    def test_validation_ok(self):
        """Tests that the validation function will accept stable marriage."""
        m_prefs = [
            [3, 5, 4, 2, 1, 0],
            [2, 3, 1, 0, 4, 5],
            [5, 2, 1, 0, 3, 4],
            [0, 1, 2, 3, 4, 5],
            [4, 5, 1, 2, 0, 3],
            [0, 1, 2, 3, 4, 5],
        ]
        w_prefs = [
            [3, 5, 4, 2, 1, 0],
            [2, 3, 1, 0, 4, 5],
            [5, 2, 1, 0, 3, 4],
            [0, 1, 2, 3, 4, 5],
            [4, 5, 1, 2, 0, 3],
            [0, 1, 2, 3, 4, 5],
        ]
        m_to_w = [3, 5, 1, 0, 4, 2]
        assert validate_marriages(m_to_w, m_prefs, w_prefs)
    
    def test_stable_3x3(self):
        """Tests that all outputs are stable for all possible 3x3 inputs."""
        possible_prefs = list(it.permutations([0, 1, 2]))
        def generate_prefs():
            result = []
            for p1 in possible_prefs:
                for p2 in possible_prefs:
                    for p3 in possible_prefs:
                        result.append((p1, p2, p3))
            return result
        for m_prefs in generate_prefs():
            for w_prefs in generate_prefs():
                assert validate_marriages(
                    stable_marriages(m_prefs, w_prefs), m_prefs, w_prefs)


    def test_validation_w_capacity_wrong(self):
        """Tests that the validation function will detect unstable marriage."""
        s_prefs = [
            [0, 1, 2],
            [2, 0, 1],
            [2, 1, 0],
            [1, 0, 2],
            [2, 1, 0],
            [0, 2, 1],
            [0, 1, 2],
            [1, 2, 0],
            [0, 1, 2],
        ]
        h_prefs = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
            [2, 5, 7, 3, 6, 8, 0, 1, 4],
            [1, 3, 8, 2, 6, 5, 0, 7, 4],
        ]
        # This is unstable because 6-th student prefers hospital 0 and
        # hospital 0 prefers 6-th student over 7-th student.
        s_to_h = [0, 2, 2, 1, 2, 0, 1, 0, 1]
        assert not validate_marriages_with_capacity(s_to_h, s_prefs, h_prefs)


    def test_validation_w_capacity_ok(self):
        """Tests that the validation function will detect unstable marriage."""
        s_prefs = [
            [0, 1, 2],
            [2, 0, 1],
            [2, 1, 0],
            [1, 0, 2],
            [2, 1, 0],
            [0, 2, 1],
            [0, 1, 2],
            [1, 2, 0],
            [0, 1, 2],
        ]
        h_prefs = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
            [2, 5, 7, 3, 6, 8, 0, 1, 4],
            [1, 3, 8, 2, 6, 5, 0, 7, 4],
        ]
        s_to_h = [0, 2, 2, 1, 2, 0, 0, 1, 1]
        assert validate_marriages_with_capacity(s_to_h, s_prefs, h_prefs)
    

    def test_stable_w_capacity_3x3(self):
        """
        Tests that all outputs are stable for all possible 3x3 inputs.
        
        Capacity is set to 1, so we're just testing the different (general)
        implementation of the algorithm.
        """
        possible_prefs = list(it.permutations([0, 1, 2]))
        def generate_prefs():
            result = []
            for p1 in possible_prefs:
                for p2 in possible_prefs:
                    for p3 in possible_prefs:
                        result.append((p1, p2, p3))
            return result
        for m_prefs in generate_prefs():
            for w_prefs in generate_prefs():
                assert validate_marriages_with_capacity(
                    stable_marriages_with_capacity(
                        m_prefs, w_prefs, capacity=1),
                        m_prefs, w_prefs)


if __name__ == '__main__':
    unittest.main()
