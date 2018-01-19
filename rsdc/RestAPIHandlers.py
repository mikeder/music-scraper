import datetime
import json
import markdown
import uuid
from tornado import gen

import AppUtils
import BaseUtils
import WebHandlers


@gen.coroutine
class Alarm(WebHandlers.BaseHandler):
    def get(self):
        data = yield BaseUtils.BaseUtil.async_curl_request('https://www.google.com')
        self.finish(gen.Return(data.body))

    def post(self):
        self.logger.debug('Received new alarm: %s' % self.request.body)
        data = json.loads(self.request.body)
        data['title'] = self.stringutil.sanitize(data['title'])
        data['description'] = self.stringutil.sanitize(data['description'])
        data['description'] = markdown.markdown(data['description'])
        data['alarm_id'] = self.generator.random_string()
        response = self.database.addAlarm(data)
        if response['status'] == 'ok':
            # Set all client updateDue bits except for the one that is calling
            response = self.database.setUpdateDue(data['uuid'])
            self.finish(response)
        elif response['status'] == 'error':
            self.logger.error(response)
            self.finish(response)
        else:
            self.finish(response)

    def delete(self, a_alarm):
        self.logger.debug('Deleting: %s from database' % a_alarm)
        # Set all client updateDue bits except for the one that is calling
        response = self.database.deleteAlarm(a_alarm)
        self.database.setUpdateDue()
        self.finish(response)


class Scrape(WebHandlers.BaseHandler):
    def post(self):
        print self.request.body
        print self.get_body_argument('sub', None)


class Heartbeat(WebHandlers.BaseHandler):
    def get(self):
        clients = self.database.getClients()
        if clients:
            self.finish({'clients':clients})
        else:
            self.finish('None')

    def post(self):
        # Full client columns:
        # start, end, uuid, address, focus, url
        # ajax will include: uuid(sometimes), focus, url
        data = json.loads(self.request.body)
        x_real_ip = self.request.headers.get("X-Real-IP")
        data['address'] = x_real_ip or self.request.remote_ip
        now = datetime.datetime.now()
        data['start'] = now
        data['end'] = now + datetime.timedelta(minutes=1)
        if data['uuid'] != '' or data['uuid']:
            update = self.database.getUpdateDue(data['uuid'])[0]
            response = self.database.updateClient(data)
            if update['refresh'] == 0 or update['refresh'] == '0':
                response['refresh'] = 0
            elif update['refresh'] == 1 or update['refresh'] == '1':
                response['refresh'] = 1
            self.logger.debug(response)
            self.set_status(200,'Client updated')
            self.finish(response)
        else:
            data['uuid'] = str(uuid.uuid4())
            data['refresh'] = '0'
            response = self.database.addClient(data)
            self.logger.debug(response)
            self.set_status(201,'Client Added')
            self.finish(response)