# run hug server: hug -f api.py
# run GET/POST in termial: 
#   http <http method> localhost:8000/posts/addPost username=jackMan etc
#       *When inputing text with spaces, use '%20' instead of ' ' between words

import hug
import redis

redisHost = "localhost"
redisPort = 6379
redisPass = ""

r = redis.StrictRedis(host = redisHost, port = redisPort, db = 0)
print(r.set('foo', 'bar'))
print(r.get('foo'))