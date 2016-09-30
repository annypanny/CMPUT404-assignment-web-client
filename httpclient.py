#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        #if port == None:
        #    port = 80
        # create socket, establish connection
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            clientSocket.connect((host,port))
            print("connection succeeded")
        except Exception as e:
            print("socket error")
            sys.exit()
        return clientSocket

    def get_code(self, data):
        code = int(data.split(' ')[1])
        return code

    def get_headers(self,data):
        #headers = data.split('\r\n\r\n')[0]
        headers = data.split('\r\n\r\n')[1:-2]
        return headers

    def get_body(self, data):
        body = data.split('\r\n\r\n')[1]
        return body

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)


#    def get_url_info(self,url):
#        if url[:7] == "http://":
#            url = url[7:]

#        if "/" in url:
#            pos = url.index("/")
#            host = url[:pos]
#            path = url[pos:]

#        if ":" in url:
#            pos = url.index(":")
#            host = url[:pos]
#            port = url[pos+1:]

#        return host, path, port


    def GET(self, url, args=None):
        code = 500
        body = ""

        #host, path, port = self.get_url_info(url)
        #get path, host, port
        path = urlparse(url).path
        host = urlparse(url).hostname

        if urlparse(url).port != None:
            port = urlparse(url).port
        else:
            port = 80


        request = "GET " + path + " HTTP/1.1\r\n"\
                  "Host: " + host + "\r\n"\
                  "Accept: */*\r\n"\
                  "connection: close\r\n\r\n"

        clientSocket = self.connect(host, port)
        clientSocket.sendall(request)

        response = self.recvall(clientSocket)
        code = self.get_code(response)
        body = self.get_body(response)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        #host, path, port = self.get_url_info(url)

        path = urlparse(url).path
        host = urlparse(url).hostname

        if urlparse(url).port != None:
            port = urlparse(url).port
        else:
            port = 80

        if args != None:
            content = urllib.urlencode(args)
        else:
            content = ""

        content_length = str(len(content))

        request = "POST " + path + " HTTP/1.1\r\n"\
                  "Host: " + host + "\r\n"\
                  "Accept: */*\r\n"\
                  "Content-Length: " + content_length + "\r\n"\
                  "connection: close\r\n\r\n" + content + "\r\n\r\n"

        clientSocket = self.connect(host, port)
        clientSocket.sendall(request)

        response = self.recvall(clientSocket)
        code = self.get_code(response)
        body = self.get_body(response)

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )
