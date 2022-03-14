#!/usr/bin/env python3

#
"""Counting votes using Fork/Join pattern"""

import typing as T
import random
from math import ceil
from threading import Thread


class StaffMember(Thread):
    def __init__(self, votes: T.List[int]) -> None:
        super().__init__()
        self.votes = votes
        self.total = {}

    def run(self) -> None:
        for vote in self.votes:
            if self.total.get(vote):
                self.total[vote] += 1
            else:
                self.total[vote] = 1


def process_votes(votes: T.List[int]) -> None:
    jobs = []
    vote_count = len(votes)
    member_count = 3
    vote_per_pile = ceil(vote_count / member_count)

    for i in range(member_count):
        pile = blanks[i * vote_per_pile:i * vote_per_pile + vote_per_pile]
        p = StaffMember(pile)
        jobs.append(p)
    
    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    total = {}
    for j in jobs:
        # loop for dictionaries
        for key in j.total:
            # summation of each key
            if total.get(key):
                total[key] += j.total[key]
            else:
                total[key] = j.total[key]
    print(total)


if __name__ == "__main__":
    # generating a huge list of votes
    blanks = [random.randint(1, 10) for _ in range(100000)]
    process_votes(blanks)
