import logging
import json
import mimes
HOSTNAME = "localhost"
PORT = 8080
PUBLIC_DIR = "public" # folder to load documents from
ERROR_DOC = { #Location of error documents. Loaded from root folder
    "404":"404.html"
}
MIME_TYPES = mimes.MIME_TYPES #types of mimes the server accepts. To change add your items in mimes.py
SERVER_VERSION = "Melvin2204-webserver"
SYS_VERSION = "1.0"
LOG_LEVEL = logging.WARNING