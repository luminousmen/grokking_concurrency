#!/usr/bin/env python3

"""Counting votes using Fork/Join pattern"""

import typing as T
import random
from math import ceil
from threading import Thread


class StaffMember(Thread):
    def __init__(self, votes: T.List[int]):
        super().__init__()
        self.votes = votes
        self.summary = {}

    def run(self) -> None:
        for vote in self.votes:
            if self.summary.get(vote):
                self.summary[vote] += 1
            else:
                self.summary[vote] = 1

    def join(self, *args) -> T.Dict[int, int]:
        # join method that blocks the thread until the child threads has finished
        Thread.join(self, *args)
        return self.summary


def process_votes(votes: T.List[int]) -> None:
    jobs = []
    vote_count = len(votes)
    member_count = 4
    vote_per_pile = ceil(vote_count / member_count)

    # ---- Fork step ----
    for i in range(member_count):
        pile = votes[i * vote_per_pile:i * vote_per_pile + vote_per_pile]
        p = StaffMember(pile)
        jobs.append(p)
    
    for j in jobs:
        j.start()
    # ---- End Fork step ----
    # ---- Join step ----
    votes_summaries = []
    for j in jobs:
        votes_summaries.append(j.join())

    total_summary = {}
    for vote_summary in votes_summaries:
        for candidate in vote_summary:
            # summation of each key
            if total_summary.get(candidate):
                total_summary[candidate] += vote_summary[candidate]
            else:
                total_summary[candidate] = vote_summary[candidate]
    print(f"Total number of votes: {total_summary}")
    # ---- End Join step ----


if __name__ == "__main__":
    num_candidates = 3
    num_voters = 100000
    # generating a huge list of votes
    # each vote is an integer represents the selected candidate
    votes = [random.randint(1, num_candidates) for _ in range(num_voters)]
    process_votes(votes)
