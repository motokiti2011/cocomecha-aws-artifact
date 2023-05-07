import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("userFavorite")

# お気に入りGSI検索
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:
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

        if IndexType == 'USERID-INDEX':
            return serch_query(userId)

    except Exception as e:
        print("Error Exception.")
        print(e)


# レコード検索 userId-index
def serch_query(partitionKey):
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

