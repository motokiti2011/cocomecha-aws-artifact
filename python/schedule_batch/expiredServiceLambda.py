import json
import boto3
import uuid

from datetime import datetime
import random

from boto3.dynamodb.conditions import Key

# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
salesServiceInfo = dynamodb.Table("salesServiceInfo")
slipDetailInfo = dynamodb.Table("slipDetailInfo")
userMyList = dynamodb.Table("userMyList")


# 確定サービス移行
# スケジュールバッチ 期限切れ伝票チェック
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  print('EXPIREDSERVICE')
  try:
    # 伝票チェック
    expiredSlipData = slip_confirm()

    # 対象伝票が存在する場合
    if len(expiredSlipData) > 0 :
      for slip in expiredSlipData :
        # 対象伝票のステータスを更新
        expiredSlip_query(slip)
        # マイリストTBLにメッセージを追加（期限切れ）
        slipMylistMsg_query(slip['slipNo'])

    # サービス商品チェック
    expiredServiceData = service_confirm()
    if len(expiredServiceData) > 0 :
    # 対象サービスが存在する場合削除
      for service in expiredServiceData :
        # 対象サービスのステータスを更新
        expiredService_query(service)
        # マイリストTBLにメッセージを追加（期限切れ）
        serviceMylistMsg_query(service)

  except Exception as e:
      print("Error Exception.")
      print(e)


# 伝票情報確定伝票抽出
def slip_confirm():

    # TIMESTAMP = get_timestamp()
    TIMESTAMP = datetime.now().strftime('%Y%m%d')
    print('TIMESTAMP')
    print(TIMESTAMP)
    
    queryData = slipDetailInfo.query(
        IndexName = 'preferredDate-index',
        # 「取引中」のステータスが残っている場合抽出
        KeyConditionExpression = Key("processStatus").eq("0")
        & Key("preferredDate").lt(int(TIMESTAMP))
    )
    items=queryData['Items']
    print('1')
    print(items)
    return items

# サービス商品情報抽出
def service_confirm():
    # TIMESTAMP = get_timestamp()
    TIMESTAMP = datetime.now().strftime('%Y%m%d')
    queryData = salesServiceInfo.query(
        IndexName = 'preferredDate-index',
        # 「出品中」のステータスが残っている場合抽出
        KeyConditionExpression = Key("processStatus").eq("0")
        & Key("preferredDate").lt(int(TIMESTAMP))
    )
    items=queryData['Items']
    print('2')
    print(items)
    return items


# 取引中伝票情報に伝票情報を追加
def expiredSlip_query(slip):
  putResponse = slipDetailInfo.put_item(
    Item={
      'slipNo' : PartitionKey,
      'deleteDiv' : slip['deleteDiv'],
      'category' : slip['category'],
      'slipAdminUserId' : slip['slipAdminUserId'],
      'adminDiv' : slip['adminDiv'],
      'title' : slip['title'],
      'areaNo1' : slip['areaNo1'],
      'areaNo2' : slip['areaNo2'],
      'price' : slip['price'],
      'bidMethod' : slip['bidMethod'],
      'bidderId' : slip['bidderId'],
      'bidEndDate' : slip['bidEndDate'],
      'explanation' : slip['explanation'],
      'displayDiv' : slip['displayDiv'],
      'processStatus' : '3',
      'targetService' : slip['targetService'],
      'targetVehicleId' : slip['targetVehicleId'],
      'targetVehicleName' : slip['targetVehicleName'],
      'targetVehicleInfo' : slip['targetVehicleInfo'],
      'workAreaInfo' : slip['workAreaInfo'],
      'preferredDate' : slip['preferredDate'],
      'preferredTime' : slip['preferredTime'],
      'completionDate' : slip['completionDate'],
      'transactionCompletionDate' : slip['transactionCompletionDate'],
      'thumbnailUrl' : slip['thumbnailUrl'],
      'imageUrlList' : slip['imageUrlList'],
      'messageOpenLebel' : slip['messageOpenLebel'],
      'updateUserId' : slip['updateUserId'],
      'created' : slip['created'],
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)


# 取引中伝票情報にサービス情報を追加
def expiredService_query(service):

  putResponse = salesServiceInfo.put_item(
    Item={
      'slipNo' : service['slipNo'],
      'deleteDiv' : service['deleteDiv'],
      'category' : service['category'],
      'slipAdminUserId' : service['slipAdminUserId'],
      'slipAdminOfficeId' : service['slipAdminOfficeId'],
      'slipAdminMechanicId' : service['slipAdminMechanicId'],
      'adminDiv' : service['adminDiv'],
      'title' : service['title'],
      'areaNo1' : service['areaNo1'],
      'areaNo2' : service['areaNo2'],
      'price' : service['price'],
      'bidMethod' : service['bidMethod'],
      'bidderId' : service['bidderId'],
      'bidEndDate' : service['bidEndDate'],
      'explanation' : service['explanation'],
      'displayDiv' : service['displayDiv'],
      'processStatus' : '3',
      'targetService' : service['targetService'],
      'targetVehicleId' : service['targetVehicleId'],
      'targetVehicleName' : service['targetVehicleName'],
      'targetVehicleInfo' : service['targetVehicleInfo'],
      'workAreaInfo' : service['workAreaInfo'],
      'preferredDate' : service['preferredDate'],
      'preferredTime' : service['preferredTime'],
      'completionDate' : service['completionDate'],
      'transactionCompletionDate' : service['transactionCompletionDate'],
      'thumbnailUrl' : service['thumbnailUrl'],
      'imageUrlList' : service['imageUrlList'],
      'messageOpenLebel' : service['messageOpenLebel'],
      'updateUserId' : service['updateUserId'],
      'created' : service['created'],
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)



# ユーザーマイリストTBL伝票(期限切れメッセージ登録)
def slipMylistMsg_query(slip):

  now = datetime.now()

  putResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : slip['slipAdminUserId'],
      'mechanicId' : '0',
      'officeId' : '0',
      'serviceType' : '0',
      'slipNo' : slip['slipNo'],
      'serviceTitle' : slip['title'],
      'category' : '11',
      'message' : 'EXPIRED',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)


# ユーザーマイリストTBLサービス商品(期限切れメッセージ登録)
def serviceMylistMsg_query(serivice):

  now = datetime.now()

  putResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : serivice['slipAdminUserId'],
      'mechanicId' : serivice['slipAdminMechanicId'],
      'officeId' :serivice['slipAdminOfficeId'],
      'serviceType' : serivice['targetService'],
      'slipNo' : serivice['slipNo'],
      'serviceTitle' : serivice['title'],
      'category' : '11',
      'message' : 'EXPIRED',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)




# バッチ実行時のタイムスタンプ作成
def get_timestamp():
    now = datetime.now()    
    rand_minute = int(random.uniform(0, 59))
    rand_second = int(random.uniform(0, 59))
    nowTime = datetime(now.year, now.month, now.day, now.hour, rand_minute, rand_second)
    return int(nowTime.timestamp()) * 1000


