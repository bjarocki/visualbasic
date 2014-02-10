import time
from parser import w3c
import sys


class Plugin(object):

    def __init__(self, Storage):
        try:
            self.filepath = '/tmp/test.log'
            self.file = open(self.filepath)
            self.storage = Storage()
        except Exception as e:
            print(sys.modules[__name__], e)
            raise

    def __follow(self):
        self.file.seek(0, 2)
        while True:
            line = self.file.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

    def run(self):
        try:
            p = w3c.Parser()
            for line in self.__follow():
                if not self.storage.push(p.get_key(line, 'uri'), str(time.time())):
                    return False
        except Exception as e:
            print(e)
            raise
