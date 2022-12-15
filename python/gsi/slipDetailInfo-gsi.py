import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("slipDetailInfo")
# テーブルスキャン
def operation_scan():
    scanData = table.scan()
    items=scanData['Items']
    print(items)
    return scanData

# 1レコード検索 areaNo1-index
def areaNo1_query(partitionKey):
    queryData = table.query(
        IndexName = 'areaNo1-index',
        KeyConditionExpression = Key("areaNo1").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return queryData

# 2レコード検索 areaNo1AndAreaNo2-index
def areaNo1AndAreaNo2_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'areaNo1AndAreaNo2-index',
        KeyConditionExpression = Key("officeId").eq(partitionKey) & Key("areaNo2").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return queryData

# 3レコード検索 category-index
def category_query(partitionKey):
    queryData = table.query(
        IndexName = 'category-index',
        KeyConditionExpression = Key("category").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return queryData

# 4レコード検索 categoryAndAreaNo1-index
def categoryAndAreaNo1_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'categoryAndAreaNo1-index',
        KeyConditionExpression = Key("category").eq(partitionKey) & Key("areaNo1").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return queryData


# 5レコード検索 areaNo1AndCategory-index
def areaNo1AndCategory_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'areaNo1AndCategory-index',
        KeyConditionExpression = Key("areaNo1").eq(partitionKey) & Key("category").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return queryData


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    OperationType = event['OperationType']
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['areaNo1']
        if IndexType == 'AREANO1-INDEX':
            return areaNo1_query(PartitionKey)

        elif IndexType == 'AREANO1ANDAREANO2-INDEX':
          PartitionKey = event['Keys']['areaNo1']
          SortKey = event['Keys']['areaNo2']
          return areaNo1AndAreaNo2_query(PartitionKey, SortKey)

        elif IndexType == 'CATEGORY-INDEX':
          PartitionKey = event['Keys']['category']
          return category_query(PartitionKey)

        elif IndexType == 'CATEGORYANDAREANO1-INDEX':
          PartitionKey = event['Keys']['category']
          SortKey = event['Keys']['areaNo1']
          return categoryAndAreaNo1_query(PartitionKey, SortKey)

        elif IndexType == 'AREANO1ANDCATEGORY-INDEX':
          PartitionKey = event['Keys']['areaNo1']
          SortKey = event['Keys']['category']
          return areaNo1AndCategory_query(PartitionKey, SortKey)

    except Exception as e:
        print("Error Exception.")
        print(e)