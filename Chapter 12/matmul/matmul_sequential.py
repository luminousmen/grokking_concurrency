#!/usr/bin/env python3
"""Multiply two matrices sequentially"""

import random
import typing as T
from pprint import pprint

ROWS = 4
COLS = 2


def matrix_multiply(A: T.List[T.List[int]], B: T.List[T.List[int]]):
    num_rows_A = len(A)
    num_cols_A = len(A[0])
    num_rows_B = len(B)
    num_cols_B = len(B[0])
    if num_cols_A != num_rows_B:
        raise ArithmeticError(
            f"Invalid dimensions; Cannot multiply "
            f"{num_rows_A}x{num_cols_A}*{num_rows_B}x{num_cols_B}"
        )
    C = [[0] * num_cols_B for i in range(num_rows_A)]
    for i in range(num_rows_A):
        for j in range(num_cols_B):
            for k in range(num_cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C


if __name__ == "__main__":
    A = [[random.randint(0, 10) for i in range(COLS)] for j in range(ROWS)]
    B = [[random.randint(0, 10) for i in range(ROWS)] for j in range(COLS)]
    C = matrix_multiply(A, B)
    pprint(C)
