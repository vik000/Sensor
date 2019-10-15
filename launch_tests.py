from Tests.TestReader import *
from Tests.TestDataBase import *
from Tests.TestWebsocket import *


def main():
    TestWorker()
    TestDb()
    TestSensor()


if __name__ == "__main__":
    main()

