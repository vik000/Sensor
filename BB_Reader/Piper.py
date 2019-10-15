import queue
import json
import threading
import logging
try:
    from DataBase import Transform, Redis
except ModuleNotFoundError:
    from BB_Reader.DataBase import Transform, Redis


class Pipeline:
    """
    This class manages the queue, which is started on instance and it's under the attribute self.q
    """
    def __init__(self):
        self.q = queue.Queue()

    def read_queue(self):
        """
        Reads items in the queue by adding a worker to it.
        :return:
        """
        while self.q is not self.q.empty():
            worker = self.q.get()
            worker.store(worker.data)

    def start_reader(self):
        """
        Sets a thread to read from self.q
        :return:
        """
        reader = threading.Thread(target=self.read_queue)
        reader.start()

    def __add_to_queue(self, worker):
        """
        Receives a worker object, adds temperature in celsius and adds it to queue
        :param worker:
        :return:
        """
        worker.add_t()
        self.q.put(worker)

    def add_worker(self, job):
        """
        Receives data (job), instances Worker class and starts thread to add it to queue
        :return:
        """
        w = Worker(job)
        t = threading.Thread(target=self.__add_to_queue, args=(w,))
        t.start()
        t.join()


class Worker:
    """
    this class transforms data and stores it in DB
    """
    def __init__(self, data):
        self.data = json.loads(data)
        logging.info("worker created")

    @staticmethod
    def fahrenheit_to_celsius(f):
        """
        transforms degrees fahrenheit to celsius, requires inputting fahrenheit`
        :param f:
        :return:
        """
        c = (f - 32) * 5/9
        return float('{0:.3f}'.format(c))

    def add_t(self):
        """
        adds temperature to the data object
        :return:
        """
        f = self.data.get('content').get('temperature_f')
        self.data.get('content')['temperature_c'] = self.fahrenheit_to_celsius(f)

    @staticmethod
    def __paperwork(data):
        """
        inputs data, flattens the object and prepares it for db insertion
        returns a tuple with a key[0], the object [1] and a numeric index[2].
        :param data:
        :return:
        """
        t = Transform(data)
        job = t.flatten(data)
        print(job)
        key = t.make_key_from_id()
        index = t.create_time_index()
        return key, job, index

    @staticmethod
    def __send_to_db(paperwork):
        """
        connects to Redis and creates the entry in the DB.
        sends the object to the Redis class.
        :param paperwork:
        :return:
        """
        host = 'localhost'
        r = Redis(host) # the name is obvious, but it's abstract enough to use any other DB if we want to change it.
        if r.create(paperwork[0], paperwork[1], paperwork[2]) == 1:
            return paperwork[1]
        else:
            return 0

    def store(self, data):
        """
        input data and calls paperwork and send_to_db in order to store in the db.
        :param data:
        :return:
        """
        t = self.__paperwork(data)
        r = self.__send_to_db(t)
        if r != 0:
            logging.info('data stored, ' + json.dumps(r))
            logging.info("------------------------------------------------------------------------------------------")

