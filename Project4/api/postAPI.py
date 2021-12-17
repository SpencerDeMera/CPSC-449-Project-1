# run hug server: hug -f api.py
# run GET/POST in termial: 
#   http <http method> localhost:8000/posts/newPost username=jackMan etc

import configparser
import logging.config
import hug
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
from pollsWorker import removePoll
import re

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

# Startup function
# @hug.startup()
# def startup(self):
#     time.sleep(10)
#     load_dotenv()
#     ctr = 0
#     portCtr = os.environ.get('PostAPI_num')
#     port = os.environ.get('postAPI')
#     srvcPort = os.environ.get('srvcRegAPI')
#     domainName = socket.gethostbyname(socket.getfqdn())
#     while ctr < int(portCtr):
#         pload = {'name': 'posts', 'domainName': domainName, 'port': port}
#         r = requests.post(domainName + ":" + srvcPort + "/register", data=pload)
#         port += 1
#         ctr += 1

# Health check function
@hug.get("/health")
def healthy(response):
    return {"Posts Health Check": "Done"}

# endpoint for checking if post is valid
@hug.get("/posts/isValid:{post_id}")
def isValid(
    post_id: hug.types.text,
    response,
    db: sqlite
):
    # Checks if post_id is valid
    posts = sqlite_utils.Database("./data/posts.db")
    for row in posts.query(
        "SELECT * FROM posts WHERE id=:postID",
        {"postID": int(post_id)}
    ):
        # If post with post_id is real 
        if row != None:
            return True
        else:
            return False

# User Timeline
@hug.get("/posts/{username}/user")
def getUserTimeline(response, username: hug.types.text, db: sqlite):
    postArr = [] # JSON array for storing all post objects of the given user
    try:
        posts = sqlite_utils.Database("./data/posts.db")
        # get all posts from user in DESC order according to timestamp
        for row in posts.query(
            "SELECT * FROM posts WHERE author_username=:userAuth ORDER BY timestamp DESC",
            {"userAuth": username}
        ):
            postArr.append(row)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": postArr}

# Home Timeline
@hug.get("/posts/{username}/home",requires=hug.authentication.basic(userAuth))
def getHomeTimeline(response, username: hug.types.text, db: sqlite, logger:log):
    followingUsers = []
    allPosts = []
    postArr = [] # JSON array for storing all post objects of the given followers user
    inputUser = username
    try:
        posts = sqlite_utils.Database("./data/posts.db")

        # TODO: Get usernames of those followed by {username}
        url = "http://localhost:8100/users/" + str(username) + "/getFollowing"
        
        followingUsers  = requests.get(url).json()
        
        # get all posts in DESC order according to timestamp
        # use WITH in SQL
        for post in posts.query(
            "SELECT * FROM posts ORDER BY timestamp DESC"
        ):
            allPosts.append(post)

        # get all posts of user and those followed by user
        for post in allPosts:
            ctr = 0 # ctr for iterating followingUsers dictionary
            postedCtr = 0 # ctr for if current post was already displayed
                          # user posts will get posted len(followingUsers) times per user post
            while ctr < len(followingUsers):
                if post['author_username'] == username and postedCtr < 1:
                    postArr.append(post)
                    postedCtr += 1 # increment post already displayed ctr
                elif post['author_username'] == followingUsers[ctr]['following_username']:
                    postArr.append(post)
                ctr += 1 # increment iterator ctr
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": postArr}

# Public Timeline
@hug.get("/posts/public")
def getPublicTimeline(response, db: sqlite):
    postArr = [] # JSON array for storing each post object
    try:
        posts = sqlite_utils.Database("./data/posts.db")
        # get all posts in DESC order according to timestamp
        for row in posts.query(
            "SELECT * FROM posts ORDER BY timestamp DESC"
        ):
            postArr.append(row)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": postArr}

#create new Post
@hug.post("/posts/{username}/newPost",requires=hug.authentication.basic(userAuth))
def newPost(
    username: hug.types.text,
    message: hug.types.text,
    response,
    db: sqlite,
):
    postsArr = db["posts"]
    posts = sqlite_utils.Database("./data/posts.db")
    ctr = 0
    ct = datetime.datetime.now()
    ts = ct.timestamp()

    # Gets count of rows already in table
    for post in posts.query("SELECT P.id FROM posts P"):
        ctr += 1

    ctr+=1
    newPost = {
        "id": ctr,
        "author_username": username,
        "message": message,
        "human_timestamp": str(ct),
        "timestamp": ts,
        "origin_URL": None,
    }

    try:
        postsArr.insert(newPost)
        newPost["id"] = postsArr.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}
        response.set_header("Location", f"/posts/{newPost['id']}")
    return newPost

# ASYNC newPost method
@hug.post("/posts/async/{username}/newPost")
def newAsyncPost(
    username: hug.types.text,
    message: hug.types.text,
    response,
    db: sqlite,
):
    postsArr = db["posts"]
    posts = sqlite_utils.Database("./data/posts.db")
    ctr = 0
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    # port = os.environ.get('postConsumer')
    pollsPort = os.environ.get('pollsAPI')
    domainName = socket.gethostbyname(socket.getfqdn())
    # client = greenstalk.Client((domainName, port))
    client = greenstalk.Client(('127.0.0.1', 8100))

    # extracts url from text of message
    url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message) 
    # url = "http://" + domainName + ":" + str(pollsPort) + "/polls/results:" + str(poll_id)
    poll_id = url[-8:-1]
    errMsg = "Poll: " + poll_id + " Does Not Exist. Poll not linked"

    # Gets count of rows already in table
    for post in posts.query("SELECT P.id FROM posts P"):
        ctr += 1

    # creates new user object with input data
    ctr+=1
    newAsyncPost = json.dumps({
        "id": ctr,
        "author_username": username,
        "message": message,
        "human_timestamp": str(ct),
        "timestamp": ts,
        "origin_URL": None,
        "poll_URL": url
    })

    # --- background process to check if ID is valid ---
    client.put(poll_id) # inserts new job
    # - Process Running -
    job = client.reserve()
    data = job.body # passes in post_id

    url = "http://" + str(domainName) + ":" + str(pollsPort) + "/polls/isValid:" + str(poll_id)
    realID = requests.get(url)

    if realID:
        client.delete(job) # ends jobs process
    else:
        # Call worker program to remove the invalid like and send the user an email
        removePoll(username, poll_id)
        client.delete(job) # ends jobs process
        return {"ERROR": errMsg}
    # --- background process to check if ID is valid ---

    # inserts job inside Message Queue and is passed to postConsumer.py
    client.put(newAsyncPost)

    # For Testing: should be done in postConsumer.py somehow
    # job = client.reserve()
    # data = json.loads(job.body)
    # client.delete(job)
    # client.close()

    # try:
    #     postsArr.insert(data)
    #     newAsyncPost["id"] = postsArr.last_pk
    # except Exception as e:
    #     response.status = hug.falcon.HTTP_409
    #     return {"error": str(e)}
    #     response.set_header("Location", f"/posts/{newPost['id']}")
    return newAsyncPost

# repost functionality
# ISSUE: broken
@hug.post("/posts/{username}/repost/{original_username}&{id}")
def repost(
    username: hug.types.text,
    original_username: hug.types.text,
    id: hug.types.number,
    response,
    db: sqlite
):
    postsArr = db["posts"]
    posts = sqlite_utils.Database("./data/posts.db")
    post = []
    ctr = 0
    ct = datetime.datetime.now()
    ts = ct.timestamp()

    for row in posts.query(
        "SELECT * FROM posts WHERE author_username=:authName AND id=:authId",
        {"authName": original_username, "authId": id}
    ):
        post.append(row)

    message = post['message']   
    origin = 'http://localhost/posts/public?id=' + str(id) 

    # Gets count of rows already in table
    for post in posts.query("SELECT P.id FROM posts P"):
        ctr += 1

    ctr += 1

    # creates a new post object of repost
    newRepost = {
        "id": ctr,
        "author_username": username,
        "message": message,
        "human_timestamp": ct,
        "timestamp": ts,
        "origin_URL": None,
        "poll_URL": None
    }

    try:
        postsArr.insert(newRepost)
        newRepost["id"] = postsArr.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}
        response.set_header("Location", f"/posts/{newRepost['id']}")
    return newRepost

hug.API(__name__).http.serve(port=8100) # Force hug onto port 8000 # TESTING