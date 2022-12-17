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

# レコード検索 vehicleNo-index
def mechanicId_query(partitionKey):
    queryData = table.query(
        IndexName = 'vehicleNo-index',
        KeyConditionExpression = Key("vehicleNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return queryData

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['vehicleNo']
        if IndexType == 'VEHICLENO-INDEX':
            return mechanicId_query(PartitionKey)

    except Exception as e:
        print("Error Exception.")
        print(e)