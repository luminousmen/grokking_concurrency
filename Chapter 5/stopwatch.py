import time


class Stopwatch(object):
    def start(self):
        self.start_time = time.time()
        return self

    @property
    def elapsed_time(self):
        try:
            return time.time() - self.start_time
        except AttributeError:  # Wasn't explicitly started.
            self.start_time = time.time()
            return 0
