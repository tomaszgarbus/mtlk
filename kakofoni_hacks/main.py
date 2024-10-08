import gauss_elimination as ge
import json

def create_transforms_for_melody(melody: list[int]) -> dict[str, str]:
    """Creates transfoms for variables to play the melody.

    Returns a dict of unparsed transforms."""
    transforms = {}
    transforms['x'] = 'x + 1'
    transforms['ydelta'] = str(ge.polynomial_interpolation(
        [(i, 0) for i in range(11)] + [(11, 1), (12, 0)], 13
    ))
    transforms['y'] = 'y + ydelta'

    # Pad melody with 0s.
    melody += [0 for _ in range(169 - len(melody))]

    # Melody is m_0, m_1, ..., m_169.
    # We will encode it in a function \sum_{i < 13, j < 13} w_{ij} * y^i * x^j.
    # Values of x, y:
    # (0, 0), (1, 0), ..., (12, 0), (0, 1), (1, 1), ..., (12, 1), ..., (12, 12)
    matrix = []
    for y in range(13):
        for x in range(13):
            matrix.append([
                ((y ** i) % 13) * ((x ** j) % 13) % 13
                for i in range(13) for j in range(13)
            ] + [melody[y * 13 + x]])
    
    ge.gauss_elimination_mod(matrix, 13)
    # ge.print_matrix(matrix)

    z_components = []
    for y in range(13):
        for x in range(13):
            z_components.append(f'{matrix[y * 13 + x][169]} * x^{x} * y^{y}')
    transforms['z'] = ' + '.join(z_components)

    ### TEST
    # results = []
    # for y in range(13):
    #     for x in range(13):
    #         s = 0
    #         for i in range(13):
    #             for j in range(13):
    #                 s += matrix[i * 13 + j][169] * (y ** i) * (x ** j) % 13
    #         s %= 13
    #         results.append(s == melody[y * 13 + x])

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
    melody = [
      5,
      12, 9, 9, 9, 7, 5, 5, 10,
      10, 9, 9, 7, 7, 5, 5, 5,
      12, 9, 9, 7, 7, 5, 5, 2,
      2, 0, 0, 0, 0, 0, 0,
    ]
    melody = melody * (169 // len(melody))
    print(json.dumps(create_config_for_melody(melody)))