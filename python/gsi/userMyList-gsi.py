import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("userMyList")
# テーブルスキャン
def operation_scan():
    scanData = table.scan()
    items=scanData['Items']
    print(items)
    return scanData

# レコード検索 userId-index
def mechanicId_query(partitionKey):
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return queryData

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    OperationType = event['OperationType']
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['userId']
        if IndexType == 'USERID-INDEX':
            return mechanicId_query(PartitionKey)

    except Exception as e:
        print("Error Exception.")
        print(e)