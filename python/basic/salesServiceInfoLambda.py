import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("salesServiceInfo")


# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey) & Key("deleteDiv").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return items

# レコード追加
def post_product(PartitionKey, event):
  putResponse = table.put_item(
    Item={
      'slipNo' : PartitionKey,
      'deleteDiv' : event['Keys']['deleteDiv'],
      'category' : event['Keys']['category'],
      'slipAdminUserId' : event['Keys']['slipAdminUserId'],
      'slipAdminUserName' : event['Keys']['slipAdminUserName'],
      'slipAdminOfficeId' : event['Keys']['slipAdminOfficeId'],
      'slipAdminOfficeName' : event['Keys']['slipAdminOfficeName'],
      'slipAdminMechanicId' : event['Keys']['slipAdminMechanicId'],
      'slipAdminMechanicName' : event['Keys']['slipAdminMechanicName'],
      'adminDiv' : event['Keys']['adminDiv'],
      'title' : event['Keys']['title'],
      'areaNo1' : event['Keys']['areaNo1'],
      'areaNo2' : event['Keys']['areaNo2'],
      'price' : event['Keys']['price'],
      'bidMethod' : event['Keys']['bidMethod'],
      'bidderId' : event['Keys']['bidderId'],
      'bidEndDate' : event['Keys']['bidEndDate'],
      'explanation' : event['Keys']['explanation'],
      'displayDiv' : event['Keys']['displayDiv'],
      'processStatus' : event['Keys']['processStatus'],
      'serviceType' : event['Keys']['serviceType'],
      'targetVehicleId' : event['Keys']['targetVehicleId'],
      'targetVehicleDiv' : event['Keys']['targetVehicleDiv'],
      'targetVehicleName' : event['Keys']['targetVehicleName'],
      'targetVehicleInfo' : event['Keys']['targetVehicleInfo'],
      'workAreaInfo' : event['Keys']['workAreaInfo'],
      'preferredDate' : event['Keys']['preferredDate'],
      'preferredTime' : event['Keys']['preferredTime'],
      'completionDate' : event['Keys']['completionDate'],
      'transactionCompletionDate' : event['Keys']['transactionCompletionDate'],
      'thumbnailUrl' : event['Keys']['thumbnailUrl'],
      'imageUrlList' : event['Keys']['imageUrlList'],
      'messageOpenLebel' : event['Keys']['messageOpenLebel'],
      'updateUserId' : event['Keys']['updateUserId'],
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['Item']
  
  # レコード削除
def operation_delete(partitionKey):
    delResponse = table.delete_item(
       Key={
           'slipNo': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse['Items']


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['slipNo']
      sortKey = event['Keys']['deleteDiv']
      return operation_query(PartitionKey, sortKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['slipNo']
      return post_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      return operation_delete(PartitionKey)

  except Exception as e:
      print("Error Exception.")
      print(e)