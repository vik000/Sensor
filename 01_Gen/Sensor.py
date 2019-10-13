import json
from datetime import datetime as dt
import uuid
import random


class Data:
    # Creates the sensor data in the expected format.
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.type = "Sensor"
        self.temp = random.randint(80, 100)
        self.time = dt.now().isoformat()
        self.object = {}

    def __make_object(self):
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
        if self.id and self.temp and self.type and self.time:
            self.__make_object()
            return json.dumps(self.object)
            # easier json than pickle (?)
