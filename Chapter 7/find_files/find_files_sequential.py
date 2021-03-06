#!/usr/bin/env python3

"""Sequential search text files that contain a specific search term"""

import os
import time
import typing as T


def search_file(file_name: str, search_string: str) -> bool:
    file = open(file_name, "r", encoding="utf8")

    if search_string in file.read():
        file.close()
        return True
    file.close()
    return False


def search_files_sequentially(files: T.List[str], search_string: str) -> None:
    for file_name in files:
        # assuming flat folder structure
        result = search_file(user_input + os.sep + file_name, search_string)
        if result:
            print(f"Found string in file: `{file_name}`")


if __name__ == "__main__":
    user_input = input("What is the name of your directory: ")
    # removing hidden files just in case
    files = [f for f in os.listdir(user_input) if not f.startswith(".")]
    search_string = input("What word are you trying to find?: ")

    start_time = time.perf_counter()
    search_files_sequentially(files, search_string)
    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")
