import boto3
import json
import os
import datetime
import time
from twilio.rest import Client


def send_sms(event, context):

    client = Client(os.environ["ACCOUNT_SID"], os.environ["AUTH_TOKEN"])

    client.messages.create(
            body="Still sending more messages.",
            messaging_service_sid=os.environ["MESSAGING_SERVICE_SID"],
            to='+17637725690',
        )

    response = {
        "statusCode": 200,
        "body": json.dumps("Message sent!")
    }

    return response


def ingest_sms(event, context):

    # Extract the message text and the phone number
    message_body = event["queryStringParameters"]["Body"]
    message_number = event["queryStringParameters"]["From"]

    #Calculating Time stamp for text entry
    date_time = str(datetime.datetime.now())
    date_time = date_time.split(" ")
    time_only = date_time[1].split(".")


    # Store message content and the sender's phone number into Dynamo (stripped of the '+' and country code).
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("customerlist")
    item = {
        'message': message_body,
        'phone': message_number[2:],
        'date': date_time[0],
        'time': time_only[0],
        'epochtime': int(time.time()),
        #     'text': data['text'],
        #     'checked': False,
        #     'createdAt': timestamp,
        #     'updatedAt': timestamp,
    }
    table.put_item(Item=item)

    # String text for reply to customer
    auto_reply_message = "Welcome to Pizza Ranch! We'll pack up your food right away. If we need any more info, we'll message you here."

    # Formatting reply into Twilio XML and passing back as response body.
    reply = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>' \
            f'<Response><Message><Body>{auto_reply_message}</Body></Message></Response>'
    response = {
        "statusCode": 200,
        "headers": {"content-type": "text/xml"},
        "body": reply
    }

    return response


def request_proper_sms(event, context):

    client = Client(os.environ["ACCOUNT_SID"], os.environ["AUTH_TOKEN"])

    sms_request = "We just need a few more details so we can bring you your food. Can you reply with your name and parking space number? Thanks!"

    client.messages.create(
        body=sms_request,
        messaging_service_sid=os.environ["MESSAGING_SERVICE_SID"],
        to='+17637725690',
    )

    response = {
        "statusCode": 200,
        "body": json.dumps("Message Sent")
    }

    return response
