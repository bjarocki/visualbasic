import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import redis
import json
import datetime
import time
import logging

class WSHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self):
        WSHandler.waiters.add(self)

    def on_close(self):
        WSHandler.waiters.remove(self)

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                if waiter.get_argument('type', default='client') == 'client':
                    waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        WSHandler.send_updates(message)


class Server(object):
    def __init__(self):
        self.application = tornado.web.Application([
            (r'/', WSHandler),
        ])

    def run(self):
        try:
            http_server = tornado.httpserver.HTTPServer(self.application)
            http_server.listen(8888)
            main_loop = tornado.ioloop.IOLoop.instance().start()
        except:
            raise
    
