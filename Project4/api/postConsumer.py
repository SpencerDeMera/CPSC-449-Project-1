import configparser
import logging.config
import hug
import sqlite_utils
import os
import json
import socket
from dotenv import load_dotenv
import greenstalk

# Parser configuator function 
#   Code provided by instructor
config = configparser.ConfigParser()
config.read("./configs/postAPI.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)

# hug directive functions for SQLite initialization & logging
#   Code provided by instructor
@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

# hug directive functions for SQLite initialization & logging
#   Code provided by instructor
@hug.directive()
def log(name=__name__, **kwargs):
    return logging.getLogger(name)

#create new Post
# Not sure if this is the right way to do this at all
@hug.get("/async")
def newAsyncPost(response, db: sqlite):
    postsArr = db["posts"]
    port = os.environ.get('postConsumer')
    domainName = socket.gethostbyname(socket.getfqdn())
    # client = greenstalk.Client((domainName, port))
    with greenstalk.Client(('127.0.0.1', 8000)) as client:
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

hug.API(__name__).http.serve(port=8600) # Force hug onto port 8600 # TESTING