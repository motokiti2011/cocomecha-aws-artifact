import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("factoryMechaInicItem")

# レコード検索 factoryMechanicId-index
def userId_query(partitionKey):
    queryData = table.query(
        IndexName = 'factoryMechanicId-index',
        KeyConditionExpression = Key("factoryMechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['factoryMechanicId']
        if IndexType == 'USERID-INDEX':
            return factoryMechanicId_query(PartitionKey)

        elif IndexType == 'FACTORYMECHANICID-INDEX':
          PartitionKey = event['Keys']['factoryMechanicId']
          return vehicleNo_query(PartitionKey)

    except Exception as e:
        print("Error Exception.")
        print(e)