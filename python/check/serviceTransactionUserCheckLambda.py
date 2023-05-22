import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
transactionSlip = dynamodb.Table("transactionSlip")
userInfo = dynamodb.Table("userInfo")

# 取引中ユーザーチェック
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))

  OperationType = event['OperationType']

  try:
    if OperationType == 'CHECKTRANSACTION':
      slipNo = event['Keys']['slipNo']
      slipServiceType = event['Keys']['slipServiceType']
      userId = event['Keys']['userId']

    # 伝票番号から伝票取引情報を取得
    transactionData = serviceTransaction_query(slipNo, slipServiceType)
    
    # 取引依頼がない場合処理を終了
    if len(transactionData) == 0 :
      return False

    # 取引依頼がある場合チェックを続行
    
    # ユーザー情報を取得
    userInfo = userInfo_query(requestUserId)
    if len(userInfo) == 0 :
      return False

    userData = userInfo[0]

    # 取引依頼者にユーザーが含まれるかをチェックする
    for data in transactionData :
      if item['serviceType'] == '0' :
        if item['userId'] == userData['useId'] :
          return True
      if item['serviceType'] == '1' :
        if item['officeId'] == userData['officeId'] :
          return True
      if item['serviceType'] == '2' :
        if item['mechanicId'] == userData['mechanicId'] :
          return True

    # 含まれない場合は申請者以外として判断する
    return False

  except Exception as e:
      print("Error Exception.")
      print(e)

# レコード検索
def serviceTransaction_query(slipNo, serviceType):
    queryData = transactionSlip.query(
        KeyConditionExpression = Key("slipNo").eq(slipNo) & Key("serviceType").eq(serviceType)
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
      "userId": adminId,
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

  queryData = table.query(
      KeyConditionExpression = Key("userId").eq(partitionKey) & Key("userValidDiv").eq('0')
  )
  items=queryData['Items']
  print(items)
  return items

