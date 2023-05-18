import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("factoryMechaImpletion")

# 1レコード検索 factoryMechanic_-index
def factoryMechanic_query(partitionKey):
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
        if IndexType == 'FACTORYMECHANIC-INDEX':
            return factoryMechanic_query(PartitionKey)

    except Exception as e:
        print("Error Exception.")
        print(e)