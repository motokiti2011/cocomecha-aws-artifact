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
transactionSlip = dynamodb.Table("transactionSlip")
userMyList = dynamodb.Table("userMyList")


# スケジュールバッチ 期限切れ取引中伝票情報の抽出
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  print('DEADLINECHECKSERVICE')

  print('hoge1')
  try:
    deadLineServiceData = deadlineservice_query()
    print('3')
    print(deadLineServiceData['Count'])

    if deadLineServiceData['Count'] > 0 :
      for service in deadLineServiceData['Items'] :
        if service['ttlDate'] == 0:
          # TTL日付を設定する
          setTTLDate_query(service)
          # マイリストTBLにメッセージを設定する
          setMyListMsg_query(service)
  except Exception as e:
      print("Error Exception.")
      print(e)


# 取引中伝票情報の期限切れ情報を抽出しマイリストTBLへのメッセージとして通知する。
# 取引中伝票情報の期限切れデータを取得する(72時間前～現在時刻)
def deadlineservice_query():

    START_TIMESTAMP = get_min_timestamp()
    END_TIMESTAMP = get_timestamp()
    print('START_TIMESTAMP')
    print(START_TIMESTAMP)
    print('END_TIMESTAMP')
    print(END_TIMESTAMP)    
    print('2')
    queryData = transactionSlip.query(
        IndexName = 'completionScheduledDate-index',
        KeyConditionExpression = Key("deleteDiv").eq("0") 
        & Key("completionScheduledDate").between(START_TIMESTAMP, END_TIMESTAMP)
    )
    print(queryData)
    return queryData
    # items=queryData
    # print(items)
    # return items


# transactionSlipに対してTTL日付設定
def setTTLDate_query(service):

  TTL_DATE = get_ttl_timestamp()

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
      'deleteDiv' : service['deleteDiv'],
      'completionScheduledDate' : service['completionScheduledDate'],
      'ttlDate' : TTL_DATE,
      'created' : event['Keys']['created'],
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['Item']


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
      'category' : '18',
      'message' : 'COMP_DATE',
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


