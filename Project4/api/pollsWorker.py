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
from emailDebug import email_notify

dynamodb = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

def removePoll(username, poll_id):
    # Connect DynamoDB
    if not dynamodb: 
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Polls')

    response = table.delete_item(
        Key = {
            'poll_id': str(poll_id), 
            'createdBy': str(username) 
        },
    )
    id = 'p' + poll_id
    email_notify(username, str(id))
    return True