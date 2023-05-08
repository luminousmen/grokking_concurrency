#!/usr/bin/env python3.9

"""Counting votes sequentially"""

import typing as T
import random

Summary = T.Mapping[int, int]


def process_votes(pile: T.List[int]) -> Summary:
    """Counts the number of votes each candidate received."""
    summary = {}
    for vote in pile:
        if vote in summary:
            summary[vote] += 1
        else:
            summary[vote] = 1
    return summary


if __name__ == "__main__":
    num_candidates = 3
    num_voters = 100000
    # generating a huge list of votes
    # each vote is an integer represents the selected candidate
    pile = [random.randint(1, num_candidates) for _ in range(num_voters)]
    counts = process_votes(pile)
    print(f"Total number of votes: {counts}")
