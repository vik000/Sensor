# make sure redis server is on (redis-server)
import redis
import json
from datetime import datetime as dt


class Transform:
    def __init__(self, data):
        self.d = data

    def flatten(self, data):
        r = {}
        for k in data:
            if type(data.get(k)) == dict:
                n = data.get(k)
                for i in n:
                    r[i] = n.get(i)
            else:
                r[k] = data.get(k)
        return r

    def make_key_from_id(self):
        return self.d.get('id')

    def create_time_index(self):
        tf = self.d.get("content").get('time_of_measurement')
        t = dt.fromisoformat(str(tf))
        return t.strftime("%Y%m%d%H%M%S")


class Redis:
    def __init__(self, host):
        self.r = redis.Redis(host)
        # TODO: check connection!
        # TODO: add auth

    def create(self, key, set, index):
        for k in set:
            self.r.hset(key, k, set.get(k))
        self.r.zadd("sensor", {key: index}, nx=True)

    def search_by_time(self, start, end):
        return self.r.zrange('sensor', start, end)

    def update(self):
        # TODO: update db
        pass

    def delete(self):
        # TODO: delete db entry
        pass
