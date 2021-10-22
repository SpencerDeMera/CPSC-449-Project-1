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
    * FILES bin/init.sh. Initilization scripts for database schemas.
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

# Run the following to initialize the databases and start the APIs
$ cd api
$ ./bin/init.sh                                                      # Creates and initalizes user and post db files and tables
$ ./bin/foreman.sh                                                   # Starts the foreman api service
```

## Running

 API Call                                   | Route                                                     |
--------------------------------------------|-----------------------------------------------------------|
`getUser(username)`                         | `GET /users/<username>`                                   |
`getAllUsers()`                             | `GET /users/all`                                          |
`addUser(username, password, email, bio)`   | `POST /users/addUser`                                     |
`followUser(username, following_username)`  | `POST /users/<username>/followUser/<following_username>`  |
`getFollowing(username)`                    | `GET /users/<username>/getFollowing`                      |
`getUserTimeline(username)`                 | `GET /posts/<username>/user`                              |
`getHomeTimeline(username)`                 | `GET /posts/<username>/home`                              |
`getPublicTimeline()`                       | `GET /posts/public`                                       |
`newPost(author_username, message)`         | `POST /posts/<author_username>/newPost`                   |

## Issues & Incomplete Functionalities


## Credits
* Some code and methodology was provided by instructor Kenytt Avery
    * Provided code will be marked with denoting comments

* This project makes use of these libraries & tutorial sources
    * hug start guide : http://www.hug.rest/
    * HTTPie documentation / start guide : https://opensource.com/article/19/8/getting-started-httpie
    * foreman documentation / start guide : http://blog.daviddollar.org/2011/05/06/introducing-foreman.html
    * sqlite-utils documentation / start guide : https://simonwillison.net/2019/Feb/25/sqlite-utils/
    * guinicorn : https://gunicorn.org/
    * HAProxy documentation : https://www.haproxy.org/
    * Python Requests library : https://docs.python-requests.org/en/latest/

