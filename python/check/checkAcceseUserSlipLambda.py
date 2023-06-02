import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
userInfo = dynamodb.Table("userInfo")
table = dynamodb.Table("slipMegPrmUser")
salesServiceInfo = dynamodb.Table("salesServiceInfo")
slipDetailInfo = dynamodb.Table("slipDetailInfo")



# アクセスユーザーが伝票管理者かをチェックするLambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))

  OperationType = event['OperationType']

  try:
    if OperationType != 'CHECKACCESSUSERSLIP':
      print('OperationTypeFailure')
      return False
    print('LABEL_1')
    slipNo = event['Keys']['slipNo']
    serviceType = event['Keys']['serviceType']
    print('LABEL_2')
    # アクセスユーザー情報取得
    userInfo = userInfo_query(event['Keys']['userId'])
    if len(userInfo) == 0 :
      print('userQueryFailure')
      return False
    print('LABEL_3')
    # 伝票情報取得
    if serviceType == 0 :
      print('LABEL_4')
      return checkSlip(slipNo, userInfo[0])
    else :
      print('LABEL_5')
      return checkService(slipNo, userInfo[0], serviceType)
  except Exception as e:
      print("Error Exception.")
      print(e)

# ユーザー情報を取得
def userInfo_query(accessUser) :
  # 認証情報チェック後ユーザーIDを取得
  # 引数
  input_event = {
      "userId": accessUser,
  }
  Payload = json.dumps(input_event) # jsonシリアライズ
  # 同期処理で呼び出し
  response = boto3.client('lambda').invoke(
      FunctionName='certificationLambda',
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
  
  #ユーザーTBLを検索
  queryData = userInfo.query(
      KeyConditionExpression = Key("userId").eq(userId) & Key("userValidDiv").eq('0')
  )
  return queryData['Items']



# 伝票情報から管理者反映を行う
def checkSlip(slipNo, userInfo):
  queryData = slipDetailInfo.query(
      KeyConditionExpression = Key("slipNo").eq(slipNo) & Key("deleteDiv").eq('0')
  )
  items=queryData['Items']

  if len(items) == 0 :
    return False
  print('LABEL_6')
  if items[0]['slipAdminUserId'] == userInfo['userId'] :
    return True
  else :
    return False


# サービス商品から管理者反映を行う
def checkService(slipNo, userInfo, serviceType):
  # サービス商品を取得
  queryData = salesServiceInfo.query(
      KeyConditionExpression = Key("slipNo").eq(slipNo) & Key("deleteDiv").eq('0')
  )
  items=queryData['Items']

  if len(items) == 0 :
    return False
  print('LABEL_7')
  if serviceType == '1' :
    print('LABEL_8')
    if items[0]['slipAdminOfficeId'] == userInfo['officeId'] :
      return True
    else :
      return False
  else :
    print('LABEL_9')
    if items[0]['slipAdminMechanicId'] == userInfo['mechanicId'] :
      return True
    else :
      return False




