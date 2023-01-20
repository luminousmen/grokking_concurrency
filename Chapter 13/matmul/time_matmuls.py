""" Comparing Sequential vs Concurrent timings
        Concurrent only starts to win when matrix sizes >= 128.
size  seq       conc       conc/seq
 {2: (7.3e-06, 0.213735, 29278.76712328767),
 4: (2.21e-05, 0.2522912, 11415.891402714933),
 8: (0.0001411, 0.3912973, 2773.191353649894),
 16: (0.0011981, 0.4087865, 341.1956431015775),
 32: (0.0099682, 0.4038004, 40.50885816897735),
 64: (0.0813502, 0.4490451, 5.519901610567644),
 128: (0.6468402, 0.6297645, 0.9736013624385126),
 256: (5.7198182, 2.1857718, 0.3821400827040272)}
"""
from matmul_sequential import matrix_multiply as sequential_mm
from matmul_concurrent import matrix_multiply as concurrent_mm
from random import randint
from time import perf_counter_ns
from typing import List, Dict, Tuple
from pprint import pprint

Matrix = List[List[int]]


class TimimgRun:
    timings: Dict[int, Tuple[float, float, float]] = dict()

    def _time_sequential_run(self):
        print('\tStarting sequential run')
        start_sequential: float = perf_counter_ns()
        sequential_mm(self.matrixA, self.matrixB)
        end_sequential: float = perf_counter_ns()
        return (end_sequential - start_sequential) / 1_000_000_000

    def _time_concurrent_run(self):
        print('\tStarting concurrent run')
        start_concurrent: float = perf_counter_ns()
        concurrent_mm(self.matrixA, self.matrixB)
        end_concurrent: float = perf_counter_ns()
        return (end_concurrent - start_concurrent) / 1_000_000_000

    def make_comparison(self, size: int):
        self.matrixA: Matrix = [[randint(0, 10) for _ in range(1, size)]
                                for _ in range(1, size)]
        self.matrixB: Matrix = [[randint(0, 10) for _ in range(1, size)]
                                for _ in range(1, size)]

        sequential_time = self._time_sequential_run()
        concurrent_time = self._time_concurrent_run()

        comparison = concurrent_time / sequential_time
        self.timings[size] = (sequential_time, concurrent_time, comparison)

    @classmethod
    def print_timimgs(cls):
        pprint(cls.timings)


if __name__ == '__main__':
    timer = TimimgRun()
    RANGE = 9
    sizes: List[int] = [2 ** i for i in range(1, RANGE)]
    for size in sizes:
        print(f'Running with size {size}')
        timer.make_comparison(size)
    timer.print_timimgs()
