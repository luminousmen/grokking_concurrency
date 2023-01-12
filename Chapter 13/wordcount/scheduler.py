import asyncio
from enum import Enum


class State(Enum):
    START = 0
    MAPPING = 1
    REDUCING = 2
    FINISHED = 3


class Scheduler:
    def __init__(self, datasource):
        self.state = State.START
        self.data_len = len(datasource)
        self.datasource = iter(dict(enumerate(datasource)).items())

    def next_task(self):
        if self.state == State.START:
            print("STARTED")
            self.working_maps = {}
            self.map_results = {}
            self.state = State.MAPPING

        if self.state == State.MAPPING:
            try:
                map_item = next(self.datasource)
                self.working_maps[map_item[0]] = map_item[1]
                return b"map", map_item
            except StopIteration:
                if len(self.working_maps) > 0:
                    return b"disconnect", None
                self.state = State.REDUCING

        if self.state == State.REDUCING:
            self.reduce_iter = iter(self.map_results.items())
            self.working_reduces = {}
            self.results = {}
            return b"reduce", self.map_results

        if self.state == State.FINISHED:
            print("FINISHED.")
            asyncio.get_running_loop().stop()
            return b"disconnect", None

    def map_done(self, data):
        if not data[0] in self.working_maps:
            return
        self.map_results[data[0]] = data[1]
        del self.working_maps[data[0]]
        print(f"MAPPING {len(self.map_results)}/{self.data_len}")

    def reduce_done(self, data):
        print("REDUCING 1/1")
        self.state = State.FINISHED
        self.results[data[0]] = data[1]
