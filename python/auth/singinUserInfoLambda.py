import json
import boto3

from datetime import datetime, timedelta


from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
userInfo = dynamodb.Table("userInfo")
accountUserConneection = dynamodb.Table("accountUserConneection")
certificationManagementInfo = dynamodb.Table("certificationManagementInfo")


# サインイン時トリガーLambda
def lambda_handler(event, context):
  print(event)
  print(event['userName'])
  print(event['request'])

  PartitionKey = event['userName']


  # アカウント・ユーザー紐付け情報
  connectionData = operation_query(PartitionKey)
  if len(connectionData) == 0 :
    print('USER-NOT-Failure')
    # ログ吐いて処理終了
    return

  userId = connectionData[0]['userId']
  
  # 認証情報取得
  certificationData = get_certification(userId)
  if len(certificationData) > 0 :
    # すでに認証されている場合更新する。
    put_certificationData(certificationData[0])
    print('PUT_certification')
  else :
    # 未認証の場合追加する。
    post_certificationData(connectionData[0])
    print('POST_certification')

  print('SININ-SUCSESS')
  return event


# レコード検索（データ確認）
def operation_query(partitionKey):
    queryData = accountUserConneection.query(
        KeyConditionExpression = Key("accountUseId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# 認証情報取得
def get_certification(userId):
    queryData = certificationManagementInfo.query(
        KeyConditionExpression = Key("userId").eq(userId)
    )
    items=queryData['Items']
    print(items)
    return items



# 認証情報追加
def post_certificationData(data):

  dt2 = datetime.now() + timedelta(hours=2)
  ttl = str(dt2.timestamp())
  putResponse = certificationManagementInfo.put_item(
    Item={
      'userId' : data['userId'],
      'accountUseId': data['accountUseId'],
      'operationDate':  dt2.strftime('%Y%m%d'),
      'operationTime':  dt2.strftime('%H%M'),
      'created': datetime.now().strftime('%Y%m%d%H%M%S'),
      'operationDateTime': ttl
    }
  )
  print('post_accountUserConneection-SUCSESS')
  return


# 認証情報更新
def put_certificationData(data):

  # 2時間後の時刻を設定
  ttlData = datetime.now() + timedelta(hours=2)
  ttl = str(ttlData .timestamp())

  putResponse = certificationManagementInfo.put_item(
    Item={
      'userId' : data['userId'],
      'accountUseId': data['accountUseId'],
      'operationDate':  ttlData.strftime('%Y%m%d'),
      'operationTime':  ttlData.strftime('%H%M'),
      'created':  data['created'],
      'operationDateTime':  ttl
    }
  )
  print('post_accountUserConneection-SUCSESS')
  return
