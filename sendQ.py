import threading
from collections import namedtuple
import queue
from time import sleep
from random import randint

import datetime

default_max_time = 5
debug = False

class SendQ(threading.Thread):
    """
    a singleton to send mail in a random time interval
        max_time: the max time interval
        flag: flag for run/stop
    """
    __instance = None

    def __new__(cls, target=None, max_time=default_max_time):
        if SendQ.__instance:
            if debug:
                print('using old sendQ')
            if target:
                SendQ.__instance.q.put(target)
            SendQ.__instance.max_time = max_time
            return SendQ.__instance
        if debug:
            print('using a new sendQ')
        return object.__new__(cls)

    def __init__(self, target=None, max_time=default_max_time):
        if not SendQ.__instance:
            super(SendQ, self).__init__()
            self.q = queue.Queue()
            if target:
                self.q.put(target)
            self.max_time = max_time
            self.flag = True
            self.start()
            SendQ.__instance = self

    def __del__(self):
        self.flag = False
        while not self.q.empty():
            pass

    @staticmethod
    def send(*args):
        """
        need to implement
        """
        pass

    def run(self):
        while not self.q.empty() or self.flag:
            target = self.q.get()
            SendQ.send(target)
            if self.flag:
                sleep_time =randint(0, self.max_time)
                if debug:
                    print('waiting in 0 ~ {}, sleep {}'.format(self.max_time, sleep_time))
                sleep(sleep_time)

    def stop(self):
        if debug:
            print('exiting... {} remind'.format(self.q.qsize()))
        self.flag = False


if __name__ == '__main__':
    debug = True
    target = namedtuple('Target', ['to'])

    def override_function(target):
        print("send to {} at {}".format(target.to, datetime.datetime.utcnow().isoformat()))

    SendQ.send = override_function
    t = target(to='test@test.com')
    sq1 = SendQ(t, 5)
    sq2 = SendQ(t, 2)
    sleep(5)
    SendQ(t)
    SendQ(t)
    SendQ(t)
    SendQ(t)
    SendQ(t)
    SendQ(t)
    SendQ(t)
    SendQ(t)
    print('sleeping 20s in main thread')
    sleep(10)
    SendQ().stop()





