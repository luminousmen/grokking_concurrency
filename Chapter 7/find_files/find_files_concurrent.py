#!/usr/bin/env python3.9

""" Search for a specific word in multiple files within a specified
directory using data decomposition technique(Loop-level parallelism)"""

import os
import time
import glob
import typing as T
from multiprocessing.pool import ThreadPool


def search_file(file_location: str, search_string: str) -> bool:
    """Searches for a specified word in a file and returns True if the
    word is found."""
    with open(file_location, "r", encoding="utf8") as file:
        return search_string in file.read()


def search_files_concurrently(file_locations: T.List[str],
                              search_string: str) -> None:
    """Searches for a specified word in multiple files concurrently using
    multiple threads."""
    with ThreadPool() as pool:
        # search for the same search_string in each thread concurrently
        results = pool.starmap(search_file,
                               ((file_location, search_string) for
                                file_location in file_locations))
        for result, file_name in zip(results, file_locations):
            if result:
                print(f"Found string in file: `{file_name}`")


if __name__ == "__main__":
    file_locations = list(
        glob.glob(f"{os.path.abspath(os.getcwd())}/books/*.txt"))
    # get input from user
    search_string = input("What word are you trying to find?: ")

    start_time = time.perf_counter()
    search_files_concurrently(file_locations, search_string)
    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")
