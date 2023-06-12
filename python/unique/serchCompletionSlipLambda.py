import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
completionSlip = dynamodb.Table("completionSlip")
userInfo = dynamodb.Table("userInfo")

# ユーザーに関連する完了済伝票情報を取得する
def lambda_handler(event, conte):
  print("Received event: " + json.dumps(event))
  IndexType = event['IndexType']
  accessUser = event['Keys']['accessUser']
  
  try:
    print('LABEL_1')
    if IndexType != 'SERCHCOMPLETIONSLIP':
      return None
    print('LABEL_2')

    resultData = []


    # ユーザー情報取得
    print('LABEL_3')
    userData = userInfo_query(accessUser)
    if len(userData) == 0 :
      return None
    userInfo = userData[0]

    print('LABEL_4')
    mechanicId = '0'
    if userInfo['mechanicId'] != None and userInfo['mechanicId'] != '0' :
      mechanicId = userInfo['mechanicId']


    print('LABEL_5')
    officeId = '0'  
    if userInfo['officeId'] != None and userInfo['officeId'] != '0' :
      officeId = userInfo['officeId']


    # ユーザーIDに紐づく情報取得
    print('LABEL_6')
    
    resultData = slipAdminUserId_query(userInfo['userId'])
    print(resultData)

    # メカニックIDに紐づく情報取得

    if mechanicId != '0' :
      print('LABEL_7')
      mcList = slipAdminMechanicId_query(mechanicId)
      resultData = listAppend(resultData, mcList)
      print(resultData)

    # 工場IDに紐づく情報取得
    if officeId != '0': 
      print('LABEL_9')
      fcList = slipAdminOffice_query(officeId)
      resultData = listAppend(resultData, fcList)
      print(resultData)

    # 取引者に紐づく情報取得
    print('LABEL_10')
    bidUserList = slipBidderId_query(userInfo['userId'])
    resultData = listAppend(resultData, bidUserList)

    print(resultData)
    
    if mechanicId != '0' :
      print('LABEL_11')
      bidMcList = slipBidderId_query(mechanicId)
      resultData = listAppend(resultData, bidMcList)
      print(resultData)

    if officeId != '0' :
      print('LABEL_12')
      bidfcList = slipBidderId_query(officeId)
      resultData = listAppend(resultData, bidfcList)
      print(resultData)

    # 重複を削除
    result = list({item["slipNo"]: item for item in resultData}.values())
    
    print(result)

    return result

  except Exception as e:
    print("Error Exception.")
    print(e)


# userId-indexレコード検索 slipAdminUserId-index
def slipAdminUserId_query(partitionKey):
    queryData = completionSlip.query(
        IndexName = 'slipAdminUserId-index',
        KeyConditionExpression = Key("slipAdminUserId").eq(partitionKey)
    )
    items=queryData['Items']
    return items

# officeId-indexレコード検索 slipAdminOfficeId-index
def slipAdminOffice_query(partitionKey):
    queryData = completionSlip.query(
        IndexName = 'slipAdminOfficeId-index',
        KeyConditionExpression = Key("slipAdminOfficeId").eq(partitionKey)
    )
    items=queryData['Items']
    return items

# mechanicId-indexレコード検索 slipAdminMechanicId-index
def slipAdminMechanicId_query(partitionKey):
    queryData = completionSlip.query(
        IndexName = 'slipAdminMechanicId-index',
        KeyConditionExpression = Key("slipAdminMechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    return items

# bidderId-indexレコード検索 slipAdminMechanicId-index
def slipBidderId_query(partitionKey):
    queryData = completionSlip.query(
        IndexName = 'bidderId-index',
        KeyConditionExpression = Key("bidderId").eq(partitionKey)
    )
    items=queryData['Items']
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

  #ユーザーTBLを検索
  queryData = userInfo.query(
    KeyConditionExpression = Key("userId").eq(userId) & Key("userValidDiv").eq('0')
  )
  return queryData['Items']


# リストを結合する
def listAppend(list1, list2) :
  for item in list2 :
    list1.append(item)
  return list1


