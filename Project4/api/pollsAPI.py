# run hug server: hug -f api.py
# run GET/POST in termial: 
#   http <http method> localhost:8000/posts/newPost username=jackMan etc

# Users can:
#   create polls,
#   vote in polls (only once),
#   view reuslts of a poll

import hug
import boto3
from boto3.dynamodb.conditions import Key
import json
import string
import random
import os
import socket
import time
from dotenv import load_dotenv
import requests

dynamodb = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

# Startup function
@hug.startup()
def startup(self):
    time.sleep(10)
    load_dotenv()
    port = os.environ.get('pollsAPI')
    srvcPort = os.environ.get('srvcRegAPI')
    domainName = socket.gethostbyname(socket.getfqdn())
    pload = {'name': 'polls', 'domainName': domainName, 'port': port}
    r = requests.post(domainName + ":" + srvcPort + "/register", data=pload)

# Health check function
@hug.get("/health")
def healthy(response):
    return {"Polls Health Check": "Done"}

# Create a new poll
@hug.post("/polls/{username}/create")
def createNewPoll(
    username: hug.types.text,
    pollQuestion: hug.types.text,
    r1: hug.types.text,
    r2: hug.types.text,
    r3: hug.types.text,
    r4: hug.types.text,
    response,
    dynamodb=None
):
    initVal = '0'
    # Connect DynamoDB
    if not dynamodb: 
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Polls')

    pollID = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
    pollID_num = str(pollID)

    response = table.put_item(
        Item = {
            'poll_id': pollID_num,
            'createdBy': username,
            'poll_data': {
                'question': pollQuestion,
                'response1': r1,
                'resp1Votes': initVal,
                'response2': r2,
                'resp2Votes': initVal,
                'response3': r3,
                'resp3Votes': initVal,
                'response4': r4,
                'resp4Votes': initVal,
            },
            'voted': []
        }
    )

    msg = "-- New Poll Created | Poll ID: " + str(pollID_num) + " --"
    return {'Message': msg}

# Vote in a poll
@hug.post("/polls/{username}/vote/{poll_id}:{respNum}")
def vote(
    username: hug.types.text,
    poll_id: hug.types.text,
    respNum: hug.types.number,
    response,
    dynamodb=None
):
    voteCount = 0
    votedArr = []

    # Connect DynamoDB
    if not dynamodb: 
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Polls')

    response1 = table.query(
        KeyConditionExpression = Key('poll_id').eq(str(poll_id))
    )
    data = json.dumps(response1['Items'])
    jsonData = json.loads(data)
    temp = jsonData[0]['poll_data']
    temp2 = jsonData[0]['voted']
    created = jsonData[0]['createdBy']

    if respNum == 1:
        voteCount = int(temp.get('resp1Votes'))
    elif respNum == 2:
        voteCount = int(temp.get('resp2Votes'))
    elif respNum == 3:
        voteCount = int(temp.get('resp3Votes'))
    elif respNum == 4:
        voteCount = int(temp.get('resp4Votes'))
    else:
        return {'ERROR': 'Not a Valid Response Number'}

    # if voteCount != 0:
    for user in temp2:
        if username == user:
            votedArr.clear()
            return {'ALERT': 'You Already Voted in This Poll'}
        else:
            votedArr.append(str(user))
    # append username to end of voted array
    votedArr.append(str(username))

    # increment vote count
    voteCount += 1

    if respNum == 1:
        table.update_item(
            Key = {
                'poll_id': str(poll_id), 
                'createdBy': str(created) 
            },
            UpdateExpression = "SET #attrName=:s, voted=:n",
            ExpressionAttributeNames = {
                '#attrName': 'poll_data'
            },
            ExpressionAttributeValues = {
                ':s': {
                    'question': str(temp.get('question')),
                    'response1': str(temp.get('response1')),
                    'resp1Votes': str(voteCount),
                    'response2': str(temp.get('response2')),
                    'resp2Votes': str(temp.get('resp2Votes')),
                    'response3': str(temp.get('response3')),
                    'resp3Votes': str(temp.get('resp3Votes')),
                    'response4': str(temp.get('response4')),
                    'resp4Votes': str(temp.get('resp4Votes')),
                },
                ':n': votedArr
            }
        )
    elif respNum == 2:
        table.update_item(
            Key = {
                'poll_id': str(poll_id), 
                'createdBy': str(created) 
            },
            UpdateExpression = "SET #attrName=:s, voted=:n",
            ExpressionAttributeNames = {
                '#attrName': 'poll_data'
            },
            ExpressionAttributeValues = {
                ':s': {
                    'question': str(temp.get('question')),
                    'response1': str(temp.get('response1')),
                    'resp1Votes': str(temp.get('resp1Votes')),
                    'response2': str(temp.get('response2')),
                    'resp2Votes': str(voteCount),
                    'response3': str(temp.get('response3')),
                    'resp3Votes': str(temp.get('resp3Votes')),
                    'response4': str(temp.get('response4')),
                    'resp4Votes': str(temp.get('resp4Votes')),
                },
                ':n': votedArr
            }
        )
    elif respNum == 3:
        table.update_item(
            Key = {
                'poll_id': str(poll_id), 
                'createdBy': str(created) 
            },
            UpdateExpression = "SET #attrName=:s, voted=:n",
            ExpressionAttributeNames = {
                '#attrName': 'poll_data'
            },
            ExpressionAttributeValues = {
                ':s': {
                    'question': str(temp.get('question')),
                    'response1': str(temp.get('response1')),
                    'resp1Votes': str(temp.get('resp1Votes')),
                    'response2': str(temp.get('response2')),
                    'resp2Votes': str(temp.get('resp2Votes')),
                    'response3': str(temp.get('response3')),
                    'resp3Votes': str(voteCount),
                    'response4': str(temp.get('response4')),
                    'resp4Votes': str(temp.get('resp4Votes')),
                },
                ':n': votedArr
            }
        )
    elif respNum == 4:
        table.update_item(
            Key = {
                'poll_id': str(poll_id), 
                'createdBy': str(created) 
            },
            UpdateExpression = "SET #attrName=:s, voted=:n",
            ExpressionAttributeNames = {
                '#attrName': 'poll_data'
            },
            ExpressionAttributeValues = {
                ':s': {
                    'question': str(temp.get('question')),
                    'response1': str(temp.get('response1')),
                    'resp1Votes': str(temp.get('resp1Votes')),
                    'response2': str(temp.get('response2')),
                    'resp2Votes': str(temp.get('resp2Votes')),
                    'response3': str(temp.get('response3')),
                    'resp3Votes': str(temp.get('resp3Votes')),
                    'response4': str(temp.get('response4')),
                    'resp4Votes': str(voteCount),
                },
                ':n': votedArr
            }
        )
    
    return {'ALERT': str(username) + ' Voted in poll: ' + str(poll_id)}

# Get results of a poll given its ID
@hug.get("/polls/results:{poll_id}")
def getPollResults(
    poll_id: hug.types.text,
    response,
    dynamodb=None
):
    # Connect DynamoDB
    if not dynamodb: 
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Polls')

    response = table.query(
        KeyConditionExpression = Key('poll_id').eq(str(poll_id))
    )
    data = json.dumps(response['Items'])
    jsonData = json.loads(data)

    return jsonData

# endpoint for checking if post is valid
@hug.get("/polls/isValid:{poll_id}")
def isValid(
    poll_id: hug.types.text,
    response,
    dynamodb=None
):
    # Connect DynamoDB
    if not dynamodb: 
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Polls')

    response = table.query(
        KeyConditionExpression = Key('poll_id').eq(str(poll_id))
    )
    data = json.dumps(response['Items'])
    # If post with poll_id is real 
    if data != None:
        return True
    else:
        return False