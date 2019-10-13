import queue
import json
import threading
from DataBase import Transform, Redis


class Pipeline:
    # manages queue:
    def __init__(self):
        self.q = queue.Queue()

    def read_queue(self):
        while self.q is not self.q.empty():
            print(self.q.get())

    def start_reader(self):
        reader = threading.Thread(target=self.read_queue)
        reader.start()

    def __add_to_queue(self, worker):
        self.q.put(worker)

    def add_worker(self, job):
        w = Worker(job)
        t = threading.Thread(target=self.__add_to_queue, args=(w,))
        t.start()
        # make sure you also lock before you continue.
        t.join()




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
