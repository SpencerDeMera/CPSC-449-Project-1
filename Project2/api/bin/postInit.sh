#!/bin/sh
# Initialization bash file for posts microservice API

sqlite-utils insert ./data/posts.db posts --csv ./data/posts.csv --detect-types --pk=author_username
sqlite-utils create-index ./data/posts.db posts message human_timestamp timestamp origin_URL --unique