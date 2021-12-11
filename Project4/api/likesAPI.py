# run hug server: hug -f api.py
# run GET/POST in termial: 
#   http <http method> localhost:8000/posts/newPost username=jackMan etc

# Users can:
#   Like posts, 
#   get number of likes a post has, 
#   get all posts liked by a user, 
#   get all the posts ranked by popularity

import hug
import redis
import json
import requests
import os
import socket
import time
from dotenv import load_dotenv
import greenstalk
from likesWorker import removeLike

redisHost = "localhost"
redisPort = 6379
popularKey = "popPosts"

r = redis.Redis(host = redisHost, port = redisPort, decode_responses=True)

# Startup function
@hug.startup()
def startup(self):
    time.sleep(10)
    load_dotenv()
    port = os.environ.get('likesAPI')
    srvcPort = os.environ.get('srvcRegAPI')
    domainName = socket.gethostbyname(socket.getfqdn())
    pload = {'name': 'likes', 'domainName': domainName, 'port': port}
    r = requests.post(domainName + ":" + srvcPort + "/register", data=pload)

# Health check function
@hug.get("/health")
def healthy(response):
    return {"Likes Health Check": "Done"}

# Like a post
@hug.post("/posts/{username}/like/{post_id}")
def likePost(
    username: hug.types.text,
    post_id: hug.types.text,
    response
):  
    alertMsg = "Post: " + post_id + " Liked By: " + username
    errMsg = "Post: " + post_id + " Does Not Exist. Post not Liked"
    port = os.environ.get('postAPI')
    domainName = socket.gethostbyname(socket.getfqdn())
    # connect greenstalk client
    client = greenstalk.Client(('127.0.0.1', 8000))

    # If post already has a like
    if r.exists(post_id) and not r.sismember(username, post_id): 
        likesCtr = json.loads(r.get(post_id))['likes'] + 1

        newLike = {
            "likes": likesCtr 
        }
        # Converts dict to string and sets it as 'value' of key 'test' in a Redis String
        r.set(post_id, json.dumps(newLike))
        # Add post to set of posts liked by user
        r.sadd(username, post_id)
        r.zadd(popularKey, {post_id: likesCtr})
        return {"ALERT": alertMsg}
    # User has already liked this post
    elif r.exists(post_id) and r.sismember(username, post_id):
        return {"ERROR": "You Already Liked This Post"}
    # Post has not been liked by anyone
    else:
        newLike = {
            "likes": 1
        }
        # Converts dict to string and sets it as 'value' of key 'test' in a Redis String
        r.set(post_id, json.dumps(newLike))
        r.sadd(username, post_id)
        likes = 1
        r.zadd(popularKey, {post_id: likes})
        # Converts from string dict to dict and returns as JSON
        return {"ALERT": alertMsg}

    # --- background process to check if ID is valid ---
    client.put(post_id) # inserts new job
    # - Process Running -
    job = client.reserve()
    data = job.body # passes in post_id

    url = "http://" + str(domainName) + ":" + str(port) + "/posts/isValid:" + str(post_id)
    realID = requests.get(url).json()

    if realID:
        client.delete(job) # ends jobs process
    else:
        # Call worker program to remove the invalid like and send the user an email
        removeLike(username, post_id)
        client.delete(job) # ends jobs process
        return {"ERROR": errMsg} 
    client.close()
    # --- background process to check if ID is valid ---

# Get like count of post with ID 'post_id'
@hug.get("/likes/getLikes:{post_id}")
def getLikes(
    post_id: hug.types.text,
    response
):
    if r.exists(post_id):
        msg = "Post " + post_id
        # JSON serialize to json for output
        return {msg: json.loads(r.get(post_id))}
    else:
        msg = "Post: " + post_id + " Has 0 Likes"
        return {"ALERT": msg}

# Get IDs of all posts liked by user
@hug.get("/likes/{username}")
def getLiked( 
    username: hug.types.text, 
    response
):
    msg = "All Posts Liked By " + username
    likedPostsArr = []
    
    # Gets set of all post IDs liked by user
    mems = r.smembers(username)
    for obj in mems:
        idMsg = "PostID: " + obj
        likedPostsArr.append(idMsg)

    # JSON serialize to json for output
    return {msg: likedPostsArr}

# Get IDs of all popular posts in ASC order
@hug.get("/posts/popular")
def getPopularPosts(response):
    msg = "Popular Posts"
    popPostsArr = []

    # Gets list of all strings set sorted in DESC order
    posts = r.zrange(popularKey, 0, -1, desc=True, withscores=True)
    # For each Redis string in set, separate like count and post_id
    for obj in posts:
        post = {
            "Post ID": obj[0],
            "Number of Likes": obj[1]
        }
        popPostsArr.append(post)

    # JSON serialize to json for output
    return {msg: popPostsArr}
