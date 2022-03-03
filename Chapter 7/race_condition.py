#!/usr/bin/env python3
"""Bank account without synchronization cause race condition """

import sys
import time
import threading

THREAD_DELAY = 1e-16


class UnsyncedBankAccount:
    def __init__(self):
        self.is_open: bool = False
        self.balance: float = 0

    def get_balance(self) -> float:
        return self.balance

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError

    def withdraw(self, amount: float) -> None:
        if 0 < amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError


def transaction(bank_account: UnsyncedBankAccount) -> None:
    bank_account.deposit(10)
    time.sleep(0.001)
    bank_account.withdraw(10)


def cash_machine(account: UnsyncedBankAccount) -> None:
    threads = []

    # create 1000 threads that will deposit and withdraw money
    # from account concurrently
    for _ in range(1000):
        t = threading.Thread(target=transaction, args=(account,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    # greatly improve the chance of an operation being interrupted
    # by thread switch, thus testing synchronization effectively.
    sys.setswitchinterval(THREAD_DELAY)

    # initialization
    bank_account = UnsyncedBankAccount()
    bank_account.deposit(1000)

    # test unsynced bank account
    for _ in range(10):
        cash_machine(bank_account)

    print("Balance of unsynced account after concurrent transactions:")
    print(f"{bank_account.balance}. Expected: 1000")
