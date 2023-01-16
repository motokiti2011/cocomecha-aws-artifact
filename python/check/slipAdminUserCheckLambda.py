import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
slipDetailInfo = dynamodb.Table("slipDetailInfo")
salesServiceInfo = dynamodb.Table("salesServiceInfo")


# レコード検索
def slipDetailInfo_query(slipNo, adminId):
    queryData = slipDetailInfo.query(
        IndexName = 'slipAdminUserId-index',
        KeyConditionExpression = Key("slipAdminUserId").eq(adminId)
    )
    items=queryData['Items']
    print(items)
    return items

    if len(items) == 0:
      return []

    item = items[0]
    
    if item['slipNo'] == slipNo :
      return item
    else :
      return []


# レコード検索
def salesServiceInfoOffice_query(slipNo, adminId):
    queryData = slipDetailInfo.query(
        IndexName = 'slipAdminOfficeId',
        KeyConditionExpression = Key("slipAdminOfficeId").eq(adminId) & Key("deleteDiv").eq("0")
    )
    items=queryData['Items']
    print(items)
    return items

    if len(items) == 0:
      return []

    item = items[0]
    
    if item['slipNo'] == slipNo :
      return item
    else :
      return []

# レコード検索
def salesServiceInfoMecha_query(slipNo, adminId):
    queryData = slipDetailInfo.query(
        IndexName = 'slipAdminMechanic-index',
        KeyConditionExpression = Key("slipAdminMechanicId").eq(adminId) & Key("deleteDiv").eq("0")
    )
    items=queryData['Items']
    print(items)
    return items

    if len(items) == 0:
      return []

    item = items[0]
    
    if item['slipNo'] == slipNo :
      return item
    else :
      return []


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))

  OperationType = event['OperationType']

  try:
    if OperationType == 'ADMINIDCHECHK':
      slipNo = event['Keys']['slipNo']
      serviceType = event['Keys']['serviceType']
      adminId = event['Keys']['adminId']

      if serviceType == '0':
        return slipDetailInfo_query(slipNo, adminId)

      elif serviceType == '1':
        return salesServiceInfoOffice_query(slipNo, adminId)

      elif serviceType == '2':
        return salesServiceInfoMecha_query(slipNo, adminId)

  except Exception as e:
      print("Error Exception.")
      print(e)