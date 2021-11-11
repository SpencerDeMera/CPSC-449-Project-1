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
    r1: hug.types.text,
    r2: hug.types.text,
    r3: hug.types.text,
    r4: hug.types.text,
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
            'poll_data': {
                'question': pollQuestion,
                'response1': r1,
                'resp1Votes': 0,
                'response2': r2,
                'resp2Votes': 0,
                'response3': r3,
                'resp3Votes': 0,
                'response4': r4,
                'resp4Votes': 0,
            },
            'voted': []
        }
    )
    # increment the poll_id
    poll_id += 1

    return {"New Poll": Item}

# Vote in a poll
@hug.post("/polls/{username}/vote/{poll_id}:{respNum}")
def vote(
    username: hug.types.text,
    poll_id: hug.types.text,
    respNum: hug.types.text,
    response,
    dynamoDB = None
):
    voteCount = 0

    # Connect DynamoDB
    if not dynamodb: 
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Polls')

    try:
        response1 = table.get_item(
            Key = {'poll_id': poll_id, 'createdBy': username}
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        # Checks if a user already voted in this poll
        for user in response1['Item']['voted']:
            if username == user:
                return {'ERROR': 'You Already Voted in This Poll'}

        if respNum == 1:
            voteCount = int(response1['Item']['poll_data']['resp1Votes'])
        elif respNum == 2:
            voteCount = int(response1['Item']['poll_data']['resp2Votes'])
        elif respNum == 3:
            voteCount = int(response1['Item']['poll_data']['resp3Votes'])
        elif respNum == 4:
            voteCount = int(response1['Item']['poll_data']['resp4Votes'])
        else:
            return {'ERROR': 'Not a Valid Response Number'}

    voteCount += 1

    if respNum == 1:
        response2 = table.update_item(
            Key = { 'poll_id': poll_id, 'createdBy': username },
            UpdateExpression = "set poll_data.resp1Votes=:v",
            ExpressionAttributes = { ':v': int(voteCount) },
            ReturnValues = "UPDATED_NEW"
        )
    elif respNum == 2:
        response2 = table.update_item(
            Key = { 'poll_id': poll_id, 'createdBy': username },
            UpdateExpression = "set poll_data.resp2Votes=:v",
            ExpressionAttributes = { ':v': int(voteCount) },
            ReturnValues = "UPDATED_NEW"
        )
    elif respNum == 3:
        response2 = table.update_item(
            Key = { 'poll_id': poll_id, 'createdBy': username },
            UpdateExpression = "set poll_data.resp3Votes=:v",
            ExpressionAttributes = { ':v': int(voteCount) },
            ReturnValues = "UPDATED_NEW"
        )
    elif respNum == 4:
        response2 = table.update_item(
            Key = { 'poll_id': poll_id, 'createdBy': username },
            UpdateExpression = "set poll_data.resp4Votes=:v",
            ExpressionAttributes = { ':v': int(voteCount) },
            ReturnValues = "UPDATED_NEW"
        )

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

    table = dynamodb.Table('Polls')

    try:
        response1 = table.get_item(
            Key = {'poll_id': poll_id, 'createdBy': username}
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return {'Poll': response1}
