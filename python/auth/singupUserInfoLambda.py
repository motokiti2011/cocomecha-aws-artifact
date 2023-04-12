import json
import boto3

from datetime import datetime


from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
userInfo = dynamodb.Table("userInfo")
accountUserConneection = dynamodb.Table("accountUserConneection")


def lambda_handler(event, context):
  print(event)
  print(event['userName'])
  print(event['request'])

  PartitionKey = event['userName']

  connectionData = operation_query(PartitionKey)
  if len(connectionData) > 0 :
    print('user-ADD-SUCSESS')
    userId = id = str(uuid.uuid4())
    
    post_accountUserConneection(PartitionKey, userId)
    post_userInfo(userId, event)
  else :
    print('USER-NOT-ADD')

  return



# レコード検索（データ確認）
def operation_query(partitionKey):
    queryData = accountUserConneection.query(
        KeyConditionExpression = Key("accountUseId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# ユーザーTBLレコード追加
def post_userInfo(userId, event):
  putResponse = userInfo.put_item(
    Item={
      'userId' : userId,
      'userValidDiv' : '0',
      'mailAdress' : event['request']['userAttributes']['email']
    }
  )
  print('post_userInfo-SUCSESS')
  return


# アカウントユーザー紐づけTBLレコード追加
def post_accountUserConneection(PartitionKey, userId):
  putResponse = accountUserConneection.put_item(
    Item={
      'accountUseId' : PartitionKey,
      'userId' : userId,
      'created' :  now.strftime('%x %X')
    }
  )
  print('post_accountUserConneection-SUCSESS')
  return event


