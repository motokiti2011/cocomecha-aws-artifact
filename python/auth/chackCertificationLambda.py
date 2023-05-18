import json
import boto3

from datetime import datetime, timedelta


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
  # 2時間後の時刻を設定
  ttlData = datetime.now() + timedelta(hours=2)
  ttl = str(ttlData .timestamp())

  putResponse = accountUserConneection.put_item(
    Item={
      'userId' : data['userId'],
      'accountUseId' : data['accountUseId'],
      'operationDate' :  ttlData.strftime('%Y%m%d'),
      'operationTime' :  ttlData.strftime('%H%M'),
      'created' :  data['created'],
      'operationDateTime' :  ttl
    }
  )
  print('post_accountUserConneection-SUCSESS')