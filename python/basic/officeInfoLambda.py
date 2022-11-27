import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("officeInfo")

# テーブルスキャン
def operation_scan():
    scanData = table.scan()
    items=scanData['Items']
    print(items)
    return scanData

# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("officeId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return queryData

# レコード追加
def post_product(PartitionKey, event):
  putResponse = table.put_item(
    Item={
      'officeId' : PartitionKey,
      'officeAreaNo' : event['Keys']['officeAreaNo'],
      'officeName' : event['Keys']['officeName'],
      'officeTel' : event['Keys']['officeTel'],
      'officeMailAdress' : event['Keys']['officeMailAdress'],
      'officeArea1' : event['Keys']['officeArea1'],
      'officeArea' : event['Keys']['officeArea'],
      'officePostCode' : event['Keys']['officePostCode'],
      'workContentList' : event['Keys']['workContentList'],
      'businessHours' : event['Keys']['businessHours'],
      'baseId' : event['Keys']['baseId'],
      'baseInfoList' : event['Keys']['baseInfoList'],
      'adminIdList' : event['Keys']['adminIdList'],
      'employeeList' : event['Keys']['employeeList'],
      'officePR' : event['Keys']['officePR'],
      'officePRimageURLList' : event['Keys']['officePRimageURLList'],
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
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
           'officeId': partitionKey,
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
    if OperationType == 'SCAN':
      return operation_scan()

    elif OperationType == 'QUERY':
      PartitionKey = event['Keys']['officeId']
      return operation_query(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['officeId'] + str(now)
      return post_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      return operation_delete(PartitionKey)

  except Exception as e:
      print("Error Exception.")
      print(e)