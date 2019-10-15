import json
from datetime import datetime as dt
import uuid
import random


class Data:
    def __init__(self):
        """
        This class handles the data and the format in which it's contained
        """
        self.id = str(uuid.uuid4())
        self.type = "Sensor"
        self.temp = random.randint(80, 100)
        self.time = dt.now().isoformat()
        self.object = {}

    def __make_object(self):
        """
        creates the dictionary object in the expected format.
        :return:
        """
        if self.id:
            self.object['id'] = self.id
        if self.type:
            self.object['type'] = self.type
        self.object['content'] = {}
        if self.temp:
            self.object.get('content')['temperature_f'] = self.temp
        if self.time:
            self.object.get('content')['time_of_measurement'] = self.time

    def get_object(self):
        """
        calls the object creator and outputs it as json
        :return:
        """
        if self.id and self.temp and self.type and self.time:
            self.__make_object()
            return json.dumps(self.object)
            # easier json than pickle (?)
