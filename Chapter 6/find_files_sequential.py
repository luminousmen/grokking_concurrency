#!/usr/bin/env python3
import os
import time
import typing


def search_file(file_name: str, search_string: str) -> bool:
    file = open(file_name, "r", encoding="utf8")

    if search_string in file.read():
        return True
    file.close()
    return False


def search_files(files: typing.List[str], search_string: str) -> None:
    for file_name in files:
        print(file_name)
        result = search_file(user_input + os.sep + file_name, search_string)
        if result:
            print("found string in file %s" % file_name)


if __name__ == "__main__":
    user_input = input("What is the name of your directory: ")
    files = os.listdir(user_input)
    search_string = input("What word are you trying to find?: ")

    start_time = time.time()
    search_files(files, search_string)
    process_time = time.time() - start_time
    print(f"PROCESS TIME: {process_time}")
