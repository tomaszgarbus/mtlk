import gauss_elimination as ge
import json

def create_transforms_for_melody(melody: list[int]) -> dict[str, str]:
    """Creates transfoms for variables to play the melody.

    Returns a dict of unparsed transforms."""
    transforms = {}
    transforms['x'] = 'x + 1'
    transforms['ydelta'] = str(ge.polynomial_interpolation(
        [(i, 0) for i in range(12)] + [(12, 1)], 13
    ))
    transforms['y'] = 'y + ydelta'

    # Pad melody with 0s.
    melody += [0 for _ in range(169 - len(melody))]

    # Melody is m_0, m_1, ..., m_169.
    # We will encode it in a function \sum_{i < 13, j < 13} w_{ij} * x^i * y^j.
    # Values of x, y:
    # (0, 0), (1, 0), ..., (12, 0), (0, 1), (1, 1), ..., (12, 1), ..., (12, 12)
    matrix = []
    for y in range(13):
        for x in range(13):
            matrix.append([
                ((x ** j) % 13) * ((y ** i) % 13) % 13
                for i in range(13) for j in range(13)
            ] + [melody[y * 13 + x]])
    
    ge.gauss_elimination_mod(matrix, 13)
    ge.print_matrix(matrix)

    z_components = []
    for i in range(13):
        for j in range(13):
            z_components.append(f'{matrix[i * 13 + j][169]} * x^{j} * y^{i}')
    transforms['z'] = ' + '.join(z_components)
    return transforms


def create_config_for_melody(melody: list[int]) -> dict:
    """Creates a config for melody.
    
    For now, assumes len(melody) < 170.
    
    Returns config."""
    assert len(melody) < 170, "longer melodies not supported yet"
    
    result = {
        'variables': ['x', 'ydelta', 'y', 'z'],
        'startState': {
            'x': 0,
            'ydelta': 0,
            'y': 0,
            'z': melody[0],
        },
        'unparsedVarTransforms': create_transforms_for_melody(melody),
        'playVariable': {
          'x': False,
          'ydelta': False,
          'y': False,
          'z': True
        },
        'variableOctaves': {
            'x': 2, 'y': 2, 'ydelta': 2,
            'z': 3
        },
        'activeOctaves': {},
        'bpm': 180,
        'downloadMidi': False,
    }

    return result

if __name__ == '__main__':
    print(json.dumps(create_config_for_melody([1, 2, 3] * 30)))