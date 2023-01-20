#!/usr/bin/env python3

import re
import os
import glob
import typing as T


def wordcount(filenames: T.List[str]) -> T.Dict[str, int]:
    d = {}
    for filename in filenames:
        print(f"Calculating {filename}")
        with open(filename, "r") as f:
            for line in f:
                words = re.split("\W+", line)
                for word in words:
                    word = word.lower()
                    if word != "":
                        d[word] = 1 + d.get(word, 0)
    return d


if __name__ == "__main__":
    data = list(
        glob.glob(f"{os.path.abspath(os.getcwd())}/input_files/*.txt"))
    result = wordcount(data)
    print(result)
