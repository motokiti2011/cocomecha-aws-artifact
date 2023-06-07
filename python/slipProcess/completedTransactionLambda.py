import json
import boto3
import uuid

from datetime import datetime
from decimal import Decimal

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
userInfo =  dynamodb.Table("userInfo")
completionSlip = dynamodb.Table("completionSlip")


# 取引完了Lambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)

  OperationType = event['OperationType']
  slipNo = event['Keys']['slipNo']
  serviceType = event['Keys']['serviceType']
  acceseUserId = event['Keys']['acceseUserId']
 
  try:
    if OperationType != 'COMPTRANSACTION':
      print('CONFIRMTRANSACTION_Failure')
      return 400


    print('LABEL_1')
    # アクセスユーザー情報取得
    userInfo = userInfo_query(acceseUserId)
    if len(userInfo) == 0 :
      print('Not_AdminUser_Failure')
      return 400


    print('LABEL_2')
    # 対象伝票取得
    slipData = getSlip(slipNo, serviceType)
    if len(slipData) == 0 :
      print('Not_Slip_Failure')
      return 400

    print('LABEL_3')
    # 伝票管理者チェック
    if  userInfo['userId'] != slipData[0]['slipAdminUserId'] :
      # アクセス者が管理者でない場合、依頼者チェックを行う
      requestDiv = requestAcceseCheck(slipNo, userInfo)
      if !requestDiv :
        print('Not_ADMIN_Failure')
        return None
    else :
      adminDiv = True


    print('LABEL_4')
    # 対象伝票のステータス更新 「1」(取引中) → 「2」(取引完了)
    statusResult = slipStatusExhibiting(slipNo,serviceType)
    if statusResult != 200 :
      print('Not_SlipStatusExhibiting_Failure')
      return 400


   # 管理者、取引者のユーザー情報取得
   if adminDiv :
     adminUserInfo = userInfo
     transactionUserInfo = transactionUser_query(slipNo)
   else :
     transactionUserInfo = userInfo
     adminUserInfo = userId_query(slipData[0]['slipAdminUserId'])


    print('LABEL_5')
    # 管理者へのマイリストへのMsg登録
    postMyListResult = postAdminMyList(requestData, adminUserInfo , slipData[0]) 
    if postMyListResult != 200 :
      print('PostMyList_Failure')
      return 400


    print('LABEL_6')
    # 取引者へのマイリストへのMsg登録
    postTranMyListResult = postAdminMyList(requestData, transactionUserInfo, slipData[0]) 
    if postTranMyListResult != 200 :
      print('PostMyList_Failure')
      return 400


    print('LABEL_7')
    # 完了済伝票情報の登録
    compRes = compSlip_query(slipData[0], adminUserInfo)
    if compRes != 200 :
      print('Not_compRes_Failure')
      return 400

    comptranRes = compSlip_query(requestData, transactionUserInfo)
    if comptranRes != 200 :
      print('Not_compRes_Failure')
      return 400



    # 取引中伝票情報の論理削除
    print('LABEL_8')
    postResult = requestMsgApproveAndOther(requestData, slipData[0]) 
    print('BUG_CHACK_END')
    if postResult != 200 :
      print('PostMyList_Failure')
      return 400


    # 取引中伝票情報の論理削除
    print('LABEL_9')
    postResult = requestMsgApproveAndOther(requestData, slipData[0]) 
    print('BUG_CHACK_END')
    if postResult != 200 :
      print('PostMyList_Failure')
      return 400




    # ここまで到達できれば正常終了
    print('LABEL_11')
    print('COMPLETEDTRANSACTIONLAMBDA_SUCCESS')
    return 200


  except Exception as e:
      print("Error Exception.")
      print(e)


# 管理者のユーザー情報を取得
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


# 取引依頼TBLを更新
def approvalRequest_query(requestData):

  requestData['confirmDiv'] = '1'
  requestData['updated'] = datetime.now().strftime('%x %X')
  print(requestData)

  putResponse = serviceTransactionRequest.put_item(Item=requestData)

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
def postAdminMyList(requestData, userInfo, slipData) :

  # マイリスト用のリクエスト情報生成
  requestInfo = {
    "requestId": requestData['id'],
    "requestType": '0',
    "requestTargetId": requestData['slipNo'],
    "requestTargetName": slipData['title'],
  }
  userList = []
  userList.append(userInfo)

  input_event = {
    "userList": userList,
    "slipInfo": slipData,
    "category": '10',
    "message": 'TRAN_ST',
    "requestInfo": requestInfo,
  }
  
  Payload = json.dumps(input_event, cls=DecimalEncoder) # jsonシリアライズ
  # 同期処理で呼び出し
  response = boto3.client('lambda').invoke(
      FunctionName='internalSendMsgMylistLambda',
      InvocationType='RequestResponse',
      Payload=Payload
  )

  body = json.loads(response['Payload'].read())
  print(body)

  if body != None :
    return body
  else :
    print('NOT-CERTIFICATION')
    return None



# 取引依頼者チェック
def requestAcceseCheck(slipNo, userInfo):
  # 取引依頼情報取得
  res = transactionRequest_query(slipNo)
  # 取得できない場合エラー
  if len(res) == 0 :
    return None
  tranReqest = False



# 取引依頼者情報取得
def transactionRequest_query(slipNo):
  queryData = serviceTransactionRequest.query(
      IndexName = 'slipNo-index',
      KeyConditionExpression = Key("slipNo").eq(slipNo)
  )
  items=queryData['Items']
  print(items)
  return items


# 承認した依頼者、その他の依頼者へのMsg処理
def requestMsgApproveAndOther(requestData, slipData) :
  input_event = {
    "requestData": requestData,
    "slipInfo": slipData,

  }

  Payload = json.dumps(input_event, cls=DecimalEncoder) # jsonシリアライズ
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

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, Decimal):
           return int(obj)
       return json.JSONEncoder.default(self, obj)



# 取引者のユーザー情報を取得する
def transactionUser_query(slipNo) :
  tranReqList = transactionRequest_query(slipNo):
  
  if reqId = None
  for item in tranReqList :
    if item['requestStatus'] == '1' :
      reqId = item['requestUserId']
      userType = item['serviceUserType']
  if reqId == None :
    retrn None

  if userType == '0' :
    return userId_query(reqId)
  elif userType == '1' :
    return officeId_query(reqId)
  else :
    return mechanicId_query(reqId)

# 変換なしのユーザーIDからユーザー情報を取得する。
def userId_query(userId) :
  queryData = userInfo.query(
      KeyConditionExpression = Key("userId").eq(userId) & Key("userValidDiv").eq('0')
  )
  items=queryData['Items']
  print(items)
  return items[0]


# 工場情報からユーザーIDを取得する
def officeId_query(officeId) :
  queryData = officeInfo.query(
      KeyConditionExpression = Key("officeId").eq(officeId)
  )
  items=queryData['Items']
  if len(items) == 0 :
    return None
  mechanicInfoList = items[0]['connectionMechanicInfo']
  # （仮）工場の関連メカニック情報の先頭が管理者となるためそのユーザー情報を取得
  return mechanicId_query(mechanicInfoList[0]['mechanicId'])


# メカニック情報からユーザーIDを取得する
def mechanicId_query(mechanicid) :
  queryData = mechanicInfo.query(
      KeyConditionExpression = Key("mechanicId").eq(mechanicid)
  )
  items=queryData['Items']
  if len(items) == 0 :
    return None
  return items[0]['adminUserId']




# レコード追加
def compSlip_query(slip, userInfo):

  now = datetime.now()

  putResponse = completionSlip.put_item(
    Item={
      'slipNo' : slip['slipNo'],
      'slipAdminUserId' : slip['slipAdminUserId'],
      'slipAdminOfficeId' : slip['slipAdminOfficeId'],
      'slipAdminMechanicId' : slip['slipAdminMechanicId'],
      'adminDiv' : slip['adminDiv'],
      'title' : slip['title'],
      'price' : slip['price'],
      'bidMethod' : slip['bidMethod'],
      'bidderId' : slip['bidderId'],
      'bidEndDate' : slip['bidEndDate'],
      'explanation' : slip['explanation'],
      'serviceType' : slip['serviceType'],
      'targetVehicleId' : slip['targetVehicleId'],
      'targetVehicleName' : slip['targetVehicleName'],
      'targetVehicleInfo' : slip['targetVehicleInfo'],
      'workAreaInfo' : slip['workAreaInfo'],
      'evaluationId' : slip['evaluationId'],
      'completionDate' : slip['completionDate'],
      'transactionCompletionDate' : slip['transactionCompletionDate'],
      'thumbnailUrl' : slip['thumbnailUrl'],
      'imageUrlList' : slip['imageUrlList'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse