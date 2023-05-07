import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("userVehicleInfo")

# ユーザー車両情報GSI検索
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        if IndexType == 'USERID-INDEX':
            cognitoUserId = event['Keys']['id']
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

        elif IndexType == 'VEHICLENO-INDEX':
          PartitionKey = event['Keys']['id']
          return vehicleNo_query(PartitionKey)


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


# レコード検索 vehicleNo-index
def vehicleNo_query(partitionKey):
    queryData = table.query(
        IndexName = 'vehicleNo-index',
        KeyConditionExpression = Key("vehicleNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

