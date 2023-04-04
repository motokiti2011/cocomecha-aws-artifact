import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("inquiryInfo")

# 問い合わせTBLGSI検索Lambda
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['id']
        if IndexType == 'INQUIRYUSERID-INDEX':
            return inquiryUserId_query(PartitionKey)

        elif IndexType == 'INQUIRYADLESS-INDEX':
          PartitionKey = event['Keys']['id']
          return inquiryAdless_query(PartitionKey)

        elif IndexType == 'ANSERDIV-INDEX':
          PartitionKey = event['Keys']['id']
          return anserDiv_query(PartitionKey)

    except Exception as e:
        print("Error Exception.")
        print(e)



# レコード検索 inquiryUserId-index
def inquiryUserId_query(partitionKey):
    queryData = table.query(
        IndexName = 'inquiryUserId-index',
        KeyConditionExpression = Key("inquiryUserId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# レコード検索 inquiryAdless-index
def inquiryAdless_query(partitionKey):
    queryData = table.query(
        IndexName = 'inquiryAdless-index',
        KeyConditionExpression = Key("inquiryAdless").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード検索 anserDiv-index
def anserDiv_query(partitionKey):
    queryData = table.query(
        IndexName = 'anserDiv-index',
        KeyConditionExpression = Key("anserDiv").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

