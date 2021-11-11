# Initialization schema for polls service
# Check to see tables:
#   $ aws dynamodb list-tables --endpoint-url http://localhost:8000

import boto3

def createPollTable(dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

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
                'AttributeType': 'N'
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

if __name__ == '__main__':
    # Creates new table
    pollTable = createPollTable()
    print("createPollTable Table Status:", pollTable.table_status)