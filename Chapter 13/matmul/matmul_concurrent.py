#!/usr/bin/env python3.9
""" Multiply two matrices concurrently """

from typing import List
import random
from multiprocessing import Pool

Row = List[int]
Column = List[int]
Matrix = List[Row]


def matrix_multiply(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
    """ Multiply two matrices, calculating each row of the solution
    concurrently. """
    num_rows_a = len(matrix_a)
    num_cols_a = len(matrix_a[0])
    num_rows_b = len(matrix_b)
    num_cols_b = len(matrix_b[0])
    if num_cols_a != num_rows_b:
        raise ArithmeticError(
            f"Invalid dimensions; Cannot multiply "
            f"{num_rows_a}x{num_cols_a}*{num_rows_b}x{num_cols_b}"
        )

    pool = Pool()
    results = pool.map(
        process_column,
        [(matrix_a, matrix_b, i) for i in range(num_rows_a)])
    pool.close()
    pool.join()
    return results


def process_column(args: tuple) -> Column:
    """ Creates 1 column of the solution_matrix """
    matrix_a, matrix_b, row_idx = args
    num_cols_a = len(matrix_a[0])
    num_cols_b = len(matrix_b[0])

    result_col = [0] * num_cols_b
    for j in range(num_cols_b):  # for each col in matrix_b
        for k in range(num_cols_a):  # for each col in matrix a
            result_col[j] += matrix_a[row_idx][k] * matrix_b[k][j]
    return result_col


if __name__ == "__main__":
    cols = 4
    rows = 2
    A = [[random.randint(0, 10) for i in range(cols)]
         for j in range(rows)]
    print(f"matrix A: {A}")
    B = [[random.randint(0, 10) for i in range(rows)]
         for j in range(cols)]
    print(f"matrix B: {B}")
    C = matrix_multiply(A, B)
    print(f"matrix C: {C}")
