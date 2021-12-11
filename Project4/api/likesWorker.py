import redis
import json
import requests
import os
import socket
import time
from dotenv import load_dotenv
import greenstalk

redisHost = "localhost"
redisPort = 6379
popularKey = "popPosts"

r = redis.Redis(host = redisHost, port = redisPort, decode_responses=True)

def removeLike(username, like_id):
    r.srem(username, like_id)
    r.zrem(popularKey, like_id)
    # Call Email File
    return True