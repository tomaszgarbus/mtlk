import math
import matplotlib.pyplot as plt
import numpy as np

class BezierCurve:
    """Representation of a Bezier curve. Not necessarily efficient."""
    def __init__(self, control_points: list[tuple[float, float]]):
        self._b = control_points
        self._n = len(control_points)


    def evaluate(self, t: float) -> tuple[float, float]:
        """Evaluate the curve at t \in [0; 1]."""
        if t < 0 or t > 1:
            return ValueError("t must be in range [0; 1]")
        bt = (0., 0.)
        for i in range(self._n):
            mul = (math.comb(self._n - 1, i)
                   * math.pow(t, i)
                   * math.pow(1 - t, self._n - 1 - i))
            bt = (
                bt[0] + mul * self._b[i][0],
                bt[1] + mul * self._b[i][1]
            )
        return bt


    def plot(self, resolution=400) -> None:
        """Displays a figure with a plot of the curve."""
        xs = list(np.linspace(0, 1, resolution))
        ys = list(map(self.evaluate, xs))
        plt.plot(*zip(*self._b))
        plt.plot(*zip(*ys))
        plt.show()


if __name__ == '__main__':
    sample_bc = BezierCurve([(1, 1), (2, 8), (6, 0), (8, 7)])
    sample_bc.plot()
