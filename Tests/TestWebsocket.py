import pytest
import uuid
import datetime
import re
from AA_Gen.Sensor import Data


class TestSensor:

    def test_positive_class_format(self):
        d = Data()
        assert isinstance(d.temp, int)
        assert re.search("([0-z]{8})-([0-z]{4})-([0-z]{4})-([0-z]{4})-([0-z]{12})", d.id)
        assert d.temp >= 80 or d.temp <= 100
        assert d.type == "Sensor"
        assert isinstance(uuid.UUID(d.id), uuid.UUID)
        assert isinstance(datetime.datetime.fromisoformat(d.time), datetime.datetime)
        assert isinstance(d.object, dict)

    def test_negative_id(self):
        d = Data()
        d.id = 1
        with pytest.raises(AttributeError):
            assert isinstance(uuid.UUID(d.id), uuid.UUID)

    def test_get_object(self):
        d = Data()
        assert isinstance(d.get_object(), str)





