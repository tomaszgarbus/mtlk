import unittest
from stable_marriages import stable_marriages, validate_marriages
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
        print(possible_prefs)
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
    
    def test_stable_4x4(self):
        """Tests that all outputs are stable for all possible 4x4 inputs."""
        possible_prefs = list(it.permutations([0, 1, 2, 3]))
        print(possible_prefs)
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


if __name__ == '__main__':
    unittest.main()
