# CPSC 449 Project-2
## Spencer DeMera & Ricardo Segarra

## Project Description:
This project uses a variety of tools and services to power two RESTful back-end services that facilitate user interaction and communication via digital blogging. Users can view three different timelines, follow other users, create new posts, users can be added, and repost other posts. 

## Contents:
* File README.md. README file for the project.
* FOLDER api. Folder that contains all api files.
    * FILE Procfile. Procfile for foreman service definitions.
    * FILE .env. Env file for avoiding missing input.
    * FILES userAPI.py & postAPI.py. User and Post API files.
    * FILES data/users.csv, data/followers.csv & data/posts.csv. CSV schema files for each database.
    * FOLDER log. Log folder to contain api.log files.
    * FILES bin/init.sh & bin/foreman.sh. Initilization scripts for database schemas and foreman start.
    * FILES configs/userAPI.ini & postAPI.ini. Initilization files for SQLite DBs.
    * FILE configs/logging.ini. Initilization file for SQLite logging and configs.

## Installation
Use the following to setup your environment:

```shell
$ sudo apt update                                                    # Update system
$ sudo apt install --yes python3-pip ruby-foreman httpie sqlite3     # Install package and tool installers
$ python3 -m pip install hug sqlite-utils                            # Install hug and Python sqlite-utils libraries
# Log out then back in to ensure all PATH changes are established
$ sudo apt install --yes haproxy gunicorn                            # Install production tools

# Install reids and DyanmoDB data stores
# Redis
$ sudo apt install --yes redis                                      # Install Redis
$ redis-cli ping                                                    # Verify that Redis is running w/ response 'PONG'
$ sudo apt install --yes python3-hiredis                            # Install redis-py library and Hiredis parser
# Some python3 instances won't install redis-py with the above command, must use below \/
$ python3 -m pip install redis                                      # Alt. install for python3 install failure
# DynamoDB
$ sudo apt install --yes awscli                                     # Install the AWS CLI 
$ aws configure                                                     # Configure the AWS instance w/ necessary parameters
$ sudo apt install --yes python3-boto3                              # Install Boto3 python library

# Run the following to initialize the databases and start the APIs
$ cd api
$ ./bin/init.sh                                                      # Creates and initalizes user and post db files and tables
$ ./bin/foreman.sh                                                   # Starts the foreman and HAProxy api services
```

## Running
* GET can be run in terminal or browser address bar
* POST must be run inside a terminal only

 API Call                                   | Route                                                     | Action
--------------------------------------------|-----------------------------------------------------------|-------------------------------------------------------
`addUser(username, password, email, bio)`   | `POST /users/addUser`                                     | Adds a new user to database
`followUser(username, following_username)`  | `POST /users/<username>/followUser/<following_username>`  | Follow a new user
`getFollowing(username)`                    | `GET /users/<username>/getFollowing`                      | Get all usernames followed by given user
`getUserTimeline(username)`                 | `GET /posts/<username>/user`                              | Get timeline of all posts made by user
`getHomeTimeline(username)`                 | `GET /posts/<username>/home`                              | Get timeline of all posts by user and users followed
`getPublicTimeline()`                       | `GET /posts/public`                                       | Get timeline of all posts of every user
`newPost(author_username, message)`         | `POST /posts/<author_username>/newPost`                   | Add a new post
`repost(username,original_username,id)`     | `POST /posts/<username>/repost<author_username>&<id>`     | Repost a post from another users

## Issues & Incomplete Functionalities
* Issues
    * Number in place of `username` value on JSON output after new user is created
        * addUser will output JSON with the number of users instead of username in `username` when displayed after run
        * The actual new user object created by addUser will actually have the created username value in `username`
            * Not sure what is causing said issue, insufficent time to resolve issue
* Incomplete functions
    * Repost code is fully implemented but the server throws HTTP 405 upon POST request
        * Insufficient time to resolve issue

## Credits
* Some code and methodology was provided by instructor Kenytt Avery
    * Provided code will be marked with denoting comments
* This project makes use of these libraries & tutorial sources
    * [hug start guide](http://www.hug.rest/)
    * [HTTPie documentation / start guide](https://opensource.com/article/19/8/getting-started-httpie)
    * [foreman documentation / start guide](http://blog.daviddollar.org/2011/05/06/introducing-foreman.html)
    * [sqlite-utils documentation / start guide](https://simonwillison.net/2019/Feb/25/sqlite-utils/)
    * [guinicorn](https://gunicorn.org/)
    * [HAProxy documentation](https://www.haproxy.org/)
    * [Python Requests library](https://docs.python-requests.org/en/latest/)
