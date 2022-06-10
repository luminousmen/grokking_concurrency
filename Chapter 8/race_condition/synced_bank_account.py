#!/usr/bin/env python3
"""Bank account without synchronization cause race condition """

from threading import Lock


class SyncedBankAccount:
    """Bank account with synchronization strategy, thread-safe"""

    balance: float

    def __init__(self, balance: float = 0):
        self.balance: float = balance
        self.mutex = Lock()

    def deposit(self, amount: float) -> None:
        # acquiring a lock on the shared resource
        self.mutex.acquire()
        try:
            if amount > 0:
                self.balance += amount
            else:
                raise ValueError("You can't deposit negative amount of money")
        finally:
            # releasing a lock on the shared resource
            self.mutex.release()

    def withdraw(self, amount: float) -> None:
        self.mutex.acquire()
        try:
            if 0 < amount <= self.balance:
                self.balance -= amount
            else:
                raise ValueError("Account does not contain sufficient funds")
        finally:
            self.mutex.release()
