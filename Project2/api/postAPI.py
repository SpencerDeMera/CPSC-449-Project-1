# run hug server: hug -f api.py
# run GET/POST in termial: 
#   http <http method> localhost:8000/posts/addPost username=jackMan etc
#       *When inputing text with spaces, use '%20' instead of ' ' between words

import configparser
import logging.config

import hug
import sqlite_utils

import requests

# Users: 
#   Attributes: usernames, bio, email, password
#   Actions: follow, post messages
# Posts: 
#   Attributes: author_username, message, human_timestamp, timestamp, origin_URL
#   Actions: repost -> URL of original post
# Timelines: 
#   Attributes: user (user Posts), home (followed users), public (all users)
#   (Reverse chronological order, newest first)

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

# User Timeline
@hug.get("/{username}/user")
def getUserTimeline(response, username: hug.types.text, db: sqlite):
    postArr = [] # JSON array for storing all post objects of the given user
    try:
        posts = sqlite_utils.Database("./data/posts.db")
        for row in posts.query(
            "SELECT * FROM posts WHERE author_username=?", (username,)
        ):
            postArr.append(row)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": postArr}

# Home Timeline
@hug.get("/{username}/home")
def getHomeTimeline(response, username: hug.types.text, db: sqlite):
    postArr = [] # JSON array for storing all post objects of the given followers user
    try:
        posts = sqlite_utils.Database("./data/posts.db")
        for row in posts.query(
            "SELECT * FROM posts WHERE author_username=?", (username,)
        ):
            postArr.append(row)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": postArr}

# Public Timeline
@hug.get("/public")
def getPublicTimeline(response, db: sqlite):
    postArr = [] # JSON array for storing each post object
    try:
        for row in db["posts"].rows:
            postArr.append(row)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": postArr}