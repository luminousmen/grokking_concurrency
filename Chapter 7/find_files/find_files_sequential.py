#!/usr/bin/env python3

"""Sequential search text files that contain a specific search term"""

import os
import time
from typing import List
from os.path import isfile, join


def search_file(file_name: str, search_string: str) -> bool:
    with open(file_name, "r", encoding="utf8") as file:
        return search_string in file.read()


def search_files_sequentially(files: List[str], search_string: str) -> None:
    for file_name in files:
        result = search_file(join(search_dir, file_name), search_string)
        if result:
            print(f"Found string in file: `{file_name}`")


if __name__ == "__main__":
    search_dir = input("Search in which directory?: ")
    # removing hidden files just in case, and ignore subdirs
    files = [f for f in os.listdir(search_dir)
             if isfile(f) and not f.startswith(".")]
    search_string = input("What word are you trying to find?: ")

    start_time = time.perf_counter()
    search_files_sequentially(files, search_string)
    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")
