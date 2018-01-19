import logging

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

import AppUtils


class BaseHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request)
        self.logger = logging.getLogger(__name__)
        self.generator = AppUtils.Generator()
        self.stringutil = AppUtils.StringUtil()

    def write_error(self, status_code, **kwargs):
        self.write(str(status_code))

    @property
    def database(self):
        return self.application.database


class Scrape(BaseHandler):
    def post(self, sub):
        self.logger.info(sub)

class Alarm(BaseHandler):
    def get(self, a_alarm_id):
        alarm = self.database.getAlarms(a_alarm_id)[0]
        self.render('alarm.html', alarm=alarm)


class Home(BaseHandler):
    def get(self):
        self.render('home.html')


class Test(BaseHandler):
    def get(self):
        self.write('1')


class EchoWebSocket(WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")
