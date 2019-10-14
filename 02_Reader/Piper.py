import queue
import json
import threading
import logging
from DataBase import Transform, Redis


class Pipeline:
    # manages queue:
    def __init__(self):
        self.q = queue.Queue()

    def read_queue(self):
        while self.q is not self.q.empty():
            worker = self.q.get()
            worker.store(worker.data)

    def start_reader(self):
        reader = threading.Thread(target=self.read_queue)
        reader.start()

    def __add_to_queue(self, worker):
        worker.add_t()
        self.q.put(worker)

    def add_worker(self, job):
        w = Worker(job)
        t = threading.Thread(target=self.__add_to_queue, args=(w,))
        t.start()
        t.join()


class Worker:
    # transforms data
    # stores in DB
    def __init__(self, data):
        self.data = json.loads(data)
        logging.info("worker created")

    @staticmethod
    def __fahrenheit_to_celsius(f):
        c = (f - 32) * 5/9
        return c

    def add_t(self):
        f = self.data.get('content').get('temperature_f')
        self.data.get('content')['temperature_c'] = self.__fahrenheit_to_celsius(f)

    def __paperwork(self, data):
        t = Transform(data)
        job = t.flatten(data)
        print(job)
        key = t.make_key_from_id()
        index = t.create_time_index()
        return key, job, index

    def __send_to_db(self, paperwork):
        host = 'localhost'
        r = Redis(host) # the name is obvious, but it's abstract enough to use any other DB if we want to change it.
        r.create(paperwork[0], paperwork[1], paperwork[2])

    def store(self, data):
        t = self.__paperwork(data)
        self.__send_to_db(t)
        logging.info('data stored, ' + json.dumps(data))
        logging.info("------------------------------------------------------------------------------------------")
