import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("mechanicInfo")

# レコード検索 adminUserId-index
def mechanicId_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'adminUserId-index',
        KeyConditionExpression = Key("adminUserId").eq(partitionKey) & Key("validDiv").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return items


# レコード検索 officeId-index
def mechanicId_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'officeId-index',
        KeyConditionExpression = Key("officeId").eq(partitionKey) & Key("validDiv").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:


        if IndexType == 'ADMINUSERID-index':
          PartitionKey = event['Keys']['adminUserId']
          sortKey = event['Keys']['validDiv']
            return mechanicId_query(PartitionKey, sortKey)

        elif IndexType == 'OFFICEID-INDEX':
          PartitionKey = event['Keys']['officeId']
          sortKey = event['Keys']['validDiv']
          return category_query(PartitionKey, sortKey)

    except Exception as e:
        print("Error Exception.")
        print(e)