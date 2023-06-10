import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
slipDetailInfo = dynamodb.Table("slipDetailInfo")
salesServiceInfo = dynamodb.Table("salesServiceInfo")
transactionSlip = dynamodb.Table("transactionSlip")
completionSlip = dynamodb.Table("completionSlip")

userInfo = dynamodb.Table("userInfo")
officeInfo = dynamodb.Table("officeInfo")
mechanicInfo = dynamodb.Table("mechanicInfo")

# 内部処理 引数に指定された操作で伝票の工程ステータス遷移処理を行う
def lambda_handler(event, context) :
  print("Received event: " + json.dumps(event))

  try:
    slipNo = event['slipNo']
    serviceType = event['serviceType']
    processStatus = event['processStatus']

    print('LABEL_1')    
    # 対象伝票のステータスを更新する
    slip = moveProcessStatus(slipNo, serviceType, processStatus)
    if slip == None :
      print('moveprocess_Failure')
      return 500

    print('LABEL_2')
    # 取引開始の場合は購入者情報に取引者のIDを登録
    if processStatus == '1' :
      print('LABEL_2.5')
      reqData = event['transactionReq']
      if reqData == None :
        print('None_reqData_moveprocess_Failure')
        return 500
      print('LABEL_2.6')
      tranSlip = setBidUser(slip, serviceType, reqData)
      if tranSlip != 200 :
        print('LABEL_2.7')
        print('setBidUser_moveprocess_Failure')
        return 500

    print('INTERNALMOVESLIPPROCESSSTATUSLAMBDA_Successed')
    print('LABEL_3')
    return 200

  except Exception as e:
      print("Error Exception.")
      print(e)


# 対象の伝票情報を取得
def moveProcessStatus(slipNo, serviceType, processStatus):

  if serviceType == '0' :
    print('LABEL_4')
    return slipDitailStatusMove_query(slipNo, processStatus)
  else :
    print('LABEL_5')
    return salesServiceStatusMove_query(slipNo, processStatus)


# 伝票情報のステータス操作
def slipDitailStatusMove_query(slipNo, processStatus) :
  # 対象の伝票情報取得
  queryData = slipDetailInfo.query(
      KeyConditionExpression = Key("slipNo").eq(slipNo) & Key("deleteDiv").eq("0")
  )
  print('LABEL_6')
  items = queryData['Items']
  if len(items) == 0 :
    print('Not_Target_Slip')
    return None

  print('LABEL_7')
  slip = items[0]
  slip['processStatus'] = processStatus
  slip['updated'] = datetime.now().strftime('%x %X')

  print('LABEL_8')
  # ステータスを更新
  putResponse = slipDetailInfo.put_item(
    Item= slip
  )

  print('LABEL_9')
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print('LABEL_10')
    print(putResponse)
    return None
  else:
    print('Post Successed.')

  print('LABEL_11')
  return slip


# サービス商品のステータス操作
def salesServiceStatusMove_query(slipNo, processStatus) :
  # 対象の伝票情報取得
  queryData = salesServiceInfo.query(
      KeyConditionExpression = Key("slipNo").eq(slipNo) & Key("deleteDiv").eq("0")
  )
  print('LABEL_12')
  items = queryData['Items']
  if len(items) == 0 :
    print('Not_Target_SalesService')
    return None

  print('LABEL_13')
  salesService = items[0]
  salesService['processStatus'] = processStatus
  salesService['updated'] = datetime.now().strftime('%x %X')

  print('LABEL_14')
  # ステータスを更新
  putResponse = salesServiceInfo.put_item(
    Item= salesService
  )

  print('LABEL_15')
  # putResponse = slipDetailInfo.put_item(salesService)

  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print('LABEL_16')
    return None
  else:
    print('Post Successed.')
  print('LABEL_17')
  return salesService


# 入札者（購入者）に取引者IDを設定する
def setBidUser(slip, serviceType, tranReq) :

  slip['bidderId'] = tranReq['requestUserId']
  slip['bidUserType'] = tranReq['serviceUserType']

  putResponse = 400
  if serviceType == '0' :
    putResponse = salesServiceInfo.put_item(Item= slip)
  else :
    putResponse = slipDetailInfo.put_item(Item= slip)

  return   putResponse['ResponseMetadata']['HTTPStatusCode']

