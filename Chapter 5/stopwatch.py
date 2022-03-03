import time


class Stopwatch:
    """Stopwatch to measure elapsed time"""
    start_time: time

    def start(self):
        self.start_time = time.time()
        return self

    @property
    def elapsed_time(self) -> time:
        try:
            return time.time() - self.start_time
        except AttributeError:
            self.start_time = time.time()
            return 0
