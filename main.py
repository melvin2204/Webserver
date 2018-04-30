"""
Python webserver by Melvin2204
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import sys
sys.path.append("conf")
import conf as c # conf.py
ADDRESS = c.ADDRESS
PORT = c.PORT
PUBLIC_DIR = c.PUBLIC_DIR
ERROR_DOC = c.ERROR_DOC
MIME_TYPES = c.MIME_TYPES

class Server(BaseHTTPRequestHandler):
    def _set_resonse(self,type = "text/html"):
        self.send_response(200)
        self.send_header("Content-type",type)
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        file = self.getFile(self.path)
        if not file == False:
            self._set_resonse(type = file[1])
            self.wfile.write(file[0].encode('utf-8'))
        else:
            error_doc = self.getFile(ERROR_DOC.get("404"),root=True)
            if error_doc == False:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write("404 not found but another 404 occurred when loading the error document.".encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header("Content-type", error_doc[1])
                self.end_headers()
                self.wfile.write(error_doc[0].encode('utf-8'))

    def getFile(self,file,root = False):
        if os.path.isdir(PUBLIC_DIR + file):
            file = file + "/"
        if file.endswith("/"):
            file = file + "index.html"
        if root == True:
            loc = file
        else:
            loc = PUBLIC_DIR + file
        if not os.path.isfile(loc):
            return False
        try:
            tempFile = open(loc,"r")
            data = tempFile.read()
            tempFile.close()
            type = os.path.splitext(loc)[1][1:]
            return (data,self.checkType(type))
        except:
            return False

    def checkType(self,extension):
        type = MIME_TYPES.get(extension)
        if type == None:
            return "text/plain"
        else:
            return type



def run(server_class= HTTPServer, handler_class=BaseHTTPRequestHandler):
    logging.basicConfig(level=logging.INFO)
    server_address = (ADDRESS,PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run(handler_class=Server)