#!/usr/bin/env python3

from protocol import Protocol, HOST, PORT

import os
from uuid import uuid4
import asyncio
import json
import re


class Worker(Protocol):
    def connection_lost(self, exc):
        print("The server closed the connection")
        print("Stop the event loop")
        asyncio.get_running_loop().stop()

    def process_command(self, command, data=None):
        commands = {
            b"map": self.call_mapfn,
            b"reduce": self.call_reducefn,
            b"disconnect": self.connection_lost,
        }
        if command in commands:
            commands[command](data)
        else:
            print(f"Unknown command received: {command}")

    def mapfn(self, filename):
        print(f"Running map for {filename}")
        with open(filename, "r", encoding="ISO-8859-1") as f:
            for line in f:
                words = re.split("\W+", line)
                for word in words:
                    word = word.lower()
                    if word != '':
                        yield word, 1

    def combinefn(self, results):
        for key in results.keys():
            results[key] = sum(results[key])
        return results

    def reducefn(self, map_files):
        reduced_result = {}
        for filename in map_files.values():
            with open(filename, "r") as f:
                print(f"Running reduce for {filename}")
                d = json.load(f)
                for k, v in d.items():
                    reduced_result[k] = v + reduced_result.get(k, 0)
        return reduced_result

    def call_mapfn(self, data):
        print(f"Mapping {data}")
        results = {}
        for k, v in self.mapfn(data[1]):
            if k not in results:
                results[k] = []
            results[k].append(v)

        results = self.combinefn(results)
        temp_file = self.save_map_results(results)
        self.send_command(command=b"mapdone", data=(data[0], temp_file))

    def save_map_results(self, results):
        temp_dir = self.get_temp_dir()
        temp_file = os.path.join(temp_dir, f"{uuid4()}.json")
        print(f"Saving to {temp_file}")
        with open(temp_file, "w") as f:
            d = json.dumps(results)
            f.write(d)
        print(f"Saved to {temp_file}")
        return temp_file

    def call_reducefn(self, data):
        print(f"Reducing {data[0]}")
        results = self.reducefn(data)
        with open(self.get_result_filename(), "w") as f:
            d = json.dumps(results)
            f.write(d)
        self.send_command(command=b"reducedone",
                          data=(data[0], self.get_result_filename()))


def main():
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(Worker, HOST, PORT)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
