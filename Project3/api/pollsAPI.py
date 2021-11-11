# run hug server: hug -f api.py
# run GET/POST in termial: 
#   http <http method> localhost:8000/posts/newPost username=jackMan etc

# Users can:
#   create polls,
#   vote in polls (only once),
#   view reuslts of a poll

import hug
import boto3

# variable for id of polls
poll_id = 0

# Create a new poll
@hug.post("/polls/{username}/create")
def createNewPoll(
    username: hug.types.text,
    pollQuestion: hug.types.text,
    q1: hug.types.text,
    q2: hug.types.text,
    q3: hug.types.text,
    q4: hug.types.text,
    response,
    dynamoDB = None
):
    # Connect DynamoDB
    if not dynamodb: 
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Polls')
    # creates new poll and inserts into Polls table
        # will return response for success
    response = table.put_item(
        Item = {
            'poll_id': poll_id,
            'createdBy': username,
            'info': {
                'question': pollQuestion,
                'response1': q1,
                'response2': q2,
                'response3': q3,
                'response4': q4
            }
        }
    )
    # increment the poll_id
    poll_id += 1

# Vote in a poll
@hug.post("/polls/{username}/vote/{poll_id}")
def vote(
    username: hug.types.text,
    poll_id: hug.types.text,
    response,
    dynamoDB = None
):
    # Connect DynamoDB
    if not dynamodb: 
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

# Get results of a poll given its ID
@hug.get("/polls/results/{poll_id}")
def getPollResults(
    poll_id: hug.types.text,
    response,
    dynamoDB = None
):
    # Connect DynamoDB
    if not dynamodb: 
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
