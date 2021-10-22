# CPSC 449 Project-2
## Spencer DeMera & Ricardo Segarra

## Project Description:


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

`$ sudo apt update`
`$ sudo apt install --yes python3-pip ruby-foreman httpie sqlite3`
`$ python3 -m pip install hug sqlite-utils`
`$ sudo apt install --yes haproxy gunicorn`

## Running


## Errors & Bugs

