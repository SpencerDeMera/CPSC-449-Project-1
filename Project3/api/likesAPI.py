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

redisHost = "localhost"
redisPort = 6379
popularKey = "popPosts"

r = redis.Redis(host = redisHost, port = redisPort, decode_responses=True)

# Like a post
@hug.post("/posts/{username}/like/{post_id}")
def likePost(
    username: hug.types.text,
    post_id: hug.types.text,
    response
):  
    alertMsg = "Post: " + post_id + " Liked By: " + username
    
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

# Get like count of post with ID 'post_id'
@hug.get("/likes/getLikes:{post_id}")
def getLikes(
    post_id: hug.types.text,
    response
):
    # Calls method in postAPI.py to check if post_id is valid
    url = "http://localhost:8000/posts/getPost:" + post_id
    realID = requests.get(url).json()

    # If post_id is valid
    if realID:
        if r.exists(post_id):
            msg = "Post " + post_id
            # JSON serialize to json for output
            return {msg: json.loads(r.get(post_id))}
        else:
            msg = "Post: " + post_id + " Has 0 Likes"
            return {"ALERT": msg}
    else:
        # JSON serialize to json for output
        return {"ERROR": "Invalid Post ID"}

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