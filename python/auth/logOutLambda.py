import json
import boto3

from datetime import datetime


from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
certificationManagementInfo = dynamodb.Table("certificationManagementInfo")
accountUserConneection = dynamodb.Table("accountUserConneection")



# ログアウト時の認証情報管理
def lambda_handler(event, context):
  print(event)
  print(event['userId'])

  PartitionKey = event['userId']
  
  # アカウント紐づけからユーザーIDを取得
  
  accountData = operation_queryConnection(PartitionKey)
  if len(accountData) > 0 :
    userId = accountData[0]['userId']
  else :
    print('USERID-FAILED')
    return
  print('userId')  
  print(userId)
  # 認証情報管理検索
  certificationData = operation_query(userId)
  if len(certificationData) > 0 :
    delete_certificationData(userId)
    print('USER-DEL-SUCSESS')

  else :
    print('USER-DEL-SUCSESS-ALREADY')

  return


# アカウント紐づけレコード検索（データ確認）
def operation_queryConnection(partitionKey):
    queryData = accountUserConneection.query(
        KeyConditionExpression = Key("accountUseId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# レコード検索（データ確認）
def operation_query(partitionKey):
    queryData = certificationManagementInfo.query(
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# 認証情報レコード削除
def delete_certificationData(partitionKey):
    delResponse = certificationManagementInfo.delete_item(
       Key={
           'userId': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse


