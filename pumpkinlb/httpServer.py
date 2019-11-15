# PumpkinLB Copyright (c) 2014-2015, 2017 Tim Savannah under GPLv3.
# You should have received a copy of the license as LICENSE
#
# See: https://github.com/kata198/PumpkinLB

import json
import multiprocessing
from http.server import HTTPServer, BaseHTTPRequestHandler
# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from functools import partial

def MakeHandlerClassFromArgv(algorithmQueue):
    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler, object):
        def __init__(self, *args, **kwargs):
            # self.do_stuff(algorithmQueue)
            self.algorithmQueue = algorithmQueue
            super(SimpleHTTPRequestHandler, self).__init__(*args, **kwargs)




        # def do_stuff(self, algorithmQueue):


        def _set_headers(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def _html(self, message):
            """This just generates an HTML document that includes `message`
            in the body. Override, or re-write this do do more interesting stuff.
            """
            content = ""
            return content.encode("utf8")  # NOTE: must return a bytes object!

        def do_GET(self):
            self._set_headers()
            self.wfile.write(self._html("hi!"))

        def do_HEAD(self):
            self._set_headers()

        def do_POST(self):
            self._set_headers()
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            temp = (json.loads(body))["servers"]
            self.algorithmQueue.put(temp)
            response = BytesIO()
            response.write(b'Received: ')
            response.write(body)
            self.wfile.write(response.getvalue())
    return SimpleHTTPRequestHandler

class HttpServerReq(multiprocessing.Process):
    '''
        Class that run Http server that listen to the Dynamic load balancer algorithm changer requests
    '''

    def __init__(self, httpServerAddress, httpServerPort, algorithmQueue=[]):
        multiprocessing.Process.__init__(self)
        self.httpServerAddress = httpServerAddress
        self.httpServerPort = httpServerPort
        self.algorithmQueue = algorithmQueue

    def run(self):
        server_address = ("localhost", 9090)
        HandlerClass = MakeHandlerClassFromArgv(self.algorithmQueue)
        httpd = HTTPServer(server_address, HandlerClass)
        httpd.serve_forever()
