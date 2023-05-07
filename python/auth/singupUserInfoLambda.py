import json
import boto3
import uuid

from datetime import datetime


from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
userInfo = dynamodb.Table("userInfo")
accountUserConneection = dynamodb.Table("accountUserConneection")

# サインアップLambda
def lambda_handler(event, context):
  print(event)
  print(event['userName'])
  print(event['request'])
  print(event['request']['userAttributes']['email'])
  print(event['triggerSource'])

  PartitionKey = event['userName']
  mailAdless = event['request']['userAttributes']['email']
  triggerSource = event['triggerSource']
  
  # パスワードリセット以外の場合ユーザー追加
  if triggerSource != 'PostConfirmation_ConfirmForgotPassword' :
    userId = str(uuid.uuid4())
    post_accountUserConneection(PartitionKey, userId)
    post_userInfo(userId, mailAdless)
    print('USER-ADD-SUCSESS')
  else :
    print('USER-NOT-ADD')

  return event


# ユーザーTBLレコード追加
def post_userInfo(userId, mailAdless):
  putResponse = userInfo.put_item(
    Item={
      'userId' : userId,
      'userValidDiv' : '0',
      'mailAdress' : mailAdless
    }
  )
  print('post_userInfo-SUCSESS')



# アカウントユーザー紐づけTBLレコード追加
def post_accountUserConneection(PartitionKey, userId):
  putResponse = accountUserConneection.put_item(
    Item={
      'accountUseId' : PartitionKey,
      'userId' : userId,
      'created' :  datetime.now().strftime('%x %X')
    }
  )
  print('post_accountUserConneection-SUCSESS')



