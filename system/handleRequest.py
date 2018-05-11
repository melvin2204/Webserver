from system import ilpy  #inline python
from system import handleQueryString  #handle GET/POST
import logging
def GET(self,c):
    path = self.path  # the requested path including GET query
    queryString = {}
    if "?" in self.path:  # if the path contains a query
        path = self.path.split("?")[0]  # split it
        queryString = handleQueryString.parse(self.path.split("?")[1])  # Parse the query string
    file = self.getFile(path)  # file contents of request path. Returns code on error, tuple on success
    if checkCode(self,file,c):  # if the file is found
        if file[2]:  # if the file is an ilpy file
            REMOTE_ADDR = self.client_address[0]  # user ip
            HOST = self.headers.get("Host")  # host
            USER_AGENT = self.headers.get('User-Agent')  # useragent
            if c.config['server']['BEHIND_PROXY'].lower() == "true":  # if the server is behind a proxy, use the forwarded for headers
                REMOTE_ADDR = self.headers.get("X-Forwarded-For")
                HOST = self.headers.get("X-Forwarded-Host")
            arguments = {
                "self": self,
                "REMOTE_ADDR": REMOTE_ADDR,
                "HOST": HOST,
                "USER_AGENT": USER_AGENT,
                "GET": queryString,
                "POST": {}
            }  # add the arguments to a dict
            self._set_response(type=file[1], code=200)  # set the response header
            output = ilpy.run(file[0],arguments)  # Parse and run the ilpy file. Catch output afterwards
            firstLine = output.split("\n", 1)[0]  # get the first line of the output to remove the content-type
            if firstLine.startswith("#"):  # if there is a comment (content-type)
                output = output.split("\n", 1)[1]  # remove it
            self.wfile.write(output.encode("utf-8"))  # write the final output to the response
        else:  # the file does not need to be ran first
            self._set_response(type=file[1], code=200)  # set the response header
            self.wfile.write(file[0])  # write the output to the response

def POST(self,c):
    path = self.path  # the requested path including GET query
    queryString = {}
    if "?" in self.path:  # if the path contains a query
        path = self.path.split("?")[0]  # split it
        queryString = handleQueryString.parse(self.path.split("?")[1])  # Parse the query string
    file = self.getFile(path)  # file contents of request path. Returns code on error, tuple on success
    content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
    post_data = self.rfile.read(content_length).decode('utf-8')  # <--- Gets the data itself
    post_data = handleQueryString.parse(post_data)  #get the post data in a dict
    if checkCode(self,file,c):  # if the file is found
        if file[2]:  # if the file is an ilpy file
            REMOTE_ADDR = self.client_address[0]  # user ip
            HOST = self.headers.get("Host")  # host
            USER_AGENT = self.headers.get('User-Agent')  # useragent
            if c.config['server']['BEHIND_PROXY'].lower() == "true":  # if the server is behind a proxy, use the forwarded for headers
                REMOTE_ADDR = self.headers.get("X-Forwarded-For")
                HOST = self.headers.get("X-Forwarded-Host")
            arguments = {
                "self": self,
                "REMOTE_ADDR": REMOTE_ADDR,
                "HOST": HOST,
                "USER_AGENT": USER_AGENT,
                "GET": queryString,
                "POST": post_data,
            }  # add the arguments to a dict
            self._set_response(type=file[1], code=200)  # set the response header
            output = ilpy.run(file[0],arguments)  # Parse and run the ilpy file. Catch output afterwards
            firstLine = output.split("\n", 1)[0]  # get the first line of the output to remove the content-type
            if firstLine.startswith("#"):  # if there is a comment (content-type)
                output = output.split("\n", 1)[1]  # remove it
            self.wfile.write(output.encode("utf-8"))  # write the final output to the response
        else:  # the file does not need to be ran first
            self._set_response(type=file[1], code=200)  # set the response header
            self.wfile.write(file[0])  # write the output to the response

def checkCode(self,code,c):
    if type(code) is tuple:
        return True
    elif code == 503:  # if a 503 occured
        self._set_response(type="text/plain", code=503)
        # self.wfile.write(b"404 not found but an error occurred when loading the error document.")
    elif code == 403:  # if a 403 occured
        self._set_response(type="text/plain", code=403)
        # self.wfile.write(b"404 not found but an error occurred when loading the error document.")
    else:  # the file is not found
        error_doc = self.getFile(c.config['error_doc'].get("404"), root=True)  # Get the 404 page location
        if not type(code) is tuple:  # an error occured when loading the 404 file
            self._set_response(type="text/plain", code=404)
            self.wfile.write(b"404 not found but an error occurred when loading the error document.")
        else:  # the file is found
            self._set_response(type=error_doc[1], code=404)
            self.wfile.write(error_doc[0])  # write the output of the 404 file