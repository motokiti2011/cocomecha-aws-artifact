import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
salesServiceInfo = dynamodb.Table("salesServiceInfo")
slipDetailInfo = dynamodb.Table("slipDetailInfo")
transactionSlip = dynamodb.Table("transactionSlip")


# スケジュールバッチ 確定サービス移行
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  print('CONFIRMMIGRATIONSERVICE')

  try:    
    # 伝票チェック
    confirmSlipData = slip_confirm()

    # 対象伝票が存在する場合
    if len(confirmSlipData) > 0 :

        for slip in confirmSlipData :
          # 対象伝票を削除(保留)
          #slipconfirm_delete(slip['slipNo'])
          # 対象伝票を取引中伝票に追加
          slipconfirm_post(slip)

    # サービス商品チェック
    confirmServiceData = service_confirm()

    if len(confirmServiceData) > 0 :
    # 対象サービスが存在する場合削除
        for service in confirmServiceData :
          # 対象サービスを削除(保留)
          #serviceconfirm_delete(service['slipNo'])
          # 対象サービスを取引中伝票に追加
          serviceconfirm_post(service)

  except Exception as e:
      print("Error Exception.")
      print(e)


# 伝票情報確定伝票抽出
def slip_confirm():
    queryData = slipDetailInfo.query(
        IndexName = 'processStatus-index',
        # 「取引中」のステータスが残っている場合抽出
        KeyConditionExpression = Key("processStatus").eq("1")
    )
    items=queryData['Items']
    print(items)
    return items

# サービス商品情報抽出
def service_confirm():
    queryData = salesServiceInfo.query(
        IndexName = 'processStatus-index',
        # 「取引中」のステータスが残っている場合抽出
        KeyConditionExpression = Key("processStatus").eq("1")
    )
    items=queryData['Items']
    print(items)
    return items


# 伝票情報削除
#def slipconfirm_delete(slipNo):
#    delResponse = slipDetailInfo.delete_item(
#       Key={
#           'slipNo': slipNo,
#       }
#    )
#    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
#        print(delResponse)
#
# サービス商品削除
#def serviceconfirm_delete(slipNo):
#    delResponse = salesServiceInfo.delete_item(
#       Key={
#           'slipNo': slipNo,
#       }
#    )
#    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
#        print(delResponse)


# 取引中伝票情報に伝票情報を追加
def slipconfirm_post(slip):
  putResponse = transactionSlip.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'serviceType' : '0',
      'userId' : slip['slipAdminUserId'],
      'mechanicId' : '0',
      'officeId' : '0',
      'slipNo' : slip['slipNo'],
      'serviceTitle' : slip['title'],
      'slipRelation' : '0',
      'slipAdminId' : slip['slipAdminUserId'],
      'slipAdminName' : '',
      'bidderId' : slip['bidderId'],
      'deleteDiv' : '0',
      'completionScheduledDate' : 0,
      'ttlDate' : 0,
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)


# 取引中伝票情報にサービス情報を追加
def serviceconfirm_post(service):

  adminId = service['slipAdminUserId']
  if  service['serviceType'] == 2:
    adminId = service['slipAdminOfficeId']
  elif service['serviceType'] == 3:
    adminId = service['slipAdminMechanicId']

  putResponse = transactionSlip.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'serviceType' : service['serviceType'],
      'userId' : service['slipAdminUserId'],
      'mechanicId' : service['slipAdminMechanicId'],
      'officeId' : service['slipAdminOfficeId'],
      'slipNo' : service['slipNo'],
      'serviceTitle' : service['title'],
      'slipRelation' : '0',
      'slipAdminId' : adminId,
      'slipAdminName' :  '',
      'bidderId' : service['bidderId'],
      'deleteDiv' : '0',
      'completionScheduledDate' : 0,
      'ttlDate' : 0,
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)


