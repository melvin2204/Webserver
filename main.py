"""
Python webserver by Melvin2204
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import sys
import threading
from socketserver import ThreadingMixIn
import time
try:
    from system import ilpy  #inline python
    from system import checkport  #check if the port is free
    from system import versionCheck  #check for updates
    from system import handleQueryString  #handle GET/POST
    from system import handleRequest  #handle requests
    import conf.conf as c  # conf.py
except Exception as e:
    logging.critical("Error loading modules.")
    logging.critical(str(e))
    sys.exit()

HOSTNAME = c.config['server']['HOSTNAME']
PORT = int(c.config['server']['PORT'])
PUBLIC_DIR = c.config['server']['PUBLIC_DIR']
ERROR_DOC = c.config['error_doc']
BEHIND_PROXY = c.config['server']['BEHIND_PROXY'].lower()
MIME_TYPES = c.MIME_TYPES

class Server(BaseHTTPRequestHandler):
    server_version = "Melvin2204 Webserver"  #Name of the server in the headers
    with open("system/version.txt","r") as version:  #read the server ersion and add it to the headers
        version = version.read()
    sys_version = version
    def _set_response(self,type = "text/plain",code=200):  #write a response header
        self.send_response(code)  #response code. Default 200
        self.send_header("Content-type",type)  #Send content type header. Default text/plain
        self.send_header("download","https://github.com/melvin2204/Webserver/")  #send downloadlink header
        self.end_headers()  #send headers

    def do_GET(self):  #Get request
        handleRequest.GET(self,c)  #handle GET request

    def do_POST(self):
        handleRequest.POST(self,c)  #handle POST request

    def getFile(self,file,root = False):  #function for getting files from the server
        if root == True:  #wether to use the root dir
            loc = file
        else:  #use public dir
            loc = self.makeLocation(file)  #make the path a valid location for the server
            if loc == False:
                return 403  #access denied due to no index
        if not os.path.isfile(loc):  # the file is not found
            return 404  #return false == 404
        try:
            if loc.endswith(".ilpy"):  # if the file is an ilpy file that needs to be treated different
                tempFile = open(loc, "r")  #open the file
                data = loc  #make the data var to prevent errors
                firstLine = tempFile.readline().strip()  # read the first line to check for content type
                type = "text/plain"  #default content type
                if firstLine.startswith("#"):  #if the first line is a content type
                    header = firstLine.split(":")[0].replace(" ","")  #split the first header line and remove spaces
                    if header.lower()[1:] == "content-type":  #if the first line is a content type
                        type = firstLine.split(":")[1].replace(" ", "")  #get the content type and remove spaces
                run = True  # give it the run var to make the server parse it before outputting
            else:  #the file is not an ilpy file
                tempFile = open(loc,"rb")  #get the data in bytes
                data = tempFile.read()
                type = os.path.splitext(loc)[1][1:]  #get the file extension
                run = False  # it does not need to be ran before sending
                type = self.checkType(type)  #get the mime type
            tempFile.close()
            return (data,type,run)  #return the data
        except Exception as e:
            logging.error(e)  #an error occured
            return 503  #return 503 internal server error

    def makeLocation(self,file):  #used for making a valid location
        if os.path.isdir(PUBLIC_DIR + file) and not file.endswith("/"):  #if the path is a directory instead of a file but isnt ended with a slash.
            #make it a directory eg index.html is a folder and the user types "index.html".
            #Take them to the folder instead of the file index.html
            file = file + "/"  #add the slash
        if file.endswith("/"):  #if the path is a folder
            if os.path.isfile(PUBLIC_DIR + file + "index.ilpy"):  #check for index.ilpy.
                # if that doesn't exist search for index.html / .htm
                file = file + "index.ilpy"
            elif os.path.isfile(PUBLIC_DIR + file + "index.html"):  #no index.ilpy, search for index.html
                file = file + "index.html"
            elif os.path.isfile(PUBLIC_DIR + file + "index.htm"):  #no index.ilpy and .html, search for index.htm
                file = file + "index.htm"
            else:  #no index is found return 403
                return False
        return PUBLIC_DIR + file  #return file with public folder

    def checkType(self,extension):  #search the mime type
        type = MIME_TYPES.get(extension)  #get the mimetype based on file extension
        if type == None:  #no mime found
            return "text/plain"
        else:
            return type

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def run(server_class= HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = (HOSTNAME,PORT)  #get settings
    logging.info("Starting server")
    #httpd = server_class(server_address, handler_class)
    httpd = ThreadedHTTPServer(server_address, handler_class)  #Multi threaded
    logging.info("Running forever")
    print("Up and running! Visit {host}:{port} to use the website.".format(host=HOSTNAME, port=PORT))
    httpd.serve_forever()  #to prevent the sript from being stopped

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
    with open("system/version.txt","r") as version:
        version = version.read()  #read the version of the webserver
    print(art + version)  #print the logo
    logging.basicConfig(level=c.LOG_LEVEL)  #set logging level from config
    logging.info("Checking if port is available.")
    if not checkport.checkport(HOSTNAME,PORT):  #if the port is already used
        input("Press enter to exit.")
        sys.exit()
    if c.config["update"]["AUTO_CHECK"].lower()== "true":  #the users wants to autocheck
        if versionCheck.check(c.config["update"]['AUTO_UPDATE'].lower(),c.config["update"]["VERSION_URL"],c.config["update"]["DOWNLOAD_URL"]):  #if the server is updated
            logging.info("Updating done.")
            for i in range(0,5):
                print("Restarting server in {s}".format(s = 5 - (i)))
                time.sleep(1)
            #os.execl("main.py")
            with open("main.py","r") as code:  #read the new code and execute it
                exec(code.read())
    #all checks done, ready to start
    run(handler_class=Server)  #start the server