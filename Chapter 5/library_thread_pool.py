#!/usr/bin/env python3.9

"""Library thread pool implementation"""

import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import current_thread


def cpu_waster(i: int) -> str:
    """Wasting the processor time, professionally"""
    name = current_thread().getName()
    print(f"{name} doing Task {i}")
    time.sleep(3)
    return f"Task {i} completed"


def main() -> None:
    with ThreadPoolExecutor(
        max_workers=os.cpu_count(),
        thread_name_prefix="Pool_Thread"
    ) as pool:
        tasks = []
        for i in range(20):
            tasks.append(pool.submit(cpu_waster, i))

        print("All work requests sent")
        for task in as_completed(tasks):
            print(task.result())
        print("All work completed")


if __name__ == "__main__":
    main()
