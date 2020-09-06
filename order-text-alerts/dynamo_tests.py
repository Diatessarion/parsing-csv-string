import boto3
import json
import datetime


def get_message(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("customerlist")

    tableitem = table.get_item(Key={"message": 'DatabaseInfo'})
    epoch_time = tableitem["Item"]["timestamp"]

    date_time = datetime.datetime.fromtimestamp(int(float(epoch_time))).strftime("%Y-%m-%d %I:%M:%S")

   # string_time = date_time.strftime("%Y-%m-%d %I:%M:%S")

    response = {
        "statusCode": 200,
        "body": json.dumps(date_time)
    }

    return response
