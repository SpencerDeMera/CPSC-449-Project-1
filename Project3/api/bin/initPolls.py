# Initialization schema for polls service
# Start DyanmoDB 
#   Navigate to 'CS 449'/dynamodb_local_latest & enter
#   $ java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
# Check to see tables:
#   $ aws dynamodb list-tables --endpoint-url http://localhost:8000

import boto3
import json
import string
import random

def createPollTable(dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName = 'Polls',
        KeySchema = [
            {
                'AttributeName': 'poll_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'createdBy',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName': 'poll_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'createdBy',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput = {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

def deletePollTable(dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        table = dynamodb.Table('Polls')
        table.delete()

def main(dynamodb = None):
    # delete existing table (testing)
    deletePollTable()
    # Creates new table
    pollTable = createPollTable()
    print("createPollTable Table Status:", pollTable.table_status)

    # Connect DynamoDB
    if not dynamodb: 
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Polls')

    initVal = '0'
    pollID = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
    pollID_num = str(pollID)

    newPoll = {
        'poll_id': pollID_num,
        'createdBy': 'Admin',
        'poll_data': {
            'question': 'How are you enjoying the polls service?',
            'response1': 'Its Great!',
            'resp1Votes': initVal,
            'response2': 'Its Okay',
            'resp2Votes': initVal,
            'response3': 'Its Bad!',
            'resp3Votes': initVal,
            'response4': 'I am Indifferent',
            'resp4Votes': initVal,
        },
        'voted': []
    }
    response = table.put_item(
        Item = newPoll
    )

    print("-- Default Poll Created --")
    print("-- Poll ID: " + pollID_num + " --")

if __name__ == '__main__':
    main()