import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("userMyList")


# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("id").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード更新
def put_product(PartitionKey, event):
  
  now = datetime.now()
  
  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'userId' : event['Keys']['userId'],
      'mechanicId' : event['Keys']['mechanicId'],
      'officeId' : event['Keys']['officeId'],
      'serviceType' : event['Keys']['serviceType'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : event['Keys']['serviceTitle'],
      'category' : event['Keys']['category'],
      'message' : event['Keys']['message'],
      'readDiv' : event['Keys']['readDiv'],
      'messageDate' : event['Keys']['messageDate'],
      'messageOrQuastionId' : event['Keys']['messageOrQuastionId'],
      'deleteDiv' : event['Keys']['deleteDiv'],
      'created' : event['Keys']['created'],
      'updated' :  now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse
  
  # レコード削除
def operation_delete(partitionKey):
    delResponse = table.delete_item(
       key={
           'id': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse

# レコード追加
def post_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'userId' : event['Keys']['userId'],
      'mechanicId' : event['Keys']['mechanicId'],
      'officeId' : event['Keys']['officeId'],
      'serviceType' : event['Keys']['serviceType'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : event['Keys']['serviceTitle'],
      'category' : event['Keys']['category'],
      'message' : event['Keys']['message'],
      'readDiv' : event['Keys']['readDiv'],
      'messageDate' : event['Keys']['messageDate'],
      'messageOrQuastionId' : event['Keys']['messageOrQuastionId'],
      'deleteDiv' : event['Keys']['deleteDiv'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')

    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse

def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['id']
      return operation_query(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = id
      return post_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      return operation_delete(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['id']
      return put_product(PartitionKey, event)

  except Exception as e:
      print("Error Exception.")
      print(e)