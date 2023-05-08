#!/usr/bin/env python3.9
"""Bank account without synchronization cause race condition """

import sys
import time
from threading import Thread
import typing as T

from bank_account import BankAccount
from synced_bank_account import SyncedBankAccount
from unsynced_bank_account import UnsyncedBankAccount

THREAD_DELAY = 1e-16


class ATM(Thread):
    """Automated teller machine (ATM) or cash machine"""

    def __init__(self, bank_account: BankAccount):
        super().__init__()
        self.bank_account = bank_account

    def transaction(self) -> None:
        self.bank_account.deposit(10)
        # simulating some real action here
        time.sleep(0.001)
        self.bank_account.withdraw(10)

    def run(self) -> None:
        self.transaction()


def test_atms(account: BankAccount, atm_number: int = 1000) -> None:
    atms: T.List[ATM] = []
    # create `atm_number` threads that will deposit and withdraw money
    # from account concurrently
    for _ in range(atm_number):
        atm = ATM(account)
        atms.append(atm)
        atm.start()

    # waiting for atm threads to finish the execution
    for atm in atms:
        atm.join()


if __name__ == "__main__":
    atm_number = 1000
    # greatly improve the chance of an operation being interrupted
    # by thread switch, thus testing synchronization effectively.
    sys.setswitchinterval(THREAD_DELAY)

    # test unsynced bank account
    account = UnsyncedBankAccount()
    test_atms(account, atm_number=atm_number)

    print("Balance of unsynced account after concurrent transactions:")
    print(f"Actual: {account.balance}\nExpected: 0")

    # test synced bank account
    account = SyncedBankAccount()
    test_atms(account, atm_number=atm_number)

    print("Balance of synced account after concurrent transactions:")
    print(f"Actual: {account.balance}\nExpected: 0")
