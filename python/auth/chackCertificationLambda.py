import json
import boto3

from datetime import datetime


from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
certificationManagementInfo = dynamodb.Table("certificationManagementInfo")

# 認証状況チェックLambda
def lambda_handler(event, context):
  print(event)
  print(event['userId'])

  PartitionKey = event['userId']
  # 認証情報管理検索
  certificationData = operation_query(PartitionKey)
  if len(certificationData) > 0 :
    # 認証状態ならアクセス状況を更新する
    put_certificationData(certificationData[0])
    print('ALREADY-CERTIFICATION')
    return True
  else :
    print('NOT-ALREADY-CERTIFICATION')

  return False

# レコード検索（データ確認）
def operation_query(partitionKey):
    queryData = certificationManagementInfo.query(
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# 認証情報更新(TTL関連の日時更新)
def put_certificationData(data):
  putResponse = accountUserConneection.put_item(
    Item={
      'userId' : data['userId'],
      'accountUseId' : data['accountUseId'],
      'operationDate' :  now.strftime('%Y%m%d'),
      'operationTime' :  now.strftime('%H%M'),
      'created' :  data['created'],
      'operationDateTime' :  now.strftime('%Y%m%d%H%M')
    }
  )
  print('post_accountUserConneection-SUCSESS')
  return event