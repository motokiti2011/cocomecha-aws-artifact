import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("slipMegPrmUser")

# テーブルスキャン
def operation_scan():
    scanData = table.scan()
    items=scanData['Items']
    print(items)
    return scanData

# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード追加
def post_product(PartitionKey, event):
  putResponse = table.put_item(
    Item={
      'slipNo' : PartitionKey,
      'slipAdminUserId' : event['Keys']['slipAdminUserId'],
      'slipAdminUserName' : event['Keys']['slipAdminUserName'],
      'permissionUserList' : event['Keys']['permissionUserList'],
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['ResponseMetadata']['HTTPStatusCode']
  
  # レコード削除
def operation_delete(partitionKey):
    delResponse = table.delete_item(
       Key={
           'userId': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse['ResponseMetadata']['HTTPStatusCode']


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['slipNo']
      return operation_query(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['slipNo']
      return post_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      return operation_delete(PartitionKey)

  except Exception as e:
      print("Error Exception.")
      print(e)