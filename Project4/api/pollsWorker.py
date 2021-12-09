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

