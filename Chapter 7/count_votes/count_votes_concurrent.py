#!/usr/bin/env python3.9

"""Counting votes using Fork/Join pattern"""

import typing as T
import random
from multiprocessing.pool import ThreadPool

Summary = T.Mapping[int, int]


def process_votes(pile: T.List[int], worker_count: int = 4) -> Summary:
    """Counts the number of votes each candidate received in parallel."""
    vote_count = len(pile)
    # vote per worker
    vpw = vote_count // worker_count

    # divide the votes among workers
    vote_piles = [
        pile[i * vpw:(i + 1) * vpw]
        for i in range(worker_count)
    ]

    # create thread pool
    with ThreadPool(worker_count) as pool:
        # map each chunk of votes to a worker and run them in parallel
        worker_summaries = pool.map(process_pile, vote_piles)

    # merge the worker summaries
    total_summary = {}
    for worker_summary in worker_summaries:
        print(f"Votes from staff member: {worker_summary}")
        for candidate, count in worker_summary.items():
            if candidate in total_summary:
                total_summary[candidate] += count
            else:
                total_summary[candidate] = count

    return total_summary


def process_pile(pile: T.List[int]) -> Summary:
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
