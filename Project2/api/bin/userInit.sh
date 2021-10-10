#!/bin/sh
# Initialization bash file for users microservice API

sqlite-utils insert ./data/users.db users --csv ./data/users.csv --detect-types --pk=username
sqlite-utils create-index ./data/users.db users password email_address bio --unique