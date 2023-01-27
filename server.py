#  coding: utf-8 
import socketserver
import os
from os import path

# Copyright 2023 Abram Hindle, Eddie Antonio Santos, Georgin Maliakal

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved

# http://docs.python.org/2/library/socketserver.html

# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #web_dir = os.path.join(os.path.dirname(__file__), 'www')
        #os.chdir(web_dir)
        #Handler = http.server.SimpleHTTPRequestHandler
        #httpd = socketserver.TCPServer(("", PORT), Handler)



        self.data = self.request.recv(1024).strip()
        strdata = str(self.data)
        newdata = strdata.split()[1]
        first = strdata.split()[0]
        getmsg = "GET"

       
       
        if getmsg in first:
            pass
        else:
            response = "HTTP/1.1 405\r\nContent-Type: text/\r\n\r\n"
            self.request.sendall(response.encode())


        
        

        #try:
        mypath = str(os.getcwd())+"/www"+newdata
        
        

        if "../" in mypath:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            self.request.sendall(response.encode())


        # checks to see if the file exists
        if path.isfile(mypath):
            file_type = (newdata.split("."))[1]
            f = open(mypath,"r")
            text = f.read()
            response = "HTTP/1.1 200\r\nContent-Type: text/"+file_type+"\r\n\r\n" + text
            self.request.sendall(response.encode())
            
        

        # check to see if its a directory
        elif path.isdir(mypath):
            datalength = len(newdata)
            last_value=newdata[datalength-1]
            

            # send a 200 OK if slash is included
            if last_value == "/":
                #file_type = (newdata.split("."))[1]
                f = open(mypath+"index.html","r")
                text = f.read()
                response = "HTTP/1.1 200\r\nContent-Type: text/html\r\n\r\n" + text
                self.request.sendall(response.encode())


            # send a 302 moved error if slash is not included and redirect
            else:
                #file_type = (newdata.split("."))[1]
                #f = open(mypath+"/index.html","r")
                #text = f.read()
                response = "HTTP/1.1 301\r\nLocation: "+"http://127.0.0.1:8080"+newdata+"/\r\n\r\n"
                self.request.sendall(response.encode())
                


        else:
            #print("sent error 404")
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            self.request.sendall(response.encode())



        # except:
        #     response = "HTTP/1.1 404\r\nContent-Type: text/\r\n\r\n"
        #     self.request.sendall(response.encode())
           


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    #myfolder = "/Users/Georgin/Desktop/CMPUT404/A1/CMPUT404-assignment-webserver"

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


