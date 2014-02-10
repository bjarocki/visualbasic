import time
import json


class Plugin(object):

    def __init__(self, websocket_clients, storage_object):
        self.run_every = 10
        self.limit_of_last_requests = 10000
        self.storage = storage_object()
        self.waiters = websocket_clients
        self.tresholds = {
            'below': 10,
            'above': 100
        }

    def __records_newer_than(self, data, time_limit):
        return len([v for v in data if int(float(v)) > int(time_limit)])

    def __times_per_second(self, data):
        try:
            return (
                self.__records_newer_than(
                    data,
                    time.time() - self.run_every) / self.run_every
            )
        except:
            return 0

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

    def __apply_alerts(self, uris):
        for uri in uris:
            try:
                if uris[uri]['requests_per_seconds'] < self.tresholds['below']:
                    uris[uri]['status'] = 'ALERT'
                elif uris[uri]['requests_per_seconds'] > self.tresholds['above']:
                    uris[uri]['status'] = 'ALERT'
                else:
                    uris[uri]['status'] = 'OK'
            except:
                pass

    def __send_to_waiters(self, data):
        for waiter in self.waiters:
            try:
                waiter.write_message(
                    json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
            except Exception as e:
                print(e)

    def run(self):
        structure = {}
        while True:
            time.sleep(self.run_every)
            for uri in self.__get_uris():
                structure[uri] = {
                    'requests_per_seconds':
                    self.__times_per_second(self.__get_uri_times(uri))
                }
            self.__apply_alerts(structure)
            self.__send_to_waiters(structure)
