"""
A simple script for measuring bias in the stable marriages algorithm.

It generates random preferences for men and women, runs the algorithm many
times and computes the average satisfaction measure for both sexes.

Satisfaction measure:
For an individual man, let's say he was paired with the j-th woman on his
preference list (our of n women). Then his satisfaction score is:
    1 - j/n
We cound indices from 0.
Satisfaction measure for all men is the average over all men.
For example if every man is matched with his favourite woman, the satisfaction
score for men is 1.

We compute analogous measure for women.

To measure the bias, the script compares which sex is more satisfied with
the outcome of the matching on average.
"""

import argparse
from tqdm import trange
from stable_marriages import stable_marriages, build_ranking, invert
from random import shuffle
import numpy as np

def gen_prefs(n: int) -> tuple[list[list[int]], tuple[list[list[int]]]]:
    """Generates random preferences for men and women."""
    res = []
    for _ in range(2):
        prefs = [
            [i for i in range(n)]
            for j in range(n)
        ]
        for j in range(n):
            shuffle(prefs[j])
        res.append(prefs)
    return tuple(res)


def satisfaction_score(prefs: list[list[int]], assignments: list[int]) -> float:
    """
    Computes satisfaction score for one gender.
    """
    ranking = build_ranking(prefs)
    score = 0.
    n = len(assignments)
    for i, j in enumerate(assignments):
        score += (1 - ranking[i][j] / n) / n
    return score


def report(scores: list[float], gender: str) -> None:
    """Report scores for one gender."""
    print(
        f"{gender}:",
        f"mean: {np.mean(scores)}",
        f"stddev: {np.std(scores)}",
        sep="\n"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Measure bias in stable marriages algorithm.')
    parser.add_argument(
        "--n", type=int, default=5, help="Number of men and women.")
    parser.add_argument(
        "--rounds", type=int, default=30,
        help="Number of rounds to average over."
    )
    args = parser.parse_args()

    men_scores = []
    women_scores = []

    for round_num in trange(args.rounds):
        men_prefs, women_prefs = gen_prefs(args.n)
        marriages = stable_marriages(men_prefs, women_prefs)
        men_scores.append(satisfaction_score(
            men_prefs, marriages
        ))
        women_scores.append(satisfaction_score(
            women_prefs, invert(marriages)
        ))

    report(men_scores, "MEN")
    report(women_scores, "WOMEN")
