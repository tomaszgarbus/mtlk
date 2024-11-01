import heapq

def _build_ranking(preferences: list[list[int]]) -> list[list[int]]:
    """Transforms the preferences for one gender into a ranking.
    
    If output[i][j] = k, then it means that for person `i`, the person `j` of opposite gender
    is the k-th best choice (indexing from 0)."""
    N = len(preferences)
    ranking = [[0 for _ in range(N)] for _ in range(N)]
    for person in range(N):
        for idx, candidate in enumerate(preferences[person]):
            ranking[person][candidate] = idx
    return ranking


def _invert(assignment: list[int]) -> list[int]:
    """Inverts the assignment to be seen from the perspective of the other gender."""
    N = len(assignment)
    inverted = [None for _ in assignment]
    for person, partner in enumerate(assignment):
        inverted[partner] = person
    return inverted


def stable_marriages(
    men_preferences: list[list[int]],
    women_preferences: list[list[int]]
) -> list[int]:
    """
    Produces a stable matching between men and women.

    Stable means that there is no such pair of man M and woman W that M and W are not paired and M and W both like each
    other more than their assigned partners.

    Men and women are indexed from 0 to N. We assume equal count of men and women.

    On input, men_preferences[i] is a sorted list of all N women from most preferred to least.

    On output, the function produces the list of matches from men's perspective. That is, output[i] is the woman
    matched to the i-th man.
    """
    N = len(men_preferences)
    assert len(women_preferences) == N

    # Build women's ranking of men for faster lookup.
    women_ranking = _build_ranking(women_preferences)

    # Next woman to propose to for each man.
    next_suited = [0 for _ in range(N)]
    # Men who either don't have assignment yet or lost it to another suitor.
    unassigned_men = [i for i in range(N)]
    # Man to woman assignments.
    m_to_w = [None for _ in range(N)]
    # Woman to man assignments.
    w_to_m = [None for _ in range(N)]
    while unassigned_men:
        suitor = unassigned_men.pop()
        suited = men_preferences[suitor][next_suited[suitor]]
        next_suited[suitor] += 1
        if w_to_m[suited] is None:
            m_to_w[suitor] = suited
            w_to_m[suited] = suitor
        else:
            prev_suitor = w_to_m[suited]
            if women_ranking[suited][suitor] < women_ranking[suited][prev_suitor]:
                m_to_w[suitor] = suited
                w_to_m[suited] = suitor
                m_to_w[prev_suitor] = None
                unassigned_men.append(prev_suitor)
            else:
                unassigned_men.append(suitor)
    assert validate_marriages(m_to_w, men_preferences, women_preferences), (
        m_to_w, men_preferences, women_preferences
    )
    return m_to_w


def validate_marriages(
    m_to_w: list[int],
    men_preferences: list[list[int]],
    women_preferences: list[list[int]],
) -> bool:
    """Validates that nobody has incentive to cheat on their assigned partner.
    
    Doesn't validate other correctness constraints such as that everyone has exactly
    one partner etc."""
    N = len(m_to_w)
    w_to_m = _invert(m_to_w)
    men_ranking = _build_ranking(men_preferences)
    women_ranking = _build_ranking(women_preferences)
    for m in range(N):
        for w in range(N):
            if m_to_w[m] == w:
                continue
            elif (
                men_ranking[m][w] < men_ranking[m][m_to_w[m]]
                and women_ranking[w][m] < women_ranking[w][w_to_m[w]]):
                return False
    return True


# TODO: rewrite regular stable marriage as a special case of this implementation.
def stable_marriages_with_capacity(
    student_preferences: list[list[int]],
    hospitals_preferences: list[list[int]],
    capacity: int,
) -> list[int]:
    """
    Produces a stable matching with capacity between medical students and hospitals.

    Students are indexed from 0 to N, hospitals from 0 to M. We assume that N = M x capacity.

    On input, student_preferences[i] is a sorted list of all M hospitals from most preferred to least.

    On output, the function produces the list of matches from the students' perspective. That is, output[i] the
    hospital into which i-th student got accepted.
    """
    N = len(student_preferences)
    M = len(hospitals_preferences)

    assert N == M * capacity

    # Hospitals' ranking of students for faster lookup.
    hospitals_ranking = _build_ranking(hospitals_preferences)
    # Students who either don't have assignment yet or lost it to another student.
    unassigned_students = [i for i in range(N)]
    # Next hospital to try for each student.
    next_hospital = [0 for _ in range(N)]
    # Student to hospital assignments.
    s_to_h = [None for _ in range(N)]
    # Hospital to student assignments.
    # Set contains elements (-ranking, student number) so that less preferred student
    # always lands as smallest element.
    h_to_s: list[list[int, int]] = [set() for _ in range(M)]
    while unassigned_students:
        s = unassigned_students.pop()
        h = student_preferences[s][next_hospital[s]]
        next_hospital[s] += 1
        heapq.heappush(h_to_s[h], (-hospitals_ranking[h][s], s))
        if len(h_to_s) > capacity:
            _, dropped_s = heapq.heappop(h_to_s)
            s_to_h[dropped_s] = None
            unassigned_students.append(dropped_s)
    return s_to_h


if __name__ == "__main__":
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
    print(stable_marriages(m_prefs, w_prefs))
