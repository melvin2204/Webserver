"""
Python webserver by Melvin2204
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import sys
import threading
from socketserver import ThreadingMixIn
import extensions.ilpy as ilpy
try:
    import conf.conf as c # conf.py
except:
    logging.critical("Could not find conf.py.")
    sys.exit()

HOSTNAME = c.config['server']['HOSTNAME']
PORT = int(c.config['server']['PORT'])
PUBLIC_DIR = c.config['server']['PUBLIC_DIR']
ERROR_DOC = c.config['error_doc']
BEHIND_PROXY = c.config['server']['BEHIND_PROXY'].lower()
MIME_TYPES = c.MIME_TYPES

class Server(BaseHTTPRequestHandler):
    server_version = c.config['server']['SERVER_VERSION']
    sys_version = c.config['server']['SYS_VERSION']
    def _set_resonse(self,type = "text/plain",code=200):
        self.send_response(code)
        self.send_header("Content-type",type)
        self.end_headers()

    def do_GET(self):#Get request
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        file = self.getFile(self.path)#file contents of request path. Returns false if 404
        if not file == False:
            if file[2]:
                REMOTE_ADDR = self.client_address[0]
                HOST = self.headers.get("Host")
                USER_AGENT = self.headers.get('User-Agent')
                CONTENT_TYPE = "text/plain"
                if BEHIND_PROXY == "true":
                    REMOTE_ADDR = self.headers.get("X-Forwarded-For")
                    HOST = self.headers.get("X-Forwarded-Host")
                arguments = {
                    "self": self,
                    "REMOTE_ADDR": REMOTE_ADDR,
                    "HOST": HOST,
                    "USER_AGENT": USER_AGENT,
                    "CONTENT_TYPE": CONTENT_TYPE
                }
                self._set_resonse(type=file[1], code=200)
                #exec(file[0], arguments)
                dir_path = os.path.dirname(os.path.realpath(__file__))
                output = ilpy.run(dir_path + "/" + file[0],arguments)
                firstLine = output.split("\n",1)[0]
                if firstLine.startswith("#"):
                    output = output.split("\n",1)[1]
                self.wfile.write(output.encode("utf-8"))
            else:
                self._set_resonse(type=file[1],code=200)
                self.wfile.write(file[0])
        else:
            error_doc = self.getFile(ERROR_DOC.get("404"),root=True)
            if error_doc == False:
                self._set_resonse(type="text/plain",code=404)
                self.wfile.write(b"404 not found but another 404 occurred when loading the error document.")
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
            if loc.endswith(".ilpy"):
                tempFile = open(loc, "r")
                data = loc
                firstLine = tempFile.readline().strip()
                type = "text/plain"
                if firstLine.startswith("#"):
                    header = firstLine.split(":")[0].replace(" ","")
                    if header.lower()[1:] == "content-type":
                        type = firstLine.split(":")[1].replace(" ", "")
                run = True
            else:
                tempFile = open(loc,"rb")
                data = tempFile.read()
                type = os.path.splitext(loc)[1][1:]
                run = False
                type = self.checkType(type)
            tempFile.close()
            return (data,type,run)
        except Exception as e:
            print(e)
            return False

    def makeLocation(self,file):
        if os.path.isdir(PUBLIC_DIR + file) and not file.endswith("/"):
            file = file + "/"
        if file.endswith("/"):
            if os.path.isfile(PUBLIC_DIR + file + "index.ilpy"):
                file = file + "index.ilpy"
            else:
                file = file + "index.html"
        return PUBLIC_DIR + file

    def checkType(self,extension):
        type = MIME_TYPES.get(extension)
        if type == None:
            return "text/plain"
        else:
            return type

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def run(server_class= HTTPServer, handler_class=BaseHTTPRequestHandler):
    logging.basicConfig(level=c.LOG_LEVEL)
    server_address = (HOSTNAME,PORT)
    logging.info("Starting server")
    #httpd = server_class(server_address, handler_class)
    httpd = ThreadedHTTPServer(server_address, handler_class)#Multi threaded
    logging.info("Running forever")
    print("Up and running! Visit {host}:{port} to use the website.".format(host=HOSTNAME, port=PORT))
    httpd.serve_forever()

art = """\
  __  __      _       _       ___  ___   ___  _  _   
 |  \/  |    | |     (_)     |__ \|__ \ / _ \| || |  
 | \  / | ___| |_   ___ _ __    ) |  ) | | | | || |_ 
 | |\/| |/ _ \ \ \ / / | '_ \  / /  / /| | | |__   _|
 | |  | |  __/ |\ V /| | | | |/ /_ / /_| |_| |  | |  
 |_|  |_|\___|_| \_/ |_|_| |_|____|____|\___/   |_|  
              | |                                    
 __      _____| |__  ___  ___ _ ____   _____ _ __    
 \ \ /\ / / _ \ '_ \/ __|/ _ \ '__\ \ / / _ \ '__|   
  \ V  V /  __/ |_) \__ \  __/ |   \ V /  __/ |      
   \_/\_/ \___|_.__/|___/\___|_|    \_/ \___|_|      
                                                     
                                                     
"""

if __name__ == "__main__":
    print(art)
    run(handler_class=Server)