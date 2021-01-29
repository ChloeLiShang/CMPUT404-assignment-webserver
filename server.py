#  coding: utf-8
import socketserver
import os.path
import mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#

# Copyright 2021 Li Shang

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print("Got a request of: %s\n" % self.data)

        host = "http://127.0.0.1:8080/"

        # decode request string
        decode_string = self.data.decode('utf-8')
        # split decoded string
        split_string = decode_string.split('\r\n')

        request = split_string[0].split()

        # handle request
        if request[0] == 'GET':
            # get path
            path = './www' + request[1]
            path_ending = path[-1]
            # collapse path
            # https://docs.python.org/3/library/os.path.html#os.path.normpath
            path = os.path.normpath(path)
            # https://www.guru99.com/python-check-if-file-exists.html
            # check if path exists and is under ./wwww
            if os.path.exists(path) and path.split('/')[0] == 'www':
                # if path is a directory
                if os.path.isdir(path):
                    if path_ending == '/':
                        new_path = path + '/index.html'
                        self.okResponse(new_path)
                    else:
                        new_path = host + request[1] + '/'
                        self.request.sendall(bytearray(
                            "HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/plain\r\nRedirect to " + new_path + "\r\nLocation: " + new_path, 'utf-8'))
                else:
                    # path is a file
                    self.okResponse(path)
            else:
                self.request.sendall(
                    bytearray("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nPath Not Found :(", 'utf-8'))
        else:
            # Non GET request
            self.request.sendall(
                bytearray("HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\nMethod Not Allowed :(", 'utf-8'))

    def okResponse(self, path):
        # get mime type of file
        # https://www.tutorialspoint.com/How-to-find-the-mime-type-of-a-file-in-Python
        mimetype = mimetypes.MimeTypes().guess_type(path)[0]
        f = open(path, 'r')
        page = f.read()
        f.close()
        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: " + mimetype + "\r\n\r\n"+page, 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
