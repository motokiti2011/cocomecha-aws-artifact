import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("browsingHistory")

# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['userId']
        if IndexType == 'USERID-INDEX':
            return operation_query(PartitionKey)
        
    except Exception as e:
        print("Error Exception.")
        print(e)