import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
serviceTransactionRequest = dynamodb.Table("serviceTransactionRequest")
userInfo = dynamodb.Table("userInfo")

# 取引依頼中ユーザーチェック
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))

  OperationType = event['OperationType']

  try:
    if OperationType == 'CHECKTRANSACTIONREQ':
      slipNo = event['Keys']['slipNo']
      requestUserId = event['Keys']['requestUserId']
      serviceType = event['Keys']['serviceType']

    print('LABEL_1')
    # 伝票番号から伝票取引依頼情報を取得
    transactionReqData = serviceTransactionRequest_query(slipNo)

    print('LABEL_2')    
    # 取引依頼がない場合処理を終了
    if len(transactionReqData) == 0 :
      return False

    # 取引依頼がある場合チェックを続行
    
    print('LABEL_3')
    # ユーザー情報を取得
    userInfo = userInfo_query(requestUserId)
    if len(userInfo) == 0 :
      return False

    print('LABEL_4')
    userData = userInfo[0]

    # 取引依頼者にユーザーが含まれるかをチェックする
    for item in transactionReqData :
      if item['serviceUserType'] == '0' :
        if item['requestUserId'] == userData['userId'] :
          return True
      if item['serviceUserType'] == '1' :
        if item['requestUserId'] == userData['officeId'] :
          return True
      if item['serviceUserType'] == '2' :
        if item['requestUserId'] == userData['mechanicId'] :
          return True
    print('LABEL_5')
    # 含まれない場合は申請者以外として判断する
    return False

  except Exception as e:
      print("Error Exception.")
      print(e)

# 取引依頼情報レコード検索
def serviceTransactionRequest_query(slipNo):
  queryData = serviceTransactionRequest.query(
      IndexName = 'slipNo-index',
      KeyConditionExpression = Key("slipNo").eq(slipNo)
  )
  items=queryData['Items']
  print(items)
  return items


# レコード検索
# ユーザー情報取得
def userInfo_query(requestUserId):
  # 認証情報チェック後ユーザーIDを取得
  # 引数
  input_event = {
      "userId": requestUserId,
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

  queryData = userInfo.query(
      KeyConditionExpression = Key("userId").eq(userId) & Key("userValidDiv").eq('0')
  )
  items=queryData['Items']
  print(items)
  return items

