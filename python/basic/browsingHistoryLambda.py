import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("browsingHistory")

# 閲覧履歴情報操作Lambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['id']
      return operation_query(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['id']
      return put_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      return operation_delete(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = id
      
      # 重複チェック
      uniqCheck = browsingUniqCheck(event)
      
      if uniqCheck:
        # 更新
        return put_product(PartitionKey, event)
      else :
        # 工場メカニック商品情報の閲覧履歴数を更新
        # 引数
        input_event = {
            "processDiv": '0',
            "serviceId": event['Keys']['slipNo'],
            "serviceType": event['Keys']['serviceType'],
            "status": '0'
        }
        Payload = json.dumps(input_event) # jsonシリアライズ
        # 呼び出し
        boto3.client('lambda').invoke(
            FunctionName='internalFcMcItemLambda',
            InvocationType='Event',
            Payload=Payload
        )
        # 登録
        return post_product(PartitionKey, event)

  except Exception as e:
      print("Error Exception.")
      print(e)



# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("id").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード更新
def put_product(PartitionKey, event):
  # 認証情報チェック
  userId = CertificationUserId(event)
  if userId == None :
    print('NOT-CERTIFICATION')
    return 500

  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'userId' : userId,
      'slipNo' : event['Keys']['slipNo'],
      'title' : event['Keys']['title'],
      'price' : event['Keys']['price'],
      'whet' : event['Keys']['whet'],
      'endDate' : event['Keys']['endDate'],
      'imageUrl' : event['Keys']['imageUrl'],
      'serviceType' : event['Keys']['serviceType'],
      'created' : event['Keys']['created'],
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse
  
  # レコード削除
def operation_delete(partitionKey):
    delResponse = table.delete_item(
       Key={
           'id': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse


# レコード追加
def post_product(PartitionKey, event):
  # 認証情報チェック
  userId = CertificationUserId(event)
  if userId == None :
    print('NOT-CERTIFICATION')
    return 500

  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'userId' : userId,
      'slipNo' : event['Keys']['slipNo'],
      'title' : event['Keys']['title'],
      'price' : event['Keys']['price'],
      'whet' : event['Keys']['whet'],
      'endDate' : event['Keys']['endDate'],
      'imageUrl' : event['Keys']['imageUrl'],
      'serviceType' : event['Keys']['serviceType'],
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')

    }
  )


# 重複チェック
def browsingUniqCheck(event):
    # 更新対象のユーザーIDで登録中の閲覧履歴情報を取得する
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(event['Keys']['userId'])
    )
    items=queryData['Items']
    
    # 未取得の場合チェックを終了する。
    if len(items) == 0 :
      return False
    
    for item in items :
      # 伝票番号が重複した場合更新
      if item['slipNo'] == event['Keys']['slipNo'] :
        return True
    # 重複なしの場合登録
    return False

# 認証情報からユーザー情報取得
def CertificationUserId(event):
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
      return body
    else :
      print('NOT-CERTIFICATION')
      return None

