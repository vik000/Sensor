import pytest
from AA_Gen.Sensor import Data
from BB_Reader.DataBase import *
import json
import re


class TestDb:

    def test_init(self):
        d = Data()
        assert isinstance(d.object, dict)

    def test_flatten(self):
        d = Data()
        t = Transform(d.object)
        f = t.flatten(t.d)
        for k, v in f.items():
            with pytest.raises(AssertionError):
                assert isinstance(v, dict)

    def test_flatten_content(self):
        d = Data()
        t = Transform(json.loads(d.get_object()))
        f = t.flatten(t.d)
        with pytest.raises(KeyError):
            f['content']

    def test_time_index(self):
        d = Data()
        print(d)
        t = Transform(json.loads(d.get_object()))
        assert isinstance(t.d.get('content'), dict)
        assert isinstance(t.create_time_index(), str)

    def test_time_index_length(self):
        this_year = dt.now().year
        this_month = dt.now().month
        this_date = dt.now().day
        d = Data()
        t = Transform(json.loads(d.get_object()))
        r = t.create_time_index()
        assert r[:4] == str(this_year)
        assert r[4:6] == str(this_month)
        assert r[6:8] == str(this_date)

    def test_time_index_format(self):
        d = Data()
        t = Transform(json.loads(d.get_object()))
        assert re.search("([0-9]{14})", t.create_time_index())

