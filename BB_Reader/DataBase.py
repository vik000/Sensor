# make sure redis server is on (redis-server)
import redis
from datetime import datetime as dt
import logging


class Transform:
    """
    This class prepares the data for the DB format.
    It could be made more abstract to accept other databases (potentially)
    """
    def __init__(self, data):
        self.d = data

    @staticmethod
    def flatten(data):
        """
        Eliminates te content sublevel of the dictionary for ease of use.
        :param data:
        :return:
        """
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
        """
        creates a primary key for the DB
        :return:
        """
        return self.d.get('id')

    def create_time_index(self):
        """
        creates a numeric reference to make it easy to search in Redis
        :return:
        """
        tf = self.d.get("content").get('time_of_measurement')
        t = dt.fromisoformat(str(tf))
        return t.strftime("%Y%m%d%H%M%S")


class Redis:
    """
    This class handles CRUD for Redis
    """
    def __init__(self, host):
        self.r = redis.Redis(host)
        # TODO: check connection!
        # TODO: add auth

    def create(self, key, hash, index):
        """
        Input: key (primary), object (for hash) and index (for score)
        Stores in Redis as hash
        Stores a key - hash relation with a score as an index to find by date instead of primary key
        :param key:
        :param hash:
        :param index:
        :return:
        """
        success = True
        for k in hash:
            if self.r.hset(key, k, hash.get(k)) == 1:
                logging.info(f"{k} stored")
            else:
                logging.error("data not stored")
                success = False
        if self.r.zadd("sensor", {key: index}, nx=True) == 1:
            logging.info("index stored")
        else:
            logging("index not stored")
            success = False
        if success:
            return 1

    def search_by_time(self, start, end):
        """
        This function has not been tested.
        searches hash key in Redis via score in the created index.
        :param start:
        :param end:
        :return:
        """
        return self.r.zrange('sensor', start, end)

    def update(self):
        # TODO: update db
        pass

    def delete(self):
        # TODO: delete db entry
        pass
