import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("historyInfoOffice")

# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("historyId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード更新
def post_product(PartitionKey, event):
  putResponse = table.put_item(
    Item={
      'historyId' : PartitionKey,
      'slipNo' : event['Keys']['slipNo'],
      'slipTitle' : event['Keys']['slipTitle'],
      'officeId' : event['Keys']['officeId'],
      'mechanicId' : event['Keys']['mechanicId'],
      'completionDate' : event['Keys']['completionDate'],
      'displayDiv' : event['Keys']['displayDiv'],
      'created' : event['Keys']['created'],
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['ResponseMetadata']['HTTPStatusCode']


# レコード追加
def operation_post(PartitionKey, event):
  putResponse = table.put_item(
    Item={
      'historyId' : PartitionKey,
      'slipNo' : event['Keys']['slipNo'],
      'slipTitle' : event['Keys']['slipTitle'],
      'officeId' : event['Keys']['officeId'],
      'mechanicId' : event['Keys']['mechanicId'],
      'completionDate' : event['Keys']['completionDate'],
      'displayDiv' : event['Keys']['displayDiv'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
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
           'historyId': partitionKey,
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

    if OperationType == 'PUT':
      PartitionKey = event['Keys']['historyId']
      return post_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      PartitionKey = event['Keys']['historyId']
      return operation_delete(PartitionKey)

    else : 
      return operation_query(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = id
      return operation_post(PartitionKey, event)

  except Exception as e:
      print("Error Exception.")
      print(e)