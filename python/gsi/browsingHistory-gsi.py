import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("browsingHistory")


# 閲覧履歴情報GSI検索
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
            FunctionName='certificationLambda',
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
            return operation_query(userId)
        
    except Exception as e:
        print("Error Exception.")
        print(e)

# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


