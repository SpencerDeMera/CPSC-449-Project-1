import hug
import configparser
import logging.config
import sqlite_utils
import requests
import datetime
import json
import time
from userAPI import userAuth
import os
import socket
from dotenv import load_dotenv
import greenstalk

# Parser configuator function 
#   Code provided by instructor
config = configparser.ConfigParser()
config.read("./configs/postAPI.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)

#   Code provided by instructor
def sqlite(section="sqlite", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

#   Code provided by instructor
def log(name=__name__, **kwargs):
    return logging.getLogger(name)

#create new Post
# Not sure if this is the right way to do this at all
def newAsyncPost(db: sqlite, response):
    postsArr = db["posts"]
    port = os.environ.get('postConsumer')
    domainName = socket.gethostbyname(socket.getfqdn())
    # client = greenstalk.Client((domainName, port))
    client = greenstalk.Client(('127.0.0.1', 8600))

    while True:
        job = client.reserve()
        print(job.body)
        data = json.loads(job.body)

        try:
            postsArr.insert(data)
            newPost["id"] = postsArr.last_pk
        except Exception as e:
            response.status = hug.falcon.HTTP_409
            return {"error": str(e)}
            response.set_header("Location", f"/posts/{newPost['id']}")
        return data
