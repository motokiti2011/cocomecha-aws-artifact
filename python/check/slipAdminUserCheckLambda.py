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



# 伝票管理者チェック
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))

  OperationType = event['OperationType']

  try:
    if OperationType == 'ADMINIDCHECHK':
      slipNo = event['Keys']['slipNo']
      serviceType = event['Keys']['serviceType']
      adminId = event['Keys']['adminId']

      if serviceType == '0':
        # 認証情報チェック後ユーザーIDを取得
        # 引数
        input_event = {
            "userId": adminId,
        }
        Payload = json.dumps(input_event) # jsonシリアライズ
        # 同期処理で呼び出し
        response = boto3.client('lambda').invoke(
            FunctionName='CertificationLambda',
            InvocationType='RequestResponse',
            Payload=Payload
        )
        body = json.loads(response['Payload'].read())
        print(body)
        # ユーザー情報のユーザーIDを取得
        if body != None :
          userId = body
        else :
          print('NOT-CERTIFICATION')
          return

        return slipDetailInfo_query(slipNo, userId)

      elif serviceType == '1':
        return salesServiceInfoOffice_query(slipNo, adminId)

      elif serviceType == '2':
        return salesServiceInfoMecha_query(slipNo, adminId)

  except Exception as e:
      print("Error Exception.")
      print(e)

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
        IndexName = 'slipAdminOfficeId-index',
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

