import pytest
from AA_Gen.Sensor import Data
from BB_Reader.Piper import Worker


class TestWorker:
    @pytest.mark.parametrize('fahrenheit, celsius',
                             [(32, 0), (0, -17.778), (212, 100), (100, 37.778), (80, 26.667) ])
    def test_change_temp(self, fahrenheit, celsius):
        d = Data()
        w = Worker(d.get_object())
        assert w.fahrenheit_to_celsius(fahrenheit) == celsius

    def test_worker_format(self):
        d = Data()
        w = Worker(d.get_object())
        assert isinstance(w.data, dict)

    def test_add_t_content(self):
        d = Data()
        w = Worker(d.get_object())
        assert isinstance(w.data.get('content'), dict)

    def test_add_t_len(self):
        d = Data()
        w = Worker(d.get_object())
        w.add_t()
        assert len(w.data.get('content')) == 3

    def test_add_t_works(self):
        d = Data()
        w = Worker(d.get_object())
        w.add_t()
        assert isinstance(w.data.get('content').get('temperature_c'), float)
