import hug
import redis
import json
import requests
import os
import socket
import time
from dotenv import load_dotenv
import greenstalk
from email import email_notify

redisHost = "localhost"
redisPort = 6379
popularKey = "popPosts"

r = redis.Redis(host = redisHost, port = redisPort, decode_responses=True)

def removeLike(username, post_id):
    if r.exists(post_id) and r.sismember(username, post_id):
        return {"ERROR": "You Already Liked This Post"}
        r.srem(username, post_id)
        r.zrem(popularKey, post_id)
    else:
        r.srem(username, post_id)
        r.zrem(popularKey, post_id)

    email_notify(username, post_id)
    return True