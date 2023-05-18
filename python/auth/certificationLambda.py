import json
import boto3

from datetime import datetime, timedelta


from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
certificationManagementInfo = dynamodb.Table("certificationManagementInfo")
accountUserConneection = dynamodb.Table("accountUserConneection")


# CognitoユーザーIDから認証情報のユーザー情報取得Lambda
def lambda_handler(event, context):
  print(event)
  print(event['userId'])

  accountId = event['userId']
  # アカウント紐づけ情報検索
  accountUserConneection = accountUserConneection_query(accountId)  
  print(accountUserConneection)
  if len(accountUserConneection) == 0 :
      return None
  
  PartitionKey = accountUserConneection[0]['userId']
  # 認証情報管理検索
  certificationData = operation_query(PartitionKey)
  print(certificationData)
  if len(certificationData) > 0 :
    # 認証状態ならアクセス状況を更新する
    data = put_certificationData(certificationData[0])
    print(PartitionKey)
    print('ALREADY-CERTIFICATION')
    return PartitionKey
  else :
    print('NOT-ALREADY-CERTIFICATION')

  return None


# アカウント紐づけレコード検索（データ確認）
def accountUserConneection_query(partitionKey):
    queryData = accountUserConneection.query(
        KeyConditionExpression = Key("accountUseId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# 認証情報レコード検索（データ確認）
def operation_query(partitionKey):
    queryData = certificationManagementInfo.query(
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# 認証情報更新(TTL関連の日時更新)
def put_certificationData(data):

  # 2時間後の時刻を設定
  dt2 = datetime.now() + timedelta(hours=2)
  
  putResponse = certificationManagementInfo.put_item(
    Item={
      'userId' : data['userId'],
      'accountUseId' : data['accountUseId'],
      'operationDate' :  dt2.strftime('%Y%m%d'),
      'operationTime' :  dt2.strftime('%H%M'),
      'created' :  data['created'],
      'operationDateTime' :  dt2.strftime('%Y%m%d%H%M')
    }
  )
  print('post_accountUserConneection-SUCSESS')
  return putResponse