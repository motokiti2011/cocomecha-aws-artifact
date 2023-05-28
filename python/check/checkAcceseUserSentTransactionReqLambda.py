import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
userInfo = dynamodb.Table("userInfo")
serviceTransactionRequest = dynamodb.Table("serviceTransactionRequest")



# アクセスユーザーが取引依頼をしているかをチェックするLambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))

  OperationType = event['OperationType']

  try:
    if OperationType != 'CHECKACCESSUSERSENTTRANSACTIONREQ':
      print('OperationTypeFailure')
      return

    slipNo = event['Keys']['slipNo']
    userId = event['Keys']['accessUserId']

    print('LABEL_1')
    # アクセスユーザー情報取得
    userInfo = userInfo_query(userId)
    if len(userInfo) == 0 :
      print('userQueryFailure')
      return

    print('LABEL_2')
    # 取引依頼情報取得
    requestInfo = serviceTransactionRequest_query(slipNo)
    print('LABEL_3')
    print(requestInfo)
    if len(requestInfo) == 0 :
      print('LABEL_4')
      return
    else :
      print('LABEL_5')
      return checkRequest(requestInfo, userInfo[0])


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



# 取引依頼情報取得
def serviceTransactionRequest_query(slipNo):
  queryData = serviceTransactionRequest.query(
    IndexName = 'slipNo-index',
    KeyConditionExpression = Key("slipNo").eq(slipNo)
  )
  items=queryData['Items']
  print(items)
  return items


# サービス商品から管理者反映を行う
def checkRequest(requestInfo, userInfo):

  userId = userInfo['userId']
  mechanicId = userInfo['mechanicId']
  if mechanicId == None:
    mechanicId = '0'
  officeId = userInfo['officeId']
  if officeId == None:
    officeId = '0'

  for item in requestInfo :
    if item['serviceUserType'] == '0' :
      if item['requestUserId'] == userId :
        return item

    if item['serviceUserType'] == '1' and officeId != '0':
      if item['requestUserId'] == officeId :
        return item

    if item['serviceUserType'] == '2' and mechanicId != '0':
      if item['requestUserId'] == mechanicId :
        return item

  # ここまで到達した場合
  return



