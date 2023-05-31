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
userMyList = dynamodb.Table("userMyList")
slipDetailInfo = dynamodb.Table("slipDetailInfo")
salesServiceInfo = dynamodb.Table("salesServiceInfo")
transactionSlip = dynamodb.Table("transactionSlip")


# 取引依頼確定Lambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)

  OperationType = event['OperationType']
  requestData = event['Keys']['serviceTransactionRequest']
  adminUserId = event['Keys']['userId']
  serviceType = event['Keys']['serviceUserType']
 
  try:
    if OperationType != 'CONFIRMTRANSACTION':
      print('CONFIRMTRANSACTION_Failure')
      return 400

    print('LABEL_1')
    # 承認者情報取得
    userInfo = userInfo_query(adminUserId)
    if len(userInfo) == 0 :
      print('Not_AdminUser_Failure')
      return 400

    print('LABEL_2')
    # 対象伝票取得
    slipData = getSlip(requestData['requestId'], serviceType)
    if len(slipData) == 0 :
      print('Not_Slip_Failure')
      return 400

    print('LABEL_3')
    # 伝票管理者チェック
    if  userInfo[0]['userId'] != slipData[0]['slipAdminUserId'] :
      print('Not_ADMIN_Failure')
      return 400


    print('LABEL_4')
    # 取引依頼の承認
    approvalResult = approvalRequest_query(requestData)
    if approvalResult != 200 :
      print('Not_Approval_Failure')
      return 400

    print('LABEL_5')
    # 対象伝票のステータス更新 「0」(出品中) → 「1」(取引中)
    statusResult = slipStatusExhibiting(requestData['requestId'])
    if statusResult != 200 :
      print('Not_SlipStatusExhibiting_Failure')
      return 400

    print('LABEL_6')
    # 管理者へのマイリストへのMsg登録
    postMyListResult = postAdminMyList(requestData, userInfo , slipData[0])
    if postMyListResult != 200 :
      print('PostMyList_Failure')
      return 400
    
    # 承認した依頼者、その他の依頼者へのMsg処理
    print('LABEL_7')
    postResult = requestMsgApproveAndOther(requestData, slipData[0])
    if postResult != 200 :
      print('PostMyList_Failure')
      return 400
    



  except Exception as e:
      print("Error Exception.")
      print(e)


# 管理者のユーザー情報を取得
def userInfo_query(adminUserId) :
  # 引数
  input_event = {
    "OperationType" : 'QUERY',
    "Keys" : {
      "userId": adminUserId
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
    return None

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

# 取引依頼TBLを更新
def approvalRequest_query(requestData):

  requestData['confirmDiv'] = '1'
  requestData['updated'] = datetime.now().strftime('%x %X')

  putResponse = serviceTransactionRequest.put_item(requestData)
  # putResponse = serviceTransactionRequest.put_item(
  #   Item={
  #     'id' : PartitionKey,
  #     'slipNo' : event['Keys']['slipNo'],
  #     'requestId' : event['Keys']['requestId'],
  #     'requestUserName' : event['Keys']['requestUserName'],
  #     'serviceUserType' : event['Keys']['serviceUserType'],
  #     'requestType' : event['Keys']['requestType'],
  #     'files' : event['Keys']['files'],
  #     'requestStatus' : event['Keys']['requestStatus'],
  #     'confirmDiv' : '1',
  #     'deadline' : event['Keys']['deadline'],
  #     'created' : now.strftime('%x %X'),
  #     'updated' : now.strftime('%x %X')
  #   }
  # )  
  return putResponse['ResponseMetadata']['HTTPStatusCode']

# 伝票の取引開始を行う
def slipStatusExhibiting(slipNo, serviceType) :
  input_event = {
    "slipNo": slipNo,
    "serviceType": serviceType,
    "processStatus": '2',
  }
  Payload = json.dumps(input_event) # jsonシリアライズ
  # 同期処理で呼び出し
  response = boto3.client('lambda').invoke(
      FunctionName='internalMoveSlipProcessStatusLambda',
      InvocationType='RequestResponse',
      Payload=Payload
  )
  body = json.loads(response['Payload'].read())
  print(body)
  # ユーザー情報のユーザーIDを取得
  if body != None :
    return body
  else :
    print('NOT-CERTIFICATION')
    return None


# 管理者のマイリストTBLにMsg登録
def postAdminMyList(requestData, userInfo, slipData)
  input_event = {
    "userList": userInfo,
    "slipInfo": slipData,
    "category": '10',
    "message": 'TRAN_ST',
    "requestInfo": requestData['requestInfo'],
  }
  Payload = json.dumps(input_event) # jsonシリアライズ
  # 同期処理で呼び出し
  response = boto3.client('lambda').invoke(
      FunctionName='internalMoveSlipProcessStatusLambda',
      InvocationType='RequestResponse',
      Payload=Payload
  )
  body = json.loads(response['Payload'].read())
  print(body)
  # ユーザー情報のユーザーIDを取得
  if body != None :
    return body
  else :
    print('NOT-CERTIFICATION')
    return None


# 承認した依頼者、その他の依頼者へのMsg処理
def requestMsgApproveAndOther(requestData, slipData) :
  input_event = {
    "requestData": requestData,
    "slipInfo": slipData,

  }
  Payload = json.dumps(input_event) # jsonシリアライズ
  # 同期処理で呼び出し
  response = boto3.client('lambda').invoke(
      FunctionName='internalRequestMsgApproveAndOtherLambda',
      InvocationType='RequestResponse',
      Payload=Payload
  )
  body = json.loads(response['Payload'].read())
  print(body)
  # ユーザー情報のユーザーIDを取得
  if body != None :
    return body
  else :
    print('NOT-CERTIFICATION')
    return None







  

