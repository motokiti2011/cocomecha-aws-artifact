import json
import boto3
import random

from datetime import datetime, timedelta
import random

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
slipDetailInfo = dynamodb.Table("slipDetailInfo")
userMyList = dynamodb.Table("userMyList")


# スケジュールバッチ 期限切れ取引中伝票情報の抽出
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  print('ExpiredSlipDeleteHourSchedule')

  # 3日前の日付取得
  targetDate = get_min_timestamp()
  targetTime = now.strftime('%H')

  try:
    # 対象データを抽出
    slipData = slipDetail_query()
    print('処理対象件数')
    print(slipData['Count'])

    if slipData['Count'] > 0 :
      for service in slipData['Items']  :
        # 希望日から72時間超えている場合
        if service['preferredDate'] < targetDate && service['preferredTime'] < targetTime :
          # 論理削除を行う
          delete_query(service)
          # マイリストTBLにメッセージを設定する
          setMyListMsg_query(service)
  except Exception as e:
      print("Error Exception.")
      print(e)


# 伝票情報の期限切れデータを取得する
def slipDetail_query():

    queryData = salesServiceInfo.query(
      IndexName = 'processStatus-index',
      KeyConditionExpression = Key("processStatus").eq("3") 
    )
    print(queryData)
    return queryData


# 論理削除を行う
def delete_query(service):

    putResponse = slipDetailInfo.put_item(
      Item= {
        'slipNo' : service['slipNo'],
        'deleteDiv' : '1',
        'category' : service['category'],
        'slipAdminUserId' : service['slipAdminUserId'],
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
        'processStatus' : service['processStatus'],
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
        'updated' : service['updated']
      }
    )
  
  return


# ユーザーマイリストTBL(期限切れメッセージ登録)
def postConfirmMylistRequest(service):

  now = datetime.now()

  putResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : service['userId'],
      'mechanicId' : service['mechanicId'],
      'officeId' : service['officeId'],
      'serviceType' : service['serviceType'],
      'slipNo' : service['slipNo'],
      'serviceTitle' : service['serviceTitle'],
      'category' : '26',
      'message' : 'EXPIRED_SERVICE_DELETE',
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
    return putResponse
  else:
    print('ConfirmMylistRequest : Post Successed.')



# バッチ実行時のタイムスタンプ作成
def get_timestamp():
    now = datetime.now()    
    rand_minute = int(random.uniform(0, 59))
    rand_second = int(random.uniform(0, 59))
    nowTime = datetime(now.year, now.month, now.day, now.hour, rand_minute, rand_second)
    # return int(nowTime.timestamp()) * 1000
    return int(nowTime.strftime('%Y%m%d'))

# バッチ実行時の3日前タイムスタンプ作成
def get_min_timestamp():
    now = datetime.now()    
    rand_minute = int(random.uniform(0, 59))
    rand_second = int(random.uniform(0, 59))
    nowDateTime = datetime(now.year -1, now.month, now.day, now.hour, rand_minute, rand_second)
    treeDayBeforTime = nowDateTime - timedelta(days=3)
    # return int(treeDayBeforTime.timestamp()) * 1000
    return int(treeDayBeforTime.strftime('%Y%m%d'))

# バッチ実行時の3日後タイムスタンプ作成
def get_ttl_timestamp():
    now = datetime.now()    
    rand_minute = int(random.uniform(0, 59))
    rand_second = int(random.uniform(0, 59))
    nowDateTime = datetime(now.year -1, now.month, now.day, now.hour, rand_minute, rand_second)
    treeDayAftterTime = nowDateTime + timedelta(days=3)
    # return int(treeDayAftterTime.timestamp()) * 1000
    return int(treeDayAftterTime.strftime('%Y%m%d'))


