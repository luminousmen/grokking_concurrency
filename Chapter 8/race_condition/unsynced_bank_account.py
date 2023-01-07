#!/usr/bin/env python3
"""Bank account without synchronization cause race condition """

from bank_account import BankAccount


class UnsyncedBankAccount(BankAccount):
    """Bank account without synchronization"""

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("You can't deposit negative amount of money")

    def withdraw(self, amount: float) -> None:
        if 0 < amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Account does not contain sufficient funds")
