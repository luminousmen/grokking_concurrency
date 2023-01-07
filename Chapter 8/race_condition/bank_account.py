""" Abstract bank account. """
from abc import ABC, abstractmethod


class BankAccount(ABC):
    """ Abstract Base Class for bank accounts"""

    balance: float

    def __init__(self, balance: float = 0):
        self.balance: float = balance

    @abstractmethod
    def deposit(self, amount: float) -> None:
        ...

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        ...
