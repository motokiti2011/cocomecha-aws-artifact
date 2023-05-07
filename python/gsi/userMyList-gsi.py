import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("userMyList")


# ユーザーマイリストGSI検索
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['id']
        if IndexType == 'USERID-INDEX':
        
          cognitoUserId = PartitionKey
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
          return userId_query(userId)

        if IndexType == 'MECHANICID-INDEX':
            return mechanicId_query(PartitionKey)


        if IndexType == 'OFFICEID-INDEX':
            return officeId_query(PartitionKey)

    except Exception as e:
        print("Error Exception.")
        print(e)


# レコード検索 userId-index
def userId_query(partitionKey):
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード検索 mechanicId-index
def mechanicId_query(partitionKey):
    queryData = table.query(
        IndexName = 'mechanicId-index',
        KeyConditionExpression = Key("mechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード検索 officeId-index
def officeId_query(partitionKey):
    queryData = table.query(
        IndexName = 'officeId-index',
        KeyConditionExpression = Key("officeId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


