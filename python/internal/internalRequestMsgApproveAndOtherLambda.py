import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
userMyList = dynamodb.Table("userMyList")
serviceTransactionRequest = dynamodb.Table("serviceTransactionRequest")
transactionSlip = dynamodb.Table("transactionSlip")
userInfo = dynamodb.Table("userInfo")
officeInfo = dynamodb.Table("officeInfo")
mechanicInfo = dynamodb.Table("mechanicInfo")

# 取引依頼処理にて承認された依頼者とその他の依頼者への処理を実施する
def lambda_handler(event, context) :
  print("Received event: " + json.dumps(event))

  requestData = event['requestData']
  slipInfo = event['slipInfo']

  try:
    # 承認された依頼情報のmsg処理を行う
    print('LABEL_1')
    res1 = approveRequestUserMsg(requestData, slipInfo)
    if res1 != 200 :
      print('approveRequestUserMsg_Failure')
      return 400

    # その他の依頼情報を取得
    print('LABEL_2')
    requestList = transactionReqSlipNo_query(slipInfo['slipNo']) 
    if len(requestList) == 0 :
      print('transactionSlipNo_query_Failure')
      return 400
    
    print('LABEL_3')

    for req in requestList :
      # 承認者を除く依頼のみ処理
      if req['requestUserId'] != requestData['requestUserId'] :
        otherReqMsg(req, slipInfo) 


    # ここまで正常に完了
    return 200

  except Exception as e:
      print("Error Exception.")
      print(e)


# 承認依頼者のメッセージ処理
def approveRequestUserMsg(requestData, slipInfo) :
  print('LABEL_4')
  # ユーザー情報を取得
  userInfo = getUserInfo(requestData)
  if len(userInfo) == 0 :
    return 500
  print('LABEL_5')
  # マイリストにMsg登録
  msg = 'TRAN_START'
  category = '15'
  msgResult = sendMsg_query(requestData, userInfo[0], slipInfo, msg, category)
  if msgResult != 200 :
    return msgResult
  print('LABEL_6')
  # 取引伝票TBLに新規登録
  tranSlipRes = initTransactionSlip_query(userInfo[0], slipInfo)
  if tranSlipRes != 200 :
    return tranSlipRes

  return 200


# 伝票番号に紐づく取引依頼TBL情報取得
def transactionReqSlipNo_query(partitionKey) :
  print('LABEL_7')
  queryData = serviceTransactionRequest.query(
      IndexName = 'slipNo-index',
      KeyConditionExpression = Key("slipNo").eq(partitionKey)
  )
  items=queryData['Items']
  print('LABEL_8')
  print(items)
  return items

# その他依頼者へのメッセージ処理を行う
def otherReqMsg(req, slipInfo) :
  print('LABEL_9')
  # 依頼情報を更新
  putRes = putOtherReq_query(req)
  if putRes != 200 :
    return putRes
  print('LABEL_10')
  # ユーザー情報を取得
  userInfo = getUserInfo(req)
  if len(userInfo) == 0 :
    return 500

  print('LABEL_11')
  # マイリストにMsg登録
  msg = 'UNSUCCESSFUL'
  category = '16'
  msgResult = sendMsg_query(req, userInfo[0], slipInfo, msg, category)
  if msgResult != 200 :
    return msgResult


# ユーザーマイリストTBLメッセージ登録
def sendMsg_query(request, userInfo, slipInfo, msg ,category):


  # マイリスト用のリクエスト情報生成
  requestInfo = {
    "requestId": request['id'],
    "requestType": '0',
    "requestTargetId": request['slipNo'],
    "requestTargetName": slipInfo['title'],
  }


  mechanicId = userInfo['mechanicId']
  if mechanicId == None :
    mechanicId = '0'

  officeId = userInfo['officeId']
  if officeId == None :
    officeId = '0'
  print(request)

  putResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : userInfo['userId'],
      'mechanicId' : mechanicId,
      'officeId' : officeId,
      'serviceType' : slipInfo['serviceType'],
      'slipNo' : slipInfo['slipNo'],
      'serviceTitle' : slipInfo['title'],
      'category' : category,
      'message' : msg,
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


# 取引依頼TBL(依頼者(確定以外)データ更新)
def putOtherReq_query(item):
  print('BUG_CHECK')
  print(item)
  # 取引依頼TBL(管理者)
  putResponse = serviceTransactionRequest.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'requestUserName' : item['requestUserName'],
      'serviceUserType' : item['serviceUserType'],
      'requestType' : item['requestType'],
      'files' : item['files'],
      'requestStatus' : item['requestStatus'],
      'confirmDiv' : '9',
      'deadline' : item['deadline'],
      'created' : item['created'],
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  return putResponse['ResponseMetadata']['HTTPStatusCode'] 


# ユーザー情報を取得する
def getUserInfo(requestData) :
  print('BUG_CHECK_2')
  print(requestData)
  if requestData['serviceUserType'] == '0' :
    userId = requestData['requestUserId']
  elif requestData['serviceUserType'] == '1' :
    userId = getOfficeUser(requestData['requestUserId'])
  else:
    userId = getMechanicUser(requestData['requestUserId'])    

  # ユーザー情報を取得
  queryData = userInfo.query(
      KeyConditionExpression = Key("userId").eq(userId) & Key("userValidDiv").eq('0')
  )
  items=queryData['Items']
  return items


# 工場情報からユーザーIDを取得する
def getOfficeUser(officeId) :
  queryData = officeInfo.query(
      KeyConditionExpression = Key("officeId").eq(officeId)
  )
  items=queryData['Items']
  if len(items) == 0 :
    return None
  mechanicInfoList = items[0]['connectionMechanicInfo']
  # （仮）工場の関連メカニック情報の先頭が管理者となるためそのユーザー情報を取得
  return getMechanicUser(mechanicInfoList[0]['mechanicId'])


# メカニック情報からユーザーIDを取得する
def getMechanicUser(mechanicid) :
  queryData = mechanicInfo.query(
      KeyConditionExpression = Key("mechanicId").eq(mechanicid)
  )
  items=queryData['Items']
  if len(items) == 0 :
    return None
  return items[0]['adminUserId']



# 取引中伝票情報新規登録（取引依頼の確定者）
def initTransactionSlip_query(userInfo, slipInfo) :

  mechanicId = '0'
  if userInfo['mechanicId'] != None and userInfo['mechanicId'] !=  '0' :
    mechanicId = userInfo['mechanicId']

  officeId = '0'
  if userInfo['officeId'] != None and userInfo['officeId'] !=  '0' :
    officeId = userInfo['officeId']

  putResponse = transactionSlip.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'serviceType' : slipInfo['serviceType'],
      'userId' : userInfo['userId'],
      'mechanicId' : mechanicId,
      'officeId' : officeId,
      'slipNo' : slipInfo['slipNo'],
      'serviceTitle' : slipInfo['title'],
      'slipRelation' : '3',
      'slipAdminId' : slipInfo['slipAdminUserId'],
      'slipAdminName' : '',
      'bidderId' : slipInfo['bidderId'],
      'deleteDiv' : '0',
      'completionScheduledDate' : 0,
      'ttlDate' : 0,
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  return putResponse['ResponseMetadata']['HTTPStatusCode']

