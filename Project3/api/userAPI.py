# run hug server: hug -f api.py
# run GET/POST in termial: 
#   http <http method> localhost:8000/users/newPost username=jackMan etc

import configparser
import logging.config
import hug
import sqlite_utils
import urllib.parse
import os
import socket
from dotenv import load_dotenv

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

def userAuth(username, password):
    users = sqlite_utils.Database("./data/users.db")
    for row in users.query(
        "SELECT * from users WHERE username=:user AND password=:pass",
        {"user": username, "pass": password}
    ):
        if row['password'] == password:
            return True
        else:
            return False

# Startup function
@hug.startup()
def startup(self):
    print("Starting USERS Service...")
    load_dotenv()
    port = os.environ.get('userAPI')
    domainName = socket.getfqdn()
    print("PORT: " + str(port) + " && FQDN: " + domainName)

# Health check function
@hug.get("/posts/health")
def healthy(response):
    return {"Users Health Check": "Done"}

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

@hug.post("/users/{username}/followUser/{following_username}")
def followUser(
    username: hug.types.text,
    following_username: hug.types.text,
    response,
    db: sqlite
):  
    followerArr = db["following"]
    followers = sqlite_utils.Database("./data/users.db")
    ctr = 0

    # Gets count of rows already in table
    for user in followers.query("SELECT F.id FROM following F"):
        ctr += 1

    newFollower = {
        "id": ctr,
        "follower_username": username,
        "following_username": following_username
    }

    try:
        followerArr.insert(newFollower)
        newFollower["id"] = followerArr.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}
        response.set_header("Location", f"/following/{newFollower['id']}")
    return newFollower

@hug.get("/users/{username}/getFollowing")
def getFollowing(
    username: hug.types.text,
    response,
    db: sqlite
):
    followingUsers = []
    try:
        users = sqlite_utils.Database("./data/users.db")
        for user in users.query(
            "SELECT F.following_username FROM following F WHERE F.follower_username=:userAuth", 
            {"userAuth": username}
        ):
            followingUsers.append(user)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return followingUsers
