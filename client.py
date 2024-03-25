from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect

class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.msg = []

    def start(self):
        self.connect()
        PeriodicCallback(self.keep_alive, 20000).start()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        print("trying to connect")
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception as e:
            print("connection error", e)
        else:
            print("connected")
            self.run()

    @gen.coroutine
    def run(self):
        while True:
            data = yield self.ws.read_message()
            self.msg.append(data)
    
    def send(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("Hello World")

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("keep alive")