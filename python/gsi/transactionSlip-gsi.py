import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("transactionSlip")

# 取引中伝票情報GSI検索
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    SortKey = event['Keys']['serviceType']

    try:
        PartitionKey = event['Keys']['id']
        if IndexType == 'SLIPUSER-INDEX':

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

            return slipUser_query(userId,SortKey)

        elif IndexType == 'SLIPOFFICE-INDEX':
          PartitionKey = event['Keys']['id']
          return slipOffice_query(PartitionKey, SortKey)

        elif IndexType == 'SLIPMECHANIC-INDEX':
          PartitionKey = event['Keys']['id']
          return slipMechanic_query(PartitionKey,SortKey)

    except Exception as e:
        print("Error Exception.")
        print(e)



# 1レコード検索 slipUserId-index
def slipUser_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 2レコード検索 slipOffice-index
def slipOffice_query(partitionKey):
    queryData = table.query(
        IndexName = 'officeId-index',
        KeyConditionExpression = Key("officeId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 3レコード検索 slipMechanic-index
def slipMechanic_query(partitionKey):
    queryData = table.query(
        IndexName = 'mechanicId-index',
        KeyConditionExpression = Key("mechanicId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items


