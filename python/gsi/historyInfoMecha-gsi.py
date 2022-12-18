import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("historyInfoMecha")

# レコード検索 historyId-index
def historyId_query(partitionKey):
    queryData = table.query(
        IndexName = 'historyId-index',
        KeyConditionExpression = Key("historyId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード検索 mechanicId-index
def mechanicId_query(partitionKey):
    queryData = table.query(
        IndexName = 'mechanicId-index',
        KeyConditionExpression = Key("mechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['historyId']
        if IndexType == 'HISTORYID-INDEX':
            return historyId_query(PartitionKey)

        elif IndexType == 'MECHANICID-INDEX':
          PartitionKey = event['Keys']['mechanicId']
          return mechanicId_query(PartitionKey)
        
    except Exception as e:
        print("Error Exception.")
        print(e)