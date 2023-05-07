import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
transactionSlip = dynamodb.Table("transactionSlip")
slipDetailInfo = dynamodb.Table("slipDetailInfo")
salesServiceInfo = dynamodb.Table("salesServiceInfo")
userMyList = dynamodb.Table("userMyList")
completionSlip = dynamodb.Table("completionSlip")


# スケジュールバッチ 取引完了伝票の抽出
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  print('TRANSACTIONEND')

  try:
    # 取引完了日越え取引情報を抽出
    endTransaction = delete_transaction_query()
    if(len(endTransaction) > 0 :
      for service in endTransaction :
        # 取引情報を論理削除
        logcaldelete_query(service)
        if service['serviceType'] == '0':
          # 伝票情報を取得し論理削除する
          slip = slipDetailInfo_query(service['slipNo'])
          # 取引終了TBLに情報を登録する
          completionSlip_query(slip)
          # マイリストTBLにメッセージを設定する(取引完了メッセージ＋評価依頼メッセージ)
          setMyListMsg_query(slip)
        elif service['serviceType'] == '1' or '2':
          # サービス商品を取得し論理削除する
          salesService = salesServiceInfo_query(service['slipNo'])
          # 取引終了TBLに情報を登録する
          completionSalesService_query(salesService)
          # マイリストTBLにメッセージを設定する(取引完了メッセージ＋評価依頼メッセージ)
          setMyListMsgSales_query(salesService)
  except Exception as e:
      print("Error Exception.")
      print(e)


# 取引中伝票情報の削除対象の情報を抽出
def delete_transaction_query():

    TIMESTAMP = get_timestamp()

    queryData = transactionSlip.query(
        IndexName = 'ttlDate-index',
        KeyConditionExpression = Key("deleteDiv").eq("0") & Key("ttlDate").LT(TIMESTAMP)
    )
    items=queryData['Items']
    print(items)
    return items


# 伝票情報を抽出し論理削除する
def slipDetailInfo_query(partitionKey):

    TIMESTAMP = get_timestamp()

    queryData = slipDetailInfo.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey) & Key("deleteDiv").eq("0")
    )
    items=queryData['Items']

    putResponse = table.put_item(
      Item={
        'slipNo' : items['0']['slipNo'],
        'deleteDiv' : '1',
        'category' : items['0']['category'],
        'slipAdminUserId' : items['0']['slipAdminUserId'],
        'adminDiv' : items['0']['adminDiv'],
        'title' : items['0']['title'],
        'areaNo1' : items['0']['areaNo1'],
        'areaNo2' : items['0']['areaNo2'],
        'price' : items['0']['price'],
        'bidMethod' : items['0']['bidMethod'],
        'bidderId' : items['0']['bidderId'],
        'bidEndDate' : items['0']['bidEndDate'],
        'explanation' : items['0']['explanation'],
        'displayDiv' : items['0']['displayDiv'],
        'processStatus' : items['0']['processStatus'],
        'targetService' : items['0']['targetService'],
        'targetVehicleId' : items['0']['targetVehicleId'],
        'targetVehicleName' : items['0']['targetVehicleName'],
        'targetVehicleInfo' : items['0']['targetVehicleInfo'],
        'workAreaInfo' : items['0']['workAreaInfo'],
        'preferredDate' : items['0']['preferredDate'],
        'preferredTime' : items['0']['preferredTime'],
        'completionDate' : items['0']['completionDate'],
        'transactionCompletionDate' : items['0']['transactionCompletionDate'],
        'thumbnailUrl' : items['0']['thumbnailUrl'],
        'imageUrlList' : items['0']['imageUrlList'],
        'messageOpenLebel' : items['0']['messageOpenLebel'],
        'updateUserId' : items['0']['updateUserId'],
        'created' : items['0']['created'],
        'updated' : items['0']['updated']
    }
  )

    return items['0']


# サービス商品情報を抽出し論理削除する
def salesServiceInfo_query(primaryKey):

    TIMESTAMP = get_timestamp()

    queryData = salesServiceInfo.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey) & Key("deleteDiv").eq("0")
    )
    items=queryData['Items']

    putResponse = table.put_item(
      Item={
        'slipNo' : items['0']['slipNo'],
        'deleteDiv' : '1',
        'category' : items['0']['category'],
        'slipAdminUserId' : items['0']['slipAdminUserId'],
        'slipAdminOfficeId' : items['0']['slipAdminOfficeId'],
        'slipAdminMechanicId' : items['0']['slipAdminMechanicId'],
        'adminDiv' : items['0']['adminDiv'],
        'title' : items['0']['title'],
        'areaNo1' : items['0']['areaNo1'],
        'areaNo2' : items['0']['areaNo2'],
        'price' : items['0']['price'],
        'bidMethod' : items['0']['bidMethod'],
        'bidderId' : items['0']['bidderId'],
        'bidEndDate' : items['0']['bidEndDate'],
        'explanation' : items['0']['explanation'],
        'displayDiv' : items['0']['displayDiv'],
        'processStatus' : items['0']['processStatus'],
        'targetService' : items['0']['targetService'],
        'targetVehicleId' : items['0']['targetVehicleId'],
        'targetVehicleName' : items['0']['targetVehicleName'],
        'targetVehicleInfo' : items['0']['targetVehicleInfo'],
        'workAreaInfo' : items['0']['workAreaInfo'],
        'preferredDate' : items['0']['preferredDate'],
        'preferredTime' : items['0']['preferredTime'],
        'completionDate' : items['0']['completionDate'],
        'transactionCompletionDate' : items['0']['transactionCompletionDate'],
        'thumbnailUrl' : items['0']['thumbnailUrl'],
        'imageUrlList' : items['0']['imageUrlList'],
        'messageOpenLebel' : items['0']['messageOpenLebel'],
        'updateUserId' : items['0']['updateUserId'],
        'created' : items['0']['created'],
        'updated' : datetime.now()
      }
    )

    return items['0']


# 取引伝票情報論理削除
def logcaldelete_query(service):
  putResponse = transactionSlip.put_item(
    Item={
      'id' : service['id'],
      'serviceType' : service['serviceType'],
      'userId' : service['userId'],
      'mechanicId' : service['mechanicId'],
      'officeId' : service['officeId'],
      'slipNo' : service['slipNo'],
      'serviceTitle' : service['serviceTitle'],
      'slipRelation' : service['slipRelation'],
      'slipAdminId' : service['slipAdminId'],
      'slipAdminName' :  service['slipAdminName'],
      'bidderId' : service['bidderId'],
      'deleteDiv' : '1',
      'completionScheduledDate' : service['completionScheduledDate'],
      'ttlDate' : service['ttlDate'],
      'created' : event['Keys']['created'],
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)


# 取引完了伝票情報登録(伝票)
def completionSlip_query(slip):

  now = datetime.now()

  putResponse = transactionSlip.put_item(
    Item={
      'slipNo' : slip['slipNo'],
      'slipAdminUserId' : slip['slipAdminUserId'],
      'slipAdminOfficeId' : '0',
      'slipAdminMechanicId' : '0',
      'adminDiv' : slip['adminDiv'],
      'title' : slip['title'],
      'price' : slip['price'],
      'bidMethod' : slip['bidMethod'],
      'bidderId' : slip['bidderId'],
      'bidEndDate' : slip['bidEndDate'],
      'explanation' : slip['explanation'],
      'targetService' : slip['targetService'],
      'targetVehicleId' : slip['targetVehicleId'],
      'targetVehicleName' : slip['targetVehicleName'],
      'targetVehicleInfo' : slip['targetVehicleInfo'],
      'workAreaInfo' : slip['workAreaInfo'],
      'evaluationId' :'0',
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



# 取引完了伝票情報登録（サービス商品）
def completionSlip_query(service):

  now = datetime.now()

  putResponse = salesServiceInfo.put_item(
    Item={
      'slipNo' : service['slipNo'],
      'slipAdminUserId' : service['slipAdminUserId'],
      'slipAdminOfficeId' : service['slipAdminOfficeId'],
      'slipAdminMechanicId' : service['slipAdminMechanicId'],
      'adminDiv' : service['adminDiv'],
      'title' : service['title'],
      'price' : service['price'],
      'bidMethod' : service['bidMethod'],
      'bidderId' : service['bidderId'],
      'bidEndDate' : service['bidEndDate'],
      'explanation' : service['explanation'],
      'targetService' : service['targetService'],
      'targetVehicleId' : service['targetVehicleId'],
      'targetVehicleName' : service['targetVehicleName'],
      'targetVehicleInfo' : service['targetVehicleInfo'],
      'workAreaInfo' : service['workAreaInfo'],
      'evaluationId' :'0',
      'completionDate' : service['completionDate'],
      'transactionCompletionDate' : service['transactionCompletionDate'],
      'thumbnailUrl' : service['thumbnailUrl'],
      'imageUrlList' : service['imageUrlList'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )

  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)



# ユーザーマイリストTBL伝票(取引完了メッセージ＋評価依頼メッセージ)
def setMyListMsg_query(slip):

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
      'category' : '17',
      'message' : 'TRAN_COMP',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse2['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)

  putResponse2 = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : slip['slipAdminUserId'],
      'mechanicId' : '0',
      'officeId' : '0',
      'serviceType' : '0',
      'slipNo' : slip['slipNo'],
      'serviceTitle' : slip['title'],
      'category' : '21',
      'message' : 'EVALUATION_REQ',
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


# ユーザーマイリストTBL伝票(取引完了メッセージ＋評価依頼メッセージ)
def setMyListMsgSales_query(service):

  now = datetime.now()

  putResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : service['slipAdminUserId'],
      'mechanicId' : service['slipAdminMechanicId'],
      'officeId' : service['slipAdminOfficeId'],
      'serviceType' : service['targetService'],
      'slipNo' : service['slipNo'],
      'serviceTitle' : service['title'],
      'category' : '17',
      'message' : 'TRAN_COMP',
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

  putResponse2 = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : service['slipAdminUserId'],
      'mechanicId' : service['slipAdminMechanicId'],
      'officeId' : service['slipAdminOfficeId'],
      'serviceType' : service['targetService'],
      'slipNo' : service['slipNo'],
      'serviceTitle' : service['title'],
      'category' : '21',
      'message' : 'EVALUATION_REQ',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse2['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)




# バッチ実行時のタイムスタンプ作成
def get_timestamp():
    now = datetime.now()
    rand_minute = int(random.uniform(0, 59))
    rand_second = int(random.uniform(0, 59))
    nowTime = datetime(now.year, now.month, now.day, now.hour, rand_minute, rand_second)
    return int(nowTime.timestamp()) * 1000


