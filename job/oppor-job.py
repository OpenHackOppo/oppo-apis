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
    return create_job(event)


def create_job(job):
    logger.info('Creating/Updating job {}'.format(job))
    if 'Id' not in job:
        job['Id'] = str(uuid.uuid4())
    endpoint = host + '/job' + '/_doc/' + job['Id']
    logger.info('Sending document {} to endpoint {}'.format(job, endpoint))
    response = requests.put(endpoint, awsauth, json=job, headers=headers)
    logger.info('Response from put request to ElasticSearch {}'.format(response))
    return job