import time


class Stopwatch:
    """Stopwatch to measure elapsed time"""
    start_time: time

    def start(self):
        self.start_time = time.perf_counter()
        return self

    @property
    def elapsed_time(self) -> time:
        try:
            return time.perf_counter() - self.start_time
        except AttributeError:
            self.start_time = time.perf_counter()
            return 0
