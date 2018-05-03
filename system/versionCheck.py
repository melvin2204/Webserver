#https://raw.githubusercontent.com/melvin2204/Webserver/beta/system/version.txt
#https://github.com/melvin2204/Webserver/archive/master.zip
import requests
import logging
import sys,os
import urllib.request
import zipfile
import time

backupFiles = ["conf/config.ini","conf/mimes.json"]

def compareVersions(v):
    return tuple(map(int, (v.split("."))))

def check(autoUpdate,versionUrl,downloadUrl):
    global backupFiles
    logging.info("Checking for updates from " + versionUrl)
    r = ""
    update = False
    try:
        r = requests.get(versionUrl, timeout=3)
        versionChecked = r.content.decode("utf-8").rstrip()
        with open("system/version.txt", "r") as f:
            versionNow = f.read()
        logging.info("Your version: {v1}. Newest version {v2}".format(v1=versionNow, v2=versionChecked))
        update = compareVersions(versionChecked) > compareVersions(versionNow)
        if update:
            logging.info("Update available to V{v}".format(v = versionChecked))
            if not autoUpdate == "true":
                if input("Do you want to update now (y/n) ").lower().strip() == "y":
                    autoUpdate = "true"
        else:
            logging.info(" V{version} is most recent".format(version = versionNow))
    except Exception as e:
        logging.error("Failed to check for updates.")
    try:
        if autoUpdate == "true" and update:
            for i in range(0,5):
                print("Downloading and installing update in {s}".format(s = 5 - (i)))
                time.sleep(1)
            logging.info("Downloading update from " + downloadUrl)
            urllib.request.urlretrieve(downloadUrl, "temp.zip")
            for file in backupFiles:
                logging.info("Backing up " + file)
                with open(file, "r") as f:
                    backup = open(file + ".backup", "w")
                    backup.write(f.read())
                    backup.close()
            logging.info("Installing files.")
            try:
                zip_ref = zipfile.ZipFile("temp.zip", 'r')
                zip_ref.extractall(".")
                zip_ref.close()
                os.remove("temp.zip")
            except Exception as e:
                logging.error("Failed to install updates. " + str(e))
                return False
            return True#restart server
        else:
            return False
    except Exception as e:
        logging.error("Failed to update webserver.")
    return False

def run():
    sys.exit()

if __name__ == "__main__":
    run()