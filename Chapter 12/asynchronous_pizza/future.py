"""The best known way to see the future is to wait"""

import typing as T


class Future:
    def __init__(self, loop) -> None:
        self.loop = loop
        self.done = False
        self.co = None
        self.result = None

    def set_coroutine(self, co: T.Coroutine[T.Any, T.Any, T.Any]) -> None:
        self.co = co

    def set_result(self, result: T.Any) -> None:
        self.done = True
        self.result = result

        if self.co:
            self.loop.add_coroutine(self.co)

    # This 'Magic Method' is what makes Future a future
    def __await__(self) -> T.Generator[T.Any, None, T.Any]:
        if not self.done:
            yield self
        return self.result
