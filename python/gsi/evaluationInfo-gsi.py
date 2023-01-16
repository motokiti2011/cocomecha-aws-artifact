import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("evaluationInfo")


# レコード検索 slipNo-index
def slipNo_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'slipNo-index',
        KeyConditionExpression = Key("slipNo").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items


# レコード検索 mechanicId-index
def mechanicId_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'mechanicId-index',
        KeyConditionExpression = Key("mechanicId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items


# レコード検索 officeId-index
def officeId_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'officeId-index',
        KeyConditionExpression = Key("officeId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['id']
        SortKey = event['Keys']['serviceType']
        if IndexType == 'MECHANICID-INDEX':
            return mechanicId_query(PartitionKey, SortKey)

        elif IndexType == 'OFFICEID-INDEX':
          return officeId_query(PartitionKey, SortKey)

        elif IndexType == 'SLIPNO-INDEX':
          return slipNo_query(PartitionKey, SortKey)

    except Exception as e:
        print("Error Exception.")
        print(e)