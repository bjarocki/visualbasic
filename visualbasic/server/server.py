import multiprocessing
import threading
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import redis
import json
import sys
import time
import logging
import syslog
import traceback

import feeds
from feeds import *

import analyzers
from analyzers import *

from storage import RedisStorage as Storage

waiters = set()


def feed_executor(plugin_name, storage_object):
    try:
        p = getattr(feeds, plugin_name).Plugin(storage_object)
        return(p.run())
    except Exception as e:
        syslog.syslog(
            syslog.LOG_ERR,
            "Exception %s %r" % (e, traceback.format_exc(800))
        )


def analyzers_executor(storage_object):
    for analyzer in analyzers.__all__:
        try:
            p = getattr(analyzers, analyzer).Plugin(waiters, storage_object)
            return(p.run())
        except Exception as e:
            syslog.syslog(
                syslog.LOG_ERR,
                "Exception %s %r" % (e, traceback.format_exc(800))
            )


class WSHandler(tornado.websocket.WebSocketHandler):

    def allow_draft76(self):
        return True

    def open(self):
        waiters.add(self)

    def on_close(self):
        waiters.remove(self)


class Server(object):

    def __init__(self):
        try:
            self.application = tornado.web.Application([
                (r'/', WSHandler),
            ])

            self.feeders_pool = multiprocessing.Pool()
            self.storage = Storage.Storage

            for feeder in feeds.__all__:
                self.feeders_pool.apply_async(
                    feed_executor, args=(feeder, self.storage, ))

            threading.Thread(
                target=analyzers_executor,
                args=(
                    self.storage,
                )).start(
            )

        except Exception as e:
            print(sys.modules[__name__], e)
            raise

    def run(self):
        try:
            http_server = tornado.httpserver.HTTPServer(self.application)
            http_server.listen(8888)
            main_loop = tornado.ioloop.IOLoop.instance().start()
        except Exception as e:
            print(sys.modules[__name__], e)
