#!/usr/bin/env python3.9

import re
import os
import glob
import typing as T

Occurrences = T.Dict[str, int]

ENCODING = "ISO-8859-1"


def wordcount(filenames: T.List[str]) -> Occurrences:
    """Calculates the word count of given files."""
    word_counts = {}
    for filename in filenames:
        print(f"Calculating {filename}")
        with open(filename, "r", encoding=ENCODING) as file:
            for line in file:
                # Split line into words using regex
                words = re.split("\W+", line)
                for word in words:
                    word = word.lower()
                    # Count the word if it is not empty
                    if word != "":
                        word_counts[word] = 1 + word_counts.get(word, 0)
    return word_counts


if __name__ == "__main__":
    data = list(
        glob.glob(f"{os.path.abspath(os.getcwd())}/input_files/*.txt"))
    result = wordcount(data)
    print(result)
