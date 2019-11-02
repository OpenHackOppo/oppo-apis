import logging
import os
import uuid

import boto3
import requests
from requests_aws4auth import AWS4Auth

region = 'us-east-2'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
host = os.environ['ES_ENDPOINT']
headers = {"Content-Type": "application/json"}
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info('Received new event {}, processing'.format(event))
    return create_user(event)


def create_user(user):
    logger.info('Creating/Updating user {}'.format(user))
    if 'Id' not in user:
        user['Id'] = str(uuid.uuid4())
    endpoint = host + '/user' + '/_doc/' + user['Id']
    logger.info('Sending document {} to endpoint {}'.format(user, endpoint))
    response = requests.put(endpoint, auth=awsauth, json=user, headers=headers)
    logger.info('Response from put request to ElasticSearch {}'.format(response))
    return user