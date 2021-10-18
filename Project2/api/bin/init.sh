#!/bin/sh

# Create users and posts .db files
cd data
touch users.db
touch posts.db
cd ..

# Initialization scripts for users microservice API

sqlite-utils insert ./data/users.db users --csv ./data/users.csv --detect-types --pk=username
sqlite-utils create-index ./data/users.db users password email_address bio --unique

sqlite-utils insert ./data/users.db following --csv ./data/followers.csv --detect-types --pk=id
sqlite-utils create-index ./data/users.db following follower_username following_username --unique

# Initialization bash script for posts microservice API

sqlite-utils insert ./data/posts.db posts --csv ./data/posts.csv --detect-types --pk=id
sqlite-utils create-index ./data/posts.db posts author_username message human_timestamp timestamp origin_URL --unique
