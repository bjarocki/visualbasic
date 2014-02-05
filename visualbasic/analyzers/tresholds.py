import time
import json

class Plugin(object):
    def __init__(self, websocket_clients, storage_object):
        self.run_every = 3
        self.limit_of_last_requests = 10000
        self.storage = storage_object()
        self.waiters = websocket_clients


    def __times_per_second(self, data):
        try:
            return len(data) / (float(data[0]) - float(data[len(data) - 1]))
        except:
            return None
                
    def __get_uri_times(self, uri):
        try:
            return self.storage.get(uri, self.limit_of_last_requests)
        except:
            return []

    def __get_uris(self):
        try:
            return self.storage.get_keys()
        except:
            return []

    def __send_to_waiters(self, data):
        for waiter in self.waiters:
            try:
                waiter.write_message(data)
            except Exception as e:
                print(e)

    def run(self):
        structure = {}
        while True:
            time.sleep(self.run_every)
            for uri in self.__get_uris():
                structure[uri] = self.__times_per_second(self.__get_uri_times(uri))
            self.__send_to_waiters(structure)

