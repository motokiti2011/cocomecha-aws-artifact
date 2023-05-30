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
mechanicInfo = dynamodb.Table("mechanicInfo")
officeInfo = dynamodb.Table("officeInfo")
userInfo = dynamodb.Table("userInfo")

# 取引依頼送信Lambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)

  OperationType = event['OperationType']

  slipNo = event['Keys']['slipNo']
  serviceType = event['Keys']['serviceType']
  requestUserId = event['Keys']['requestUserId']
  serviceUserType = event['Keys']['serviceUserType']

  try:
    if OperationType != 'TRANSACTIONREQUEST':
      print('TRANSACTIONREQUEST_Failure_0')
      return 403
    print('LABEL_1')
    # ユーザー情報を取得
    userInfo = userInfo_query(requestUserId)
    if len(userInfo) == 0 :
      print('TRANSACTIONREQUEST_Failure_1')
      return 404
    print('LABEL_2')
    # 対象の伝票情報を取得
    slip = getSlip(slipNo, serviceType)
    if len(slip) == 0 :
      print('TRANSACTIONREQUEST_Failure_2')
      return 404
    print('LABEL_3')
    # 取引中伝票情報は廃止
    print('LABEL_4')
    # 管理者のマイリストTBLにMsg登録
    resAdminMyList = AdminMyListMsg(userInfo[0], slip[0], serviceUserType, serviceType)
    if resAdminMyList != 200 :
      print('TRANSACTIONREQUEST_Failure_4')
      return 404
    print('LABEL_5')
    # 取引依頼者のマイリストTBLにMsg登録
    resReqMyList = requestMyListMsg(userInfo[0], slip[0], serviceUserType, reqRes, serviceType)
    if resReqMyList != 200 :
      print('TRANSACTIONREQUEST_Failure_5')
      return 404
    print('LABEL_6')    
    print('TRANSACTIONREQUEST_Successed')
    return 200

  except Exception as e:
      print("Error Exception.")
      print(e)

# 取引依頼TBLレコード登録
def post_transactionReq(userInfo, slip, serviceType, serviceUserType):

  now = datetime.now()
  id = str(uuid.uuid4())

  requestUserId = userInfo['userId']
  requestUserName = userInfo['userName']
  print(serviceUserType)
  print('serviceUserType')
  # ユーザー以外が依頼者の場合情報を取得
  if serviceUserType == 1 :
    print('office_query:' +userInfo['officeId'] )
    fcData = office_query(userInfo['officeId'])
    requestUserId = fcData[0]['officeId']
    requestUserName = fcData[0]['officeName']

  elif serviceUserType == 2 :
    print('mechanic_query:' +userInfo['mechanicId'] )
    mcData = mechanic_query(userInfo['mechanicId'])
    requestUserId = mcData[0]['mechanicId']
    requestUserName = mcData[0]['mechanicName']

  putResponse = serviceTransactionRequest.put_item(
    Item={
      'id' : id,
      'slipNo' : slip['slipNo'],
      'requestUserId' : requestUserId,
      'requestUserName' : requestUserName,
      'serviceUserType' : serviceUserType,
      'requestType' : '0',
      'files' : None,
      'requestStatus' : '0',
      'confirmDiv' : '0',
      'deadline' : slip['preferredDate'],
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  print('mechanic_query:1' )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return None
  else:
    print('Post Successed.')
    return id


# 伝票管理者のマイリストTBLの登録
def AdminMyListMsg(userInfo, slip, serviceUserType, serviceType):

  mechanicId = '0'
  officeId = '0'
  if serviceUserType != '0': 
    mechanicId = slip['slipAdminMechanicId']
    officeId = slip['slipAdminOfficeId']

  # 伝票管理者
  userMyListAdminResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' :slip['slipAdminUserId'],
      'mechanicId' :mechanicId,
      'officeId' : officeId,
      'serviceType' : serviceType,
      'slipNo' : slip['slipNo'],
      'serviceTitle' : slip['title'],
      'category' : '7',
      'message' : 'TRAN_RES',
      'readDiv' : '0',
      'messageDate' : datetime.now().strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')

    }
  )
  
  if userMyListAdminResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListAdminResponse)
    return userMyListAdminResponse['ResponseMetadata']['HTTPStatusCode']
  else:
    print('Post Successed.')
    return 200


# 取引依頼者のマイリストTBLにメッセージ登録
def requestMyListMsg(userInfo, slip, serviceUserType, reqestId, serviceType):

  requestInfo = {
    'requestId' : reqestId,
    'requestType' : '0',
    'requestTargetId' : slip['slipNo'],
    'requestTargetName' : 'TRAN_REQ',
  }
  print(userInfo)
  mechanicId = userInfo['mechanicId']
  if mechanicId == None :
    mechanicId = '0'
  officeId = userInfo['officeId']
  if officeId == None :
    officeId = '0'

  userMyListResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : userInfo['userId'],
      'mechanicId' : mechanicId,
      'officeId' : officeId,
      'serviceType' : serviceType,
      'slipNo' : slip['slipNo'],
      'serviceTitle' : slip['title'],
      'category' : '13',
      'message' : 'TRAN_REQ',
      'readDiv' : '0',
      'messageDate' : datetime.now().strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo': requestInfo ,
      'deleteDiv' : '0',
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')

    }
  )
  
  if userMyListResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListResponse)
    return userMyListResponse['ResponseMetadata']['HTTPStatusCode']
  else:
    print('Post Successed.')
    return 200


# メカニック情報を取得
def mechanic_query(mechanicId):
  print('01')
  print(mechanicId)
  queryData = mechanicInfo.query(
    KeyConditionExpression = Key("mechanicId").eq(mechanicId)
  )
  items=queryData['Items']
  print(items)
  return items

# 工場情報を取得
def office_query(officeId):
  print(officeId)
  queryData = officeInfo.query(
    KeyConditionExpression = Key("officeId").eq(officeId)
  )
  items=queryData['Items']
  print(items)
  return items

# 取引依頼ユーザー情報取得
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
    return []
  
  #ユーザーTBLを検索
  queryData = userInfo.query(
    KeyConditionExpression = Key("userId").eq(userId) & Key("userValidDiv").eq('0')
  )
  return queryData['Items']


# 対象の伝票情報取得
def getSlip(slipNo, serviceType) :
  if serviceType == '0' :
    return slipDetail_query(slipNo)
  else :
    return salesService_query(slipNo)


# 伝票情報取得
def slipDetail_query(slipNo) :
  queryData = slipDetailInfo.query(
      KeyConditionExpression = Key("slipNo").eq(slipNo) & Key("deleteDiv").eq("0")
  )
  items=queryData['Items']
  print(items)
  return items


# サービス商品情報取得
def salesService_query(slipNo) :
  queryData = salesServiceInfo.query(
      KeyConditionExpression = Key("slipNo").eq(slipNo) & Key("deleteDiv").eq("0")
  )
  items=queryData['Items']
  print(items)
  return items
