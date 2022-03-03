#!/usr/bin/env python3

# find_files_concurrent.py
""""""

import os
import time
import concurrent.futures
import typing as T


def search_file(file_name: str, search_string: str) -> bool:
    file = open(file_name, "r")

    if search_string in file.read():
        return True
    file.close()
    return False


def search_files(files: T.List[str], search_string: str) -> None:
    executor = concurrent.futures.ThreadPoolExecutor()

    # starting threads concurrently
    threads = []
    for file_name in files:
        thread = executor.submit(search_file, user_input + os.sep + file_name, search_string)
        threads.append((thread, file_name))

    for thread, file_name in threads:
        if thread.result():
            print(f"Found string in file {file_name}")


if __name__ == "__main__":
    user_input = input("What is the name of your directory: ")
    files = os.listdir(user_input)
    search_string = input("What word are you trying to find?: ")

    start_time = time.time()
    search_files(files, search_string)
    process_time = time.time() - start_time
    print(f"PROCESS TIME: {process_time}")
