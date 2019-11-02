import boto3

dynamodb = boto3.client("dynamodb")
table = dynamodb.Table('Oppor')


def lambda_handler(event, context):
    for record in event['Records']:
        print(record['eventID'])
        print(record['eventName'])
        update_location(record['userId'], record['latitude'], record['longitude'])
    print('Done!')


def update_location(userid, latitude, longitude):
    print('Updating user {} with latitude {} and longitude {}'.format(userid, latitude, longitude))
    result = table.update_item(
        Key={
            'Id': userid,
            'Type': 'User'
        },
        UpdateExpression='SET latitude = :lat, longitude = :lon',
        ExpressionAttributeValues={
            ':lat': latitude,
            ':lon': longitude
        }
    )
    print('Location update result: {}'.format(result))
