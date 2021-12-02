# CPSC 449 Project-4
## Spencer DeMera & Ricardo Segarra

## [Project 4 GitHub](https://github.com/SpencerDeMera/CPSC-449-Projects/tree/main/Project4)

## Project Description:
This project uses a variety of tools and services to power two RESTful back-end services that facilitate user interaction and communication via digital blogging. Users can view three different timelines, follow other users, create new posts, users can be added, and repost other posts. Additionally, users can now like posts and conduct polls while being able to view the results/metadata of both.

## Contents:
* File README.md. README file for the project.
* FOLDER api. Folder that contains all api files.
    * FILE Procfile. Procfile for foreman service definitions.
    * FILE .env. Env file for avoiding missing input.
    * FILE haproxy.cfg. HAProxy configuration file.
    * FILES userAPI.py & postAPI.py. User and Post API files.
    * FILES likesAPI.py, pollsAPI.py, & srvcRegAPI.py. Files for likes, polls, and servce registry microservices
    * FILES data/users.csv, data/followers.csv & data/posts.csv. CSV schema files for each database.
    * FOLDER log. Log folder to contain api.log files.
    * FILES bin/init.sh, bin/foreman.sh & dataStores.sh. Initilization scripts for database schemas, foreman start and NoSQL data stores.
    * FILE bin/initPolls.py. Initilization scripts for polls service DynamoDB datastore.
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
$ python3 -m pip install pyhton-dotenv                               # Installs tool for reading environment variables

# Install reids and DyanmoDB data stores
# Redis
$ sudo apt install --yes redis                                      # Install Redis
$ redis-cli ping                                                    # Verify that Redis is running w/ response 'PONG'
$ sudo apt install --yes python3-hiredis                            # Install redis-py library and Hiredis parser
# Some python3 instances won't install redis-py with the above command, must use below \/
$ python3 -m pip install redis                                      # Alt. install for python3 install failure
# DynamoDB
# Use the following commands
$ sudo apt install --yes awscli                                     # Install the AWS CLI parameters
```
* Follow the instructions at [DynamoDB Local Install Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html).
* WARNING: Make sure to install the DynamoDB file in Step #1 OUTSIDE of the project directory (outside of Project3 Folder Directory)
```shell
# STEP #3
# Open a new, additional, terminal window in the directory of your extracted dynamodb_local_latest folder 
$ cd dynamodb_local_latest
$ java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
# leave this running in this terminal window. Return to other window for step #4
# STEP #4
# Configure with:
$ aws configure                                                     # Configure the AWS instance w/ necessary 
AWS Access Key ID [None]: fakeMyKeyId
AWS Secret Access Key [None]: fakeSecretAccessKey
Default region name [None]: us-west-2
Default output format [None]: table
# After step #5 of the above guide & confirmation of DynamoDB working
$ sudo apt install --yes python3-boto3                              # Install Boto3 python library
# Some python3 instances won't install boto3 with the above command, must use below \/
$ pip install boto3                                                 # Alt. install for DynamoDB boto3 python3 install failure

# Install Beanstalkd and Greenstalk Python client libraries
$ sudo apt install --yes beanstalkd                                 # Install beanstalked 
$ python3 -m pip install greenstalk                                 # Install greenstalk python library
```
* Initializing DB schemas and starting server instances
```shell
# Run the following to initialize the databases and start the APIs
$ cd api
$ ./bin/init.sh                                                      # Creates and initalizes user and post db files and tables
$ ./bin/foreman.sh                                                   # Starts the foreman and HAProxy api services

# Start the data stores files
$ redis-server                                                       # Starts the redis server
$ cd bin
$ python3 initPolls.py                                               # Initialize the Polls table & create a default poll
$ cd ..                                                                # Gets you back to the api directory
```

## Running
* GET can be run in terminal or browser address bar
* POST must be run inside a terminal only

 API Call                                   | Route                                                     | Action
--------------------------------------------|-----------------------------------------------------------|-------------------------------------------------------
`startup(self)`                             | `STARTUP`                                                 | Runs on startup to register the service (One for each service)
`healthy()`                                 | `GET /health`                                             | Function for service registry health check (One for each service)
`addUser(username, password, email, bio)`   | `POST /users/addUser`                                     | Adds a new user to database
`followUser(username, following_username)`  | `POST /users/<username>/followUser/<following_username>`  | Follow a new user
`getFollowing(username)`                    | `GET /users/<username>/getFollowing`                      | Get all usernames followed by given user
`getUserTimeline(username)`                 | `GET /posts/<username>/user`                              | Get timeline of all posts made by user
`getHomeTimeline(username)`                 | `GET /posts/<username>/home`                              | Get timeline of all posts by user and users followed
`getPublicTimeline()`                       | `GET /posts/public`                                       | Get timeline of all posts of every user
`newPost(author_username, message)`         | `POST /posts/<author_username>/newPost`                   | Add a new post
`repost(username,original_username,id)`     | `POST /posts/<username>/repost<author_username>&<id>`     | Repost a post from another users
`likePost(username, post_id)`               | `POST /posts/<username>/like/<post_id>`                   | Like a post given its ID
`getLikes(post_id)`                         | `GET /likes/getLikes:<post_id>`                           | Number of likes post has given its ID
`getLiked(username)`                        | `GET /likes/<username>`                                   | Get list of posts liked by a user
`getPopularPosts()`                         | `GET /posts/popular`                                      | Get list of liked posts ordered by number of likes
`createNewPoll(username, question, resps.)` | `POST /polls/<username>/create`                           | Creates a new poll given username, question, and responses
`vote(username, poll_id, respNum)`          | `POST /polls/<username>/vote/<poll_id>:<respNum>`         | Adds vote to response respNum & tracks who has voted 
`getPollResults(poll_id)`                   | `GET /polls/results:<poll_id>`                            | Gets the results of a poll given its ID
`healthCheck()`                             |                                                           | Function for healthchecks
`daemon_function(name)`                     |                                                           | Function for daemon thread function calling
`main(self)`                                | `STARTUP`                                                 | Main function for service registry
`registry(name, domainName, port)`          | `POST /register`                                         | Function for registering microservices

## Resolved Issues
* Notable bug fixes
    * Fixed issue where userAPI.py fails to launch in Project3
        * Line 140 of userAPI.py had an unremoved devlopment testing line that hardcoded the PORT
        * May also be related to why HAProxy failed to proxy user service in Project2 and Project3
    * Fixed issue where db schemas failed to be properly created and initalized
        * Caused by additional `cd ..` on line 4 of init.sh file
    * Fixed issue where getLikes(post_id) fails in Project3
        * getLikes called phantom function in postAPI.py for post_id verification that no longer existed

## Issues & Incomplete Functionalities
* Issues
    * Number in place of `username` value on JSON output after new user is created
        * addUser will output JSON with the number of users instead of username in `username` when displayed after run
        * The actual new user object created by addUser will actually have the created username value in `username`
            * Not sure what is causing said issue, insufficent time to resolve issue
    * Foreman is non-operable on both our WSL & Tuffix installations regardless of restarts OR reinstalls
        * All components work separately and together when using `hug -f <filename>` commands
            * There is no guarentee that all will work with foreman together unfortunately
            * Insufficient information available & time to complete
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
    * [Redis](https://redis.io/)
    * [Redis-py](https://pypi.org/project/redis/)
    * [Hiredis Parser](https://github.com/redis/hiredis)
    * [Redis-py Commands](https://github.com/redis/redis-py/blob/master/redis/commands/core.py)
    * [DynamoDB Deployment](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html)
    * [DynamoDB Usage](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html)
    * [Boto3 Library](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
    * [Hug Decorators for Service Registries](https://hugapi.github.io/hug/reference/hug/decorators/)
    * [Service Registry Pattern](https://microservices.io/patterns/service-registry.html)
    * [Creating Microservices Registrys](https://dzone.com/articles/creating-a-microservices-registry)
    * [Threading in Python](https://realpython.com/intro-to-python-threading/)
    * [Pyhton OS Functions](https://docs.python.org/3/library/os.html#os.environ)
    * [Python dotenv](https://pypi.org/project/python-dotenv/)
    * [Python Healthchecks Examples](https://pypi.org/project/healthcheck-python/)
