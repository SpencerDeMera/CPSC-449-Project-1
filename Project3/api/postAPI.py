# run hug server: hug -f api.py
# run GET/POST in termial: 
#   http <http method> localhost:8000/posts/addPost username=jackMan etc
#       *When inputing text with spaces, use '%20' instead of ' ' between words

import configparser
import logging.config
import hug
import sqlite_utils
import requests
import datetime
from userAPI import userAuth

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
        url = "http://localhost:8000/users/" + str(username) + "/getFollowing"
        
        followingUsers  = requests.get(url).json()
        
        # get all posts in DESC order according to timestamp
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

    # creates new user object with input data
    ctr+=1
    newPost = {
        "id": ctr,
        "author_username": username,
        "message": message,
        "human_timestamp": ct,
        "timestamp": ts,
        "origin_URL": None
    }

    try:
        postsArr.insert(newPost)
        newPost["id"] = postsArr.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}
        response.set_header("Location", f"/posts/{newPost['id']}")
    return newPost

# repost functionality
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
        "origin_URL": origin
    }

    try:
        postsArr.insert(newRepost)
        newRepost["id"] = postsArr.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}
        response.set_header("Location", f"/posts/{newRepost['id']}")
    return newRepost
