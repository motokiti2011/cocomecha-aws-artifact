import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("transactionSlip")

# 1レコード検索 slipUserId-index
def slipUser_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(partitionKey) & Key("serviceType").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return items

# 2レコード検索 slipOffice-index
def slipOffice_query(partitionKey):
    queryData = table.query(
        IndexName = 'officeId-index',
        KeyConditionExpression = Key("officeId").eq(partitionKey) & Key("serviceType").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return items

# 3レコード検索 slipMechanic-index
def slipMechanic_query(partitionKey):
    queryData = table.query(
        IndexName = 'mechanicId-index',
        KeyConditionExpression = Key("mechanicId").eq(partitionKey) & Key("serviceType").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    SortKey = event['Keys']['serviceType']

    try:
        PartitionKey = event['Keys']['id']
        if IndexType == 'SLIPUSER-INDEX':
            return slipUser_query(PartitionKey,SortKey)

        elif IndexType == 'SLIPOFFICE-INDEX':
          PartitionKey = event['Keys']['id']
          return slipOffice_query(PartitionKey, SortKey)

        elif IndexType == 'SLIPMECHANIC-INDEX':
          PartitionKey = event['Keys']['id']
          return slipMechanic_query(PartitionKey,SortKey)

    except Exception as e:
        print("Error Exception.")
        print(e)