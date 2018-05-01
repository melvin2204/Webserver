import sys
import configparser
import json
import logging
if __name__ == "__main__":
    sys.exit()

config = configparser.ConfigParser(allow_no_value=True)
config.read("conf/config.ini")

mimes_file = config['server']['MIMES_FILE']
mime_file = open(mimes_file,"r")
mimes = mime_file.read()
mime_file.close()
MIME_TYPES = json.loads(mimes)

loglevel = config['server']['LOG_LEVEL']
if loglevel == "":
    LOG_LEVEL = logging.NOTSET
elif loglevel == "DEBUG":
    LOG_LEVEL = logging.DEBUG
elif loglevel == "INFO":
    LOG_LEVEL = logging.INFO
elif loglevel == "WARNING":
    LOG_LEVEL = logging.WARNING
elif loglevel == "ERROR":
    LOG_LEVEL = logging.ERROR
elif loglevel == "CRITICAL":
    LOG_LEVEL = logging.CRITICAL

"""HOSTNAME = "localhost"
PORT = 8080
PUBLIC_DIR = "public" # folder to load documents from
ERROR_DOC = { #Location of error documents. Loaded from root folder
    "404":"404.html"
}
MIME_TYPES = mimes.MIME_TYPES #types of mimes the server accepts. To change add your items in mimes.py
SERVER_VERSION = "Melvin2204-webserver"
SYS_VERSION = ""
LOG_LEVEL = logging.WARNING
BEHIND_PROXY = True# if the server is behind a proxy."""