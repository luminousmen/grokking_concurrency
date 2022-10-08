#!/usr/bin/env python3
"""Multiply two matrices concurrently, fine granularity"""

import random
import typing as T
from multiprocessing import cpu_count, sharedctypes, Process

ROWS = 4
COLS = 2


def matrix_multiply(A: T.List[T.List[int]], B: T.List[T.List[int]]):
    num_rows_A = len(A)
    num_cols_A = len(A[0])
    num_rows_B = len(B)
    num_cols_B = len(B[0])
    if num_cols_A != num_rows_B:
        raise ArithmeticError(
            "Invalid dimensions; Cannot multiply {}x{}*{}x{}".format(
                num_rows_A, num_cols_A, num_rows_B, num_cols_B
            )
        )

    num_workers = cpu_count()
    chunk_size = num_rows_A // num_workers
    # shared data
    shared_C = sharedctypes.Array("d", num_rows_A * num_cols_B)
    workers = []
    for w in range(num_workers):
        row_start_idx = min(w * chunk_size, num_rows_A)
        row_end_idx = min((w + 1) * chunk_size, num_rows_A)
        workers.append(
            Process(
                target=worker, args=(A, B, shared_C, row_start_idx, row_end_idx)
            )
        )
    for w in workers:
        w.start()
    for w in workers:
        w.join()

    C = [[0] * num_cols_B for i in range(num_rows_A)]
    for i in range(num_rows_A):
        for j in range(num_cols_B):
            C[i][j] = shared_C[i * num_cols_B + j]
    return C


def worker(A, B, shared_C, row_start_idx, row_end_idx):
    # subset of rows in A
    for i in range(row_start_idx, row_end_idx):
        for j in range(len(B[0])):
            for k in range(len(A[0])):
                shared_C[i * len(B[0]) + j] += A[i][k] * B[k][j]


if __name__ == "__main__":
    A = [[random.randint(0, 10) for i in range(COLS)] for j in range(ROWS)]
    B = [[random.randint(0, 10) for i in range(ROWS)] for j in range(COLS)]
    parallel_result = matrix_multiply(A, B)
