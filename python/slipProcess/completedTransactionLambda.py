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
    adminDiv = False
    requestDiv = False
    # 伝票管理者チェック
    if  userInfo['userId'] != slipData[0]['slipAdminUserId'] :
      # アクセス者が管理者でない場合、依頼者チェックを行う
      requestDiv = requestAcceseCheck(slipNo, userInfo)
      if requestDiv :
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
      print('BUG_1')
      adminUserInfo = userInfo
      transactionUserInfo = transactionUser_query(slipNo)
    else :
      print('BUG_2')
      transactionUserInfo = userInfo
      adminUserInfo = userId_query(slipData[0]['slipAdminUserId'])

    print('LABEL_5')
    print(adminUserInfo)
    # 管理者へのマイリストへのMsg登録
    postMyListResult = postAdminMyList(adminUserInfo , slipData[0]) 
    if postMyListResult != 200 :
      print('PostMyList_Failure')
      return 400

    print('LABEL_6')
    print(transactionUserInfo)
    # 取引者へのマイリストへのMsg登録
    postTranMyListResult = postAdminMyList(transactionUserInfo, slipData[0]) 
    if postTranMyListResult != 200 :
      print('PostMyList_Failure')
      return 400


    print('LABEL_7')
    # 完了済伝票情報の登録
    # 管理者
    compRes = compSlip_query(slipData[0], adminUserInfo, transactionUserInfo)
    if compRes != 200 :
      print('Not_compRes_Failure')
      return 400
    
    print('LABEL_8')
    # 取引中伝票を取得
    queryResult = tran_query(slipNo, serviceType)
    if len(queryResult) == 0 :
      print('Not_compRes_Failure')
      return 400

    # 取引中伝票を論理削除
    print('LABEL_9')
    res = tran_logcal_del(queryResult)
    if res != 200 :
      print('Not_compRes_Failure')
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
def postAdminMyList(userInfo, slipData) :

  # マイリスト用のリクエスト情報生成
  requestInfo = {
    "requestId": slipData['slipNo'],
    "requestType": '0',
    "requestTargetId": slipData['slipNo'],
    "requestTargetName": slipData['title'],
  }

  mechanicId = userInfo['mechanicId']
  if mechanicId == None :
    mechanicId = '0'

  officeId = userInfo['officeId']
  if officeId == None :
    officeId = '0'

  putResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : userInfo['userId'],
      'mechanicId' : mechanicId,
      'officeId' : officeId,
      'serviceType' : slipData['serviceType'],
      'slipNo' : slipData['slipNo'],
      'serviceTitle' : slipData['title'],
      'category' : '17',
      'message' : 'TRAN_COMP',
      'readDiv' : '0',
      'messageDate' : datetime.now().strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : requestInfo,
      'deleteDiv' : '0',
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  return putResponse['ResponseMetadata']['HTTPStatusCode']



# 取引依頼者チェック
def requestAcceseCheck(slipNo, userInfo):
  # 取引依頼情報取得
  res = transactionRequest_query(slipNo)

  # 取得できない場合エラー
  if len(res) == 0 :
    print('transactionRequest_query_None')
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
  print('BUG_3_1')
  print(slipNo)
  tranReqList = transactionRequest_query(slipNo)

  print('BUG_3')
  print(slipNo)
  print(tranReqList)

  reqId = None

  for item in tranReqList :
    if item['confirmDiv'] == '1' :
      reqId = item['requestUserId']
      userType = item['serviceUserType']

    if reqId == None :
      return None
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
def compSlip_query(slip, userInfo, transactionUserInfo):

  now = datetime.now()

  putResponse = completionSlip.put_item(
    Item={
      'slipNo' : slip['slipNo'],
      'userId' : userInfo['userId'],
      'serviceType' : slip['serviceType'],
      'slipAdminUserId' : slip['slipAdminUserId'],
      'slipAdminOfficeId' : slip['slipAdminOfficeId'],
      'slipAdminMechanicId' : slip['slipAdminMechanicId'],
      'adminDiv' : slip['adminDiv'],
      'title' : slip['title'],
      'price' : slip['price'],
      'bidMethod' : slip['bidMethod'],
      'bidUserType':  slip['bidUserType'],
      'bidderId' : transactionUserInfo['userId'],
      'bidEndDate' : slip['bidEndDate'],
      'explanation' : slip['explanation'],
      'serviceType' : slip['serviceType'],
      'targetVehicleId' : slip['targetVehicleId'],
      'targetVehicleName' : slip['targetVehicleName'],
      'targetVehicleInfo' : slip['targetVehicleInfo'],
      'workAreaInfo' : slip['workAreaInfo'],
      'evaluationId' : '0',
      'completionDate' : slip['completionDate'],
      'transactionCompletionDate' : now.strftime('%Y%m%d') ,
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
  return putResponse['ResponseMetadata']['HTTPStatusCode']




# 取引中の伝票情報を取得
def tran_query(slipNo, serviceType) :
  queryData = transactionSlip.query(
      IndexName = 'slipNo-index',
      KeyConditionExpression = Key("slipNo").eq(slipNo) & Key("serviceType").eq(serviceType)
  )
  items=queryData['Items']
  print(items)
  return items


# 取引中伝票情報を論理削除する
def tran_logcal_del(queryResult) :
  for item in queryResult :
    item['deleteDiv'] = '1'
    item['updated'] = datetime.now().strftime('%x %X')
    putResponse = transactionSlip.put_item(Item=item)
    
    # 問題発生時途中で処理終了
    if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
      return putResponse['ResponseMetadata']['HTTPStatusCode']

  return putResponse['ResponseMetadata']['HTTPStatusCode']

