#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Abram Hindle, Nevil Kandathil Sintho, https://github.com/tywtyw2002, and https://github.com/treedust
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
import time
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = int(data.split()[1])
        return code

    def get_headers(self,data):
        """
        Skips first line of response and return all headers until the body
        """

        # responses from assignment 1 contains \n\n. Resposnes from assignment 2 tests contains \r\n
        temp_split_1 = data.split("\n\n", 2)
        temp_split_2 = data.split("\r\n\r\n", 2)
        split_data = temp_split_1
        
        if len(temp_split_1) != 2:
            split_data = temp_split_2
        
        headers = split_data[0].split("\r\n", 2)[1]
        return headers

    def get_body(self, data):
        # responses from assignment 1 contains \n\n. Resposnes from assignment 2 tests contains \r\n
        temp_split_1 = data.split("\n\n", 2)
        temp_split_2 = data.split("\r\n\r\n", 2)
        split_data = temp_split_1
        
        if len(temp_split_1) != 2:
            split_data = temp_split_2
        
        body = split_data[1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

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
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        
        # parse host and port from url string
        host = urllib.parse.urlparse(url).hostname
        port = urllib.parse.urlparse(url).port
        path = urllib.parse.urlparse(url).path

        if path == "":
            path = "/"
        
        if not port:
            port = 80
        
        # connect to host
        self.connect(host, port)

        # send GET request - reffered class notes part 5 for headers
        
        req = f"GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection:close\r\nAccept:*/*\r\nAccept-Charset:utf-8\r\n\r\n"
        print(req)
        self.sendall(req)

        

        # print("Start receiving...")
        data = self.recvall(self.socket)
        print(repr(data))
        # print("Finished receiving!!!")
        
        code = self.get_code(data)
        body = self.get_body(data)
        print(code)
        print(body)
        # headers = self.get_headers(data)
        # print(body)
        # print(headers)

        self.close()

        time.sleep(1)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        content = ""

        # parse host and port from url string
        host = urllib.parse.urlparse(url).hostname
        port = urllib.parse.urlparse(url).port
        path = urllib.parse.urlparse(url).path

        if path == "":
            path = "/"

        if not port:
            port = 80

        # there is some data to be posted in the args variable, encode it using urlencode
        if args:
            content = urllib.parse.urlencode(args)

        # connect to host
        self.connect(host, port)

        # send GET request - reffered class notes part 5 for headers
        req = f"POST {path} HTTP/1.1 \r\nHost:{host}\r\nConnection:close\r\nAccept:*/*\r\nAccept-Charset:utf-8\r\nContent-Length:{len(content)}\r\nContent-Type:application/x-www-form-urlencoded\r\n\r\n{content}"
        self.sendall(req)

        # print("Start receiving...")
        data = self.recvall(self.socket)
        # print("Finished receiving!!!")
        
        code = self.get_code(data)
        body = self.get_body(data)
        # headers = self.get_headers(data)
        self.close()
        
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
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))


    http = HTTPClient()
    req = http.GET("http://%s:%d" % ("localhost",8080) )
    
    # print(req)