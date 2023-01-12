import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("userVehicleInfo")

# レコード検索 userId-index
def userId_query(partitionKey):
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# レコード検索 vehicleNo-index
def vehicleNo_query(partitionKey):
    queryData = table.query(
        IndexName = 'vehicleNo-index',
        KeyConditionExpression = Key("vehicleNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['id']
        if IndexType == 'USERID-INDEX':
            return userId_query(PartitionKey)

        elif IndexType == 'VEHICLENO-INDEX':
          PartitionKey = event['Keys']['id']
          return vehicleNo_query(PartitionKey)


    except Exception as e:
        print("Error Exception.")
        print(e)