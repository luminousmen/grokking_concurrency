#!/usr/bin/env python3

"""Search text files that contain a specific search term using data decomposition technique(Loop-level parallelism)"""
import itertools
import os
import time
import concurrent.futures
import typing as T


def search_file(file_name: str, search_string: str) -> bool:
    file = open(file_name, "r")
    if search_string in file.read():
        file.close()
        return True
    file.close()
    return False


def search_files_concurrently(files: T.List[str], search_string: str) -> None:
    executor = concurrent.futures.ThreadPoolExecutor()
    # assuming flat folder structure
    file_locations = [user_input + os.sep + file_name for file_name in files]
    # starting threads concurrently
    threads = executor.map(search_file, file_locations, itertools.repeat(search_string))
    for result, file_name in zip(threads, files):
        if result:
            print(f"Found string in file: `{file_name}`")


if __name__ == "__main__":
    user_input = input("What is the name of your directory: ")
    # removing hidden files just in case
    files = [f for f in os.listdir(user_input) if not f.startswith('.')]
    search_string = input("What word are you trying to find?: ")

    start_time = time.perf_counter()
    search_files_concurrently(files, search_string)
    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")
