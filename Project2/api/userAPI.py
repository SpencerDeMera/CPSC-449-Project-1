# run hug server: hug -f api.py
# run GET/POST in termial: 
#   http <http method> localhost:8000/users/addUser username=jackMan etc
#       *When inputing text with spaces, use '%20' instead of ' ' between words

import configparser
import logging.config

import hug
import sqlite_utils
import urllib.parse

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
    users = [] # JSON for storing all user data (username, password, email, bio)
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

# Create a new user and add to table of users
@hug.post("/users/addUser")
def addUser(
    username: hug.types.text,
    password: hug.types.text,
    email: hug.types.text,
    bio: hug.types.text,
    response,
    db: sqlite,
):
    usersArr = db["users"]
    # unencodes the %20 for spaces from input bio string
    bioUnencoded = urllib.parse.unquote_plus(bio)
    # creates new user object with input data
    newUser = {
        "username": username,
        "password": password,
        "email_address": email,
        "bio": bioUnencoded,
    }

    try:
        usersArr.insert(newUser)
        newUser["username"] = usersArr.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    response.set_header("Location", f"/users/{newUser['username']}")
    return newUser

# Update a users password given their username & current password
# TODO
@hug.put("/users/updatePass")
def updatePass(
    username: hug.types.text,
    password: hug.types.text,
    newPassword: hug.types.text,
):
    userArr = [] # JSON array for storing each user object
    try:
        user = db["users"].get(username)
        if user.password == password:
            user.password = newPassword
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"users": userArr}