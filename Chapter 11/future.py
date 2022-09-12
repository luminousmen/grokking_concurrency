"""The best known way to see the future is to wait"""


class Future:
    def __init__(self, loop):
        self.loop = loop
        self.done = False
        self.result = None
        self.co = None

    def set_coroutine(self, co):
        self.co = co

    def set_result(self, result):
        self.done = True
        self.result = result

        if self.co:
            self.loop.add_coroutine(self.co)

    def __await__(self):
        if not self.done:
            yield self
        return self.result
