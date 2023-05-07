import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("slipMegPrmUser")


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))

  OperationType = event['OperationType']

  try:
    if OperationType == 'CHECK':
      PartitionKey = event['Keys']['slipNo']

      cognitoUserId = event['Keys']['userId']
      # 認証情報チェック後ユーザーIDを取得
      # 引数
      input_event = {
          "userId": cognitoUserId,
      }
      Payload = json.dumps(input_event) # jsonシリアライズ
      # 同期処理で呼び出し
      response = boto3.client('lambda').invoke(
          FunctionName='CertificationLambda',
          InvocationType='RequestResponse',
          Payload=Payload
      )
      body = json.loads(response['Payload'].read())
      print(body)
      # ユーザー情報のユーザーIDを取得
      if body != None :
        userId = body
      else :
        print('NOT-CERTIFICATION')
        return

      return operation_query(PartitionKey, userId)

  except Exception as e:
      print("Error Exception.")
      print(e)


# レコード検索
def operation_query(partitionKey, checkKey):
    queryData = table.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']

    if len(items) == 0:
      return False

    item = items[0]
    
    if item['slipAdminUserId'] == checkKey :
      return True
    else :
      return False

