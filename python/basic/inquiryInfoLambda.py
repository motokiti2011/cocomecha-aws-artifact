import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("inquiryInfo")

def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['inquiryId']
      return operation_query(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['inquiryId']
      return put_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      PartitionKey = event['Keys']['inquiryId']
      return operation_delete(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = id
      return post_product(PartitionKey, event)


  except Exception as e:
      print("Error Exception.")
      print(e)

# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("inquiryId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード更新
def put_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'inquiryId' : PartitionKey,
      'inquiryUserId' : event['Keys']['inquiryUserId'],
      'inquiryUserName' : event['Keys']['inquiryUserName'],
      'inquiryUserCategory' : event['Keys']['inquiryUserCategory'],
      'inquiryUserContents' : event['Keys']['inquiryUserContents'],
      'inquiryAdless' : event['Keys']['inquiryAdless'],
      'inquiryMailAdless' : event['Keys']['inquiryMailAdless'],
      'inquiryDate' : event['Keys']['inquiryDate'],
      'anserDiv' : event['Keys']['anserDiv'],
      'anserDate' : event['Keys']['anserDate'],
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
def post_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'inquiryId' : PartitionKey,
      'inquiryUserId' : event['Keys']['inquiryUserId'],
      'inquiryUserName' : event['Keys']['inquiryUserName'],
      'inquiryUserCategory' : event['Keys']['inquiryUserCategory'],
      'inquiryUserContents' : event['Keys']['inquiryUserContents'],
      'inquiryAdless' : event['Keys']['inquiryAdless'],
      'inquiryMailAdless' : event['Keys']['inquiryMailAdless'],
      'inquiryDate' : event['Keys']['inquiryDate'],
      'anserDiv' : event['Keys']['anserDiv'],
      'anserDate' : event['Keys']['anserDate'],
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
           'inquiryId': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse['ResponseMetadata']['HTTPStatusCode']

