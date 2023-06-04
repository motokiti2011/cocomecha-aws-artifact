import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
serviceTransactionRequest = dynamodb.Table("serviceTransactionRequest")
slipDetailInfo = dynamodb.Table("slipDetailInfo")
salesServiceInfo = dynamodb.Table("salesServiceInfo")


# 完了日設定Lambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:
    if OperationType != 'SCHEDULEDCOMPSETTING':
      return None

    slipNo = event['Keys']['slipNo']
    serviceType = event['Keys']['serviceType']
    compDate = event['Keys']['compDate']
    acceseUserId = event['Keys']['acceseUserId']

    print('LABEL_1')
    # アクセス者情報取得
    userInfo = userInfo_query(acceseUserId)
    if len(userInfo) == 0 :
      print('Not_AdminUser_Failure')
      return 400

    print('LABEL_2')
    # 対象の伝票情報を取得
    slipData = getSlip(slipNo, serviceType)
    if len(slipData) == 0 :
      print('Not_Slip_Failure')
      return None
    
    print('LABEL_3')
    # 管理者チェック
    if  userInfo['userId'] != slipData[0]['slipAdminUserId'] :
      print('LABEL_3,5')
      # アクセス者が管理者でない場合、依頼者チェックを行う
      if requestAcceseCheck(slipNo, userInfo) :
        print('Not_ADMIN_Failure')
        return None
    
    print('LABEL_4')
    # 対象の伝票情報を更新
    if serviceType == '0' :
      result = put_slip(slipData[0], compDate)
    else :
      result = put_salesService(slipData[0], compDate)
    
    print('LABEL_5')
    # 更新後の結果を返却
    print('scheduledCompletionSettingLambda_Sucsess')
    return result
    
    
    
  except Exception as e:
      print("Error Exception.")
      print(e)
      

# アクセス者のユーザー情報を取得
def userInfo_query(adminUserId) :
  # 引数
  input_event = {
    "OperationType" : 'QUERY',
    "Keys" : {
      "userId": adminUserId,
      "userValidDiv" : '0'
    }
  }
  Payload = json.dumps(input_event) # jsonシリアライズ
  # 同期処理で呼び出し
  response = boto3.client('lambda').invoke(
      FunctionName='userInfoLambda',
      InvocationType='RequestResponse',
      Payload=Payload
  )
  body = json.loads(response['Payload'].read())
  print(body)
  # ユーザー情報のユーザーIDを取得
  if body != None :
    return body[0]
  else :
    print('NOT-CERTIFICATION')
    return []



# 取引依頼対象の伝票情報を取得する
def getSlip(slipNo, serviceType) :
  if serviceType == '0' :
    return slipDetail_query(slipNo)
  else :
    return salesService_query(slipNo)

# 伝票詳細情報取得
def slipDetail_query(slipNo) :
  queryData = slipDetailInfo.query(
      KeyConditionExpression = Key("slipNo").eq(slipNo) & Key("deleteDiv").eq("0")
  )
  items=queryData['Items']
  return items

# サービス商品情報取得
def salesService_query(slipNo) :
  queryData = salesServiceInfo.query(
      KeyConditionExpression = Key("slipNo").eq(slipNo) & Key("deleteDiv").eq("0")
  )
  items=queryData['Items']
  return items


# 取引依頼者チェック
def requestAcceseCheck(slipNo, userInfo):
  # 取引依頼情報取得
  res = transactionRequest_query(slipNo)
  # 取得できない場合エラー
  if len(res) == 0 :
    return None
  tranReqest = False

  # 取引依頼者情報取得
  for item in res :
    if item['requestStatus'] == '1':
      tranReqest = item
  # 取得できない場合エラー
  if tranReqest == None :
    return False

  if tranReqest['serviceUserType'] == '0' :
    if tranReqest['requestUserId'] == userInfo['userId'] :
      return True
  elif tranReqest['serviceUserType'] == '1' :
    if tranReqest['requestUserId'] == userInfo['officeId'] :
      return True
  else :
    if tranReqest['requestUserId'] == userInfo['mechanicId'] :
      return True
  
  # ここまで到達でNG
  return False

# 取引依頼者情報取得
def transactionRequest_query(slipNo):
  queryData = serviceTransactionRequest.query(
      IndexName = 'slipNo-index',
      KeyConditionExpression = Key("slipNo").eq(slipNo)
  )
  items=queryData['Items']
  print(items)
  return items

# 伝票情報の完了日付を更新
def put_slip(slipData, compDate) :

  slipData['completionDate'] = compDate
  slipData['updated'] = datetime.now().strftime('%x %X')
  
  slip = slipData
  putResponse = slipDetailInfo.put_item(Item=slip)
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    return None

  return slip

# サービス商品の完了日付を更新
def put_salesService(slipData, compDate) :

  slipData['completionDate'] = compDate
  slipData['updated'] = datetime.now().strftime('%x %X')
  
  slip = slipData
  putResponse = salesServiceInfo.put_item(Item=slip)
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    return None

  return slip


