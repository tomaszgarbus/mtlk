
class DividedDifferences:
    """A class for computation and then fast retrieval of divided differences
    for a group of points."""
    def __init__(self, points: list[tuple[float, float]]):
        """Points must be in format [x, y]."""
        self._points = points
        self._matrix = [[0 for _ in points] for _ in points]
        self._preprocessed = False
    
    def _maybe_preprocess(self):
        if self._preprocessed:
            return
        for i, p in enumerate(self._points):
            self._matrix[i][i] = p[1]
        n = len(self._points)
        for i in range(1, n):
            for j in range(i - 1, -1, -1):
                self._matrix[j][i] = (
                    self._matrix[j+1][i] - self._matrix[j][i-1]
                ) / (self._points[i][0] - self._points[j][0])
        self._preprocessed = True
    
    def retrieve(self, i0, i1) -> float:
        assert(i0 <= i1)
        self._maybe_preprocess()
        return self._matrix[i0][i1]
