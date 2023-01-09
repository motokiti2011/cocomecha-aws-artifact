import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("mechanicInfo")


# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("mechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード更新
def put_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'mechanicId' : PartitionKey,
      'validDiv' : event['Keys']['validDiv'],
      'mechanicName' : event['Keys']['mechanicName'],
      'adminUserId' : event['Keys']['adminUserId'],
      'adminAddressDiv' : event['Keys']['adminAddressDiv'],
      'telList' : event['Keys']['telList'],
      'mailAdress' : event['Keys']['mailAdress'],
      'officeConnectionDiv' : event['Keys']['officeConnectionDiv'],
      'officeId' : event['Keys']['officeId'],
      'associationOfficeList': event['Keys']['associationOfficeList'],
      'qualification' : event['Keys']['qualification'],
      'specialtyWork' : event['Keys']['specialtyWork'],
      'profileImageUrl' : event['Keys']['profileImageUrl'],
      'Introduction' : event['Keys']['Introduction'],
      'evaluationInfoIdList' : event['Keys']['evaluationInfoIdList'],
      'updateUserId' : event['Keys']['updateUserId'],
      'created' : event['Keys']['created'],
      'updated' :  now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse


# レコード登録
def post_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'mechanicId' : PartitionKey,
      'validDiv' : event['Keys']['validDiv'],
      'mechanicName' : event['Keys']['mechanicName'],
      'adminUserId' : event['Keys']['adminUserId'],
      'adminAddressDiv' : event['Keys']['adminAddressDiv'],
      'telList' : event['Keys']['telList'],
      'mailAdress' : event['Keys']['mailAdress'],
      'officeConnectionDiv' : event['Keys']['officeConnectionDiv'],
      'officeId' : event['Keys']['officeId'],
      'associationOfficeList': event['Keys']['associationOfficeList'],
      'qualification' : event['Keys']['qualification'],
      'specialtyWork' : event['Keys']['specialtyWork'],
      'profileImageUrl' : event['Keys']['profileImageUrl'],
      'Introduction' : event['Keys']['Introduction'],
      'evaluationInfoIdList' : event['Keys']['evaluationInfoIdList'],
      'updateUserId' : event['Keys']['updateUserId'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
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
           'mechanicId': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['mechanicId']
      return operation_query(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['mechanicId']
      return put_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      PartitionKey = event['Keys']['mechanicId']
      return operation_delete(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = id
      return post_product(PartitionKey, event)

  except Exception as e:
      print("Error Exception.")
      print(e)