#!/usr/bin/env python3

#
"""Simple task parallelism example"""
import time
import typing as T
import random
import concurrent.futures


def maximum(data: T.List[int]) -> int:
    max_val = data[0]
    for i in data[1:]:
        if i > max_val:
            max_val = i
    return max_val


def avg(data: T.List[int]) -> float:
    sum_val = 0
    count_val = 0
    for i in data:
        sum_val += i
        count_val += 1
    return sum_val / count_val


def process(data: T.List[int]) -> T.Tuple[int, float]:
    max_val = maximum(data)
    avg_val = avg(data)
    return max_val, avg_val


def process_concurrently(data: T.List[int]) -> T.Tuple[int, float]:
    # creating a process pool (Python have problems with running CPU-bound operations using threads)
    executor = concurrent.futures.ProcessPoolExecutor()
    # starting two threads concurrently
    # DANGER: communication overhead is right here
    max_thread = executor.submit(maximum, data)
    avg_thread = executor.submit(avg, data)
    # getting the results from threads
    max_val = max_thread.result()
    avg_val = avg_thread.result()
    return max_val, avg_val


if __name__ == "__main__":
    data = [random.randint(1, 100) for _ in range(10000)]
    print("Processing sequentially...")
    start_time = time.perf_counter()
    max_val, avg_val = process(data)
    print(f"Max: {max_val}, Avg: {avg_val}")

    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")

    start_time = time.perf_counter()
    print("Processing concurrently...")
    max_val, avg_val = process_concurrently(data)
    print(f"Max: {max_val}, Avg: {avg_val}")

    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")
