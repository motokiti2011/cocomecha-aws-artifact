import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("completionSlip")

# 1レコード検索 slipAdminUserId-index
def slipAdminUserId_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminUserId-index',
        KeyConditionExpression = Key("slipAdminUserId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 2レコード検索 slipAdminOfficeId-index
def slipAdminOffice_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminOffice-index',
        KeyConditionExpression = Key("slipAdminOfficeId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 3レコード検索 slipAdminMechanicId-index
def slipAdminBaseId_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminBaseId-index',
        KeyConditionExpression = Key("slipAdminMechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['slipAdminUserId']
        if IndexType == 'SLIPADMINUSERID-INDEX':
            return slipAdminUserId_query(PartitionKey)

        elif IndexType == 'SLIPADMINOFFICE-INDEX':
          PartitionKey = event['Keys']['slipAdminOfficeId']
          return slipAdminOffice_query(PartitionKey, SortKey)

        elif IndexType == 'SLIPADMINMECHANIC-INDEX':
          PartitionKey = event['Keys']['slipAdminMechanicId']
          return slipAdminBaseId_query(PartitionKey)

    except Exception as e:
        print("Error Exception.")
        print(e)