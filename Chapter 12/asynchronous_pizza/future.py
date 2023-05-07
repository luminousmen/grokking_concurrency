"""The best known way to see the future is to wait"""

import typing as T


class Future:
    def __init__(self) -> None:
        self.coroutine = None

    def set_coroutine(self, coroutine: T.Callable):
        self.coroutine = coroutine
