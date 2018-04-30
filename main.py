"""
Python webserver by Melvin2204
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import sys
try:
    import conf.conf as c # conf.py
except:
    logging.critical("Could not find conf.py.")
    sys.exit()
HOSTNAME = c.HOSTNAME
PORT = c.PORT
PUBLIC_DIR = c.PUBLIC_DIR
ERROR_DOC = c.ERROR_DOC
MIME_TYPES = c.MIME_TYPES

class Server(BaseHTTPRequestHandler):
    server_version = c.SERVER_VERSION
    sys_version = c.SYS_VERSION
    def _set_resonse(self,type = "text/plain",code=200):
        self.send_response(code)
        self.send_header("Content-type",type)
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        file = self.getFile(self.path)
        if not file == False:
            folder = os.path.dirname(self.makeLocation(self.path))
            if os.path.isfile(folder + "/run.py"):
                logging.info("Found a run.py in " + folder)
                arguments = {
                    "self": self
                }
                exec(open(folder + "/run.py").read(), arguments)
            self._set_resonse(type=file[1],code=200)
            self.wfile.write(file[0])
        else:
            error_doc = self.getFile(ERROR_DOC.get("404"),root=True)
            if error_doc == False:
                self._set_resonse(type="text/plain",code=404)
                self.wfile.write("404 not found but another 404 occurred when loading the error document.".encode('utf-8'))
            else:
                self._set_resonse(type=error_doc[1],code=404)
                self.wfile.write(error_doc[0])

    def do_POST(self):
        #content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        #post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",str(self.path), str(self.headers), post_data.decode('utf-8'))
        #self._set_response()
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        self._set_resonse(type="text/plain", code=405)
        self.wfile.write("405 - No post requests".encode('utf-8'))

    def getFile(self,file,root = False):
        if root == True:
            loc = file
        else:
            loc = self.makeLocation(file)
        if not os.path.isfile(loc):
            return False
        try:
            tempFile = open(loc,"rb")
            data = tempFile.read()
            tempFile.close()
            type = os.path.splitext(loc)[1][1:]
            return (data,self.checkType(type))
        except Exception as e:
            print(e)
            return False

    def makeLocation(self,file):
        if os.path.isdir(PUBLIC_DIR + file):
            file = file + "/"
        if file.endswith("/"):
            file = file + "index.html"
        return PUBLIC_DIR + file

    def checkType(self,extension):
        type = MIME_TYPES.get(extension)
        if type == None:
            return "text/plain"
        else:
            return type



def run(server_class= HTTPServer, handler_class=BaseHTTPRequestHandler):
    logging.basicConfig(filename="server.log",level=c.LOG_LEVEL)
    server_address = (HOSTNAME,PORT)
    logging.info("Starting server")
    httpd = server_class(server_address, handler_class)
    logging.info("Running forever")
    httpd.serve_forever()

if __name__ == "__main__":
    run(handler_class=Server)