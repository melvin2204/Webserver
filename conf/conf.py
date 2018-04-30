import logging
import json
import mimes
HOSTNAME = "192.168.178.50"
PORT = 81
PUBLIC_DIR = "public" # folder to load documents from
ERROR_DOC = { #Location of error documents. Loaded from root folder
    "404":"404.html"
}
MIME_TYPES = mimes.MIME_TYPES #types of mimes the server accepts. To change add your items in mimes.py

