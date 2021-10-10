# run hug server: hug -f api.py

import configparser
import logging.config

import hug
import sqlite_utils

# Users: 
#   Attributes: usernames, bio, email, password
#   Actions: follow, post messages
# Posts: 
#   Attributes: author username, post message, timestamps
#   Actions: repost -> URL of original post
# Timelines: 
#   Attributes: user (user Posts), home (followed users), public (all users)
#   (Reverse chronological order, newest first)

# Parser configuator function 
#   Code provided by instructor
config = configparser.ConfigParser()
config.read("./configs/userAPI.ini")
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

# sets /users/
@hug.get("/users/")
def users(db: sqlite):
    return {"users": db["users"].rows}

# returns JSON of specific user w/ username : <input username>
@hug.get("/users/{username}")
def getUser(response, username: hug.types.text, db: sqlite):
    try:
        user = db["users"].get(username)
        users.append(user)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"users": user}

# retunrs JSON array of all users
@hug.get("/users/all")
def getAllUsers(response, db: sqlite):
    userArr = [] # JSON array for storing each user object

    try:
        for row in db["users"].rows:
            userArr.append(row)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"users": userArr}