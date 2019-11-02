import os
import sys
import requests
import boto3
import logging
import uuid

from requests_aws4auth import AWS4Auth


region = 'eu-west-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
host = os.environ['ES_ENDPOINT']
headers = {"Content-Type": "application/json"}
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info('Received new event {}, processing'.format(event))
    for record in event['Records']:
        return create_user(record['user'])


def create_user(user):
    logger.info('Creating/Updating user {}'.format(user))
    if not user['userId']:
        user['userId'] = str(uuid.uuid4())
    endpoint = host + '/user' + '/_doc/' + user['userId']
    response = requests.put(endpoint, awsauth, json=user, headers=headers)
    logger.info('Response from put request to ElasticSearch {}'.format(response))
    return user