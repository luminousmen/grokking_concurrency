#!/usr/bin/env python3.9

"""Program for cracking the password consisting with only numbers using brute
force approach sequentially"""

import time
import math
import hashlib
import typing as T


def get_combinations(*, length: int, min_number: int = 0,
                     max_number: T.Optional[int] = None) -> T.List[str]:
    """Generate all possible password combinations"""
    combinations = []
    if not max_number:
        # calculating maximum number based on the length
        max_number = int(math.pow(10, length) - 1)

    # go through all possible combinations in a given range
    for i in range(min_number, max_number + 1):
        str_num = str(i)
        # fill in the missing numbers with zeros
        zeros = "0" * (length - len(str_num))
        combinations.append("".join((zeros, str_num)))
    return combinations


def get_crypto_hash(password: str) -> str:
    """"Calculating cryptographic hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(expected_crypto_hash: str,
                   possible_password: str) -> bool:
    actual_crypto_hash = get_crypto_hash(possible_password)
    # compare the resulted cryptographic hash with the one stored in the system
    return expected_crypto_hash == actual_crypto_hash


def crack_password(crypto_hash: str, length: int) -> None:
    """Brute force the password combinations"""
    print("Processing number combinations sequentially")
    start_time = time.perf_counter()
    combinations = get_combinations(length=length)
    for combination in combinations:
        if check_password(crypto_hash, combination):
            print(f"PASSWORD CRACKED: {combination}")
            break

    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")


if __name__ == "__main__":
    crypto_hash = \
        "e24df920078c3dd4e7e8d2442f00e5c9ab2a231bb3918d65cc50906e49ecaef4"
    length = 8
    crack_password(crypto_hash, length)
