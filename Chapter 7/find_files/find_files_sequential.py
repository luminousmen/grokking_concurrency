#!/usr/bin/env python3

""" Search for a specific word in multiple files within a specified
directory sequentially"""

import os
import time
import typing as T


def search_file(file_name: str, search_string: str) -> bool:
    """Searches for a specified word in a file and returns True if the
    word is found."""
    with open(file_name, "r", encoding="utf8") as file:
        return search_string in file.read()


def search_files_sequentially(file_locations: T.List[str],
                              search_string: str) -> None:
    for file_name in file_locations:
        result = search_file(file_name, search_string)
        if result:
            print(f"Found string in file: `{file_name}`")


if __name__ == "__main__":
    # get input from user
    search_dir = input("Search in which directory?: ")
    # removing hidden files just in case, and ignore subdirs
    file_locations = []
    for f in os.listdir(search_dir):
        # assuming flat folder structure
        if os.path.isfile(os.path.join(search_dir, f)) \
                and not f.startswith("."):
            file_locations.append(os.path.join(search_dir, f))
    search_string = input("What word are you trying to find?: ")

    start_time = time.perf_counter()
    search_files_sequentially(file_locations, search_string)
    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")
