import hug
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

