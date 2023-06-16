import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("userMyList")

# ユーザーマイリストTBL操作Lambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['id']
      return operation_query(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = id
      return post_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      return operation_delete(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['id']
      return put_product(PartitionKey, event)

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
      'userId' : event['Keys']['data']['userId'],
      'mechanicId' : event['Keys']['data']['mechanicId'],
      'officeId' : event['Keys']['data']['officeId'],
      'serviceType' : event['Keys']['data']['serviceType'],
      'slipNo' : event['Keys']['data']['slipNo'],
      'serviceTitle' : event['Keys']['data']['serviceTitle'],
      'category' : event['Keys']['data']['category'],
      'message' : event['Keys']['data']['message'],
      'readDiv' : event['Keys']['data']['readDiv'],
      'messageDate' : event['Keys']['data']['messageDate'],
      'messageOrQuastionId' : event['Keys']['data']['messageOrQuastionId'],
      'requestInfo' : event['Keys']['data']['requestInfo'],
      'deleteDiv' : event['Keys']['data']['deleteDiv'],
      'created' : event['Keys']['data']['created'],
      'updated' :  datetime.now().strftime('%x %X')
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
      'mechanicId' : event['Keys']['mechanicId'],
      'officeId' : event['Keys']['officeId'],
      'serviceType' : event['Keys']['serviceType'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : event['Keys']['serviceTitle'],
      'category' : event['Keys']['category'],
      'message' : event['Keys']['message'],
      'readDiv' : event['Keys']['readDiv'],
      'messageDate' : event['Keys']['messageDate'],
      'messageOrQuastionId' : event['Keys']['messageOrQuastionId'],
      'requestInfo' : event['Keys']['requestInfo'],
      'deleteDiv' : event['Keys']['deleteDiv'],
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')

    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse



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