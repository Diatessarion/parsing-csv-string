import json
import os
from twilio.rest import Client
import boto3
import time

def send_sms(event, context):

    client = Client(os.environ["ACCOUNT_SID"], os.environ["AUTH_TOKEN"])

    client.messages.create(
            body="Still sending more messages.",
            messaging_service_sid='MG869564792f35036a37ca76441f47f632',
            to='+17637725690'
        )

    response = {
        "statusCode": 200,
        "body": json.dumps("Message sent!?")
    }

    return response


def ingest_sms(event, context):

    message_body = event["queryStringParameters"]["Body"]
    message_number = event["queryStringParameters"]["From"]

    body = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>' \
           f'<Response><Message><Body>"Thanks for sending today!"</Body></Message></Response>'

    response = {
        "statusCode": 200,
        "headers": {"content-type": "text/xml"},
        "body": body
    }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("customerlist")
    item = {
        'message': message_body,
        'phone': message_number,
        'timestamp': str(time.time())
        #     'text': data['text'],
        #     'checked': False,
        #     'createdAt': timestamp,
        #     'updatedAt': timestamp,
    }
    # write the to the database
    table.put_item(Item=item)

    return response
