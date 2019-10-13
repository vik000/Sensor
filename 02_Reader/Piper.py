import queue
import json
import threading
from DataBase import Transform, Redis


class Pipeline:
    # manages queue:
    def __init__(self):
        self.q = queue.Queue()

    def __add_to_queue(self, worker):
        self.q.put(worker) # so far we reach HERE

    def add_worker(self, job):
        w = Worker(job)
        self.__add_to_queue(w)


class Worker:
    # transforms data
    def __init__(self, data):
        self.data = json.loads(data)

    @staticmethod
    def __fahrenheit_to_celsius(f):
        c = (f - 32) * 5/9
        return c

    def add_t(self):
        f = self.data.get('content').get('temperature_f')
        self.data.get('content')['temperature_c'] = self.__fahrenheit_to_celsius(f)

    def parse_data(self):
        return json.dumps(self.data)
