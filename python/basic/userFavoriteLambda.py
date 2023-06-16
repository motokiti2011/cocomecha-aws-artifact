import json
import boto3
import uuid

from datetime import datetime
from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("userFavorite")

# お気に入り情報データアクセスLambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))

  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['id']
      return operation_query(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['id']
      return put_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      PartitionKey = event['Keys']['id']

      # 工場メカニック商品情報のお気に入り数を更新
      # 引数
      input_event = {
          "processDiv": '1',
          "serviceId": event['Keys']['slipNo'],
          "serviceType": event['Keys']['serviceType'],
          "status": '1'
      }
      Payload = json.dumps(input_event) # jsonシリアライズ
      # 呼び出し
      boto3.client('lambda').invoke(
          FunctionName='internalFcMcItemLambda',
          InvocationType='Event',
          Payload=Payload
      )

      return operation_delete(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = id
      
      # 工場メカニック商品情報のお気に入り数を更新
      # 引数
      input_event = {
          "processDiv": '1',
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

# レコード追加
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
      'created' : event['Keys']['created'],
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['ResponseMetadata']['HTTPStatusCode']
  
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
    return delResponse['ResponseMetadata']['HTTPStatusCode']

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
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['ResponseMetadata']['HTTPStatusCode']


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
        FunctionName='certificationLambda',
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

