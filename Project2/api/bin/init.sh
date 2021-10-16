#!/bin/sh
# Initialization bash file for posts microservice API

cd data
touch users.db
touch posts.db
cd ..

sqlite-utils insert ./data/users.db users --csv ./data/users.csv --detect-types --pk=username
sqlite-utils create-index ./data/users.db users password email_address bio --unique

sqlite-utils insert ./data/users.db following --csv ./data/followers.csv --detect-types --pk=follower_username
sqlite-utils create-index ./data/users.db following following_username --unique

sqlite-utils insert ./data/posts.db posts --csv ./data/posts.csv --detect-types --pk=author_username
sqlite-utils create-index ./data/posts.db posts message human_timestamp timestamp origin_URL --unique