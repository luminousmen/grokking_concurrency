#!/usr/bin/env python3
"""Counting votes using Fork/Join pattern"""
import typing
import random
from math import ceil
from threading import Thread


class StaffMember(Thread):
    def __init__(self, blanks: typing.List[int]):
        super().__init__()
        self.blanks = blanks
        self.total = {}

    def run(self):
        for blank in self.blanks:
            if self.total.get(blank):
                self.total[blank] += 1
            else:
                self.total[blank] = 1


def process_blanks(blanks: typing.List[int]) -> None:   
    jobs = []
    vote_count = len(blanks)
    member_count = 3
    vote_per_pile = ceil(vote_count/member_count)
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
    process_blanks(blanks)
