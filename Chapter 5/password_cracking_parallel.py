#!/usr/bin/env python3

"""Program for cracking the password consisting with only numbers
using brute force approach concurrently"""

import os
import math
import time
import typing as T
import hashlib
from multiprocessing import cpu_count, Manager
# WARNING: Python have problems with running CPU-bound operations using threads so it will
# not be as efficient as in other languages
from multiprocessing.pool import ThreadPool


def get_combinations(*, length: int, min_number: int = 0, max_number: int = None) -> T.List[str]:
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
    """Calculating cryptographic hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(expected_crypto_hash: str, password: str) -> bool:
    # calculating cryptographic hash of the password
    crypto_hash = get_crypto_hash(password)
    # compare the resulted cryptographic hash with the one stored on the system
    if expected_crypto_hash.upper() == crypto_hash.upper():
        return True
    return False


def crack_password(crypto_hash: str, length: int, min_number: int, max_number: int, event) -> None:
    """Brute force the password combinations"""
    combinations = get_combinations(length=length, min_number=min_number, max_number=max_number)
    print(f"Processing {len(combinations)} combinations from {min_number} to {max_number} in process {os.getpid()}")
    for combination in combinations:
        # checking if the password has been found already in any of the processes
        if not event.is_set():
            if check_password(crypto_hash, combination):
                print(f"PASSWORD CRACKED: {combination}")
                event.set()
        else:
            break


def get_chunks(num_cores: int, length: int) -> T.List[T.Tuple[int, int]]:
    """Splitting the passwords into chunks using break points"""
    max_number = int(math.pow(10, length))
    chunks = []
    # creating a range of numbers for each process     
    for i in range(num_cores):  
        chunks.append((math.ceil(max_number/num_cores * i), math.ceil(max_number/num_cores * (i + 1)) - 1))
    return chunks


def crack_password_parallel(crypto_hash: str, length: int) -> None:
    """Orchestrate cracking the password between different processes"""
    # getting number of available processors
    num_cores = cpu_count()
    # creating a pool of threads
    pool = ThreadPool(num_cores)  # for using processes - mp.Pool(num_cores)
    m = Manager()
    event = m.Event()

    # creates start and stopping points based on the number of cores
    chunks = get_chunks(num_cores, length)

    print(f"Processing number combinations concurrently")
    start_time = time.perf_counter()

    # processing each chunk in a separate process concurrently
    pool.starmap(crack_password, [(crypto_hash, length, start, stop, event) for start, stop in chunks])
    pool.close()

    # waiting for the event to be set - to find a password
    event.wait()
    # terminate all the processes in the pool once the password found
    pool.terminate()

    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")


if __name__ == "__main__":
    crypto_hash = "e24df920078c3dd4e7e8d2442f00e5c9ab2a231bb3918d65cc50906e49ecaef4"
    max_length = 8
    crack_password_parallel(crypto_hash, max_length)

