#!/usr/bin/env python3

#
"""Bank account with synchronization; no race condition possible"""

import sys
import time
import threading

THREAD_DELAY = 1e-16


class SyncedBankAccount:
    """Bank account with synchronization strategy, thread-safe."""

    def __init__(self):
        self.is_open: bool = False
        self.balance: float = 0
        self.mutex = threading.Lock()

    def get_balance(self) -> float:
        return self.balance

    def deposit(self, amount: float) -> None:
        self.mutex.acquire()
        try:
            if amount > 0:
                self.balance += amount
            else:
                raise ValueError
        finally:
            self.mutex.release()

    def withdraw(self, amount: float) -> None:
        self.mutex.acquire()
        try:
            if 0 < amount <= self.balance:
                self.balance -= amount
            else:
                raise ValueError
        finally:
            self.mutex.release()


def transaction(bank_account: SyncedBankAccount) -> None:
    bank_account.deposit(10)
    time.sleep(0.001)
    bank_account.withdraw(10)


def cash_machine(account: SyncedBankAccount) -> None:

    threads = []
    for _ in range(1000):
        t = threading.Thread(target=transaction, args=(account, ))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    # greatly improve the chance of an operation being interrupted
    # by thread switch, thus testing synchronization effectively.
    sys.setswitchinterval(THREAD_DELAY)

    # initialization
    bank_account = SyncedBankAccount()
    bank_account.deposit(1000)

    # test synced bank account
    for _ in range(10):
        cash_machine(bank_account)

    print("Balance of synced account after concurrent transactions:")
    print(f"{bank_account.balance}. Expected: 1000")
