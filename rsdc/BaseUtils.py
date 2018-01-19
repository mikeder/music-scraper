from tornado import gen
from tornado.httpclient import HTTPRequest
import tornado.httpclient as httpclient
import logging

httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient", max_clients=10)


class BaseUtil(object):
    @classmethod
    @gen.coroutine
    def async_curl_request(cls, a_url, a_method='GET', a_headers=None, a_data=None, a_auth_username=None,
                                    a_auth_password=None, a_follow_redirects=False, a_request_id=0, a_api_name=None,
                                    a_operation=None,a_proxy_host=None,a_proxy_port=None):
        logger = logging.getLogger(__name__)

        request_data_length = 0
        httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
        try:
            if not a_headers:
                a_headers = dict()

            '''
            # Apparently setting Content-Length makes these requests fail in Prod, commenting out for now
            if a_data:
                request_data_length = len(a_data)
                a_headers['Content-Length'] = str(request_data_length)
            '''

            http_req = HTTPRequest(url=str(a_url),
                                   method=a_method,
                                   headers=a_headers,
                                   body=a_data,
                                   connect_timeout=15,
                                   request_timeout=15,
                                   auth_username=a_auth_username,
                                   auth_password=a_auth_password,
                                   follow_redirects=a_follow_redirects,
                                   proxy_host=a_proxy_host,
                                   proxy_port=a_proxy_port)

            http_client = httpclient.AsyncHTTPClient()
            response = yield gen.Task(http_client.fetch, http_req)
            raise gen.Return(response)

        except gen.Return:
            raise  # Raise the normal return response