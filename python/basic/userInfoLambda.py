import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("userInfo")

# ユーザー情報取得Lambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:
    if OperationType == 'QUERY':
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

      PartitionKey = userId
      sortKey = event['Keys']['userValidDiv']
      return operation_query(PartitionKey, sortKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['userId']
      return post_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      PartitionKey = userId
      return operation_delete(PartitionKey)

  except Exception as e:
      print("Error Exception.")
      print(e)



# レコード検索
def operation_query(partitionKey, sortKey):
    queryData = table.query(
        KeyConditionExpression = Key("userId").eq(partitionKey) & Key("userValidDiv").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード追加
def post_product(PartitionKey, event):

  now = datetime.now()
  
  putResponse = table.put_item(
    Item={
      'userId' : PartitionKey,
      'userValidDiv' : event['Keys']['userValidDiv'],
      'corporationDiv' : event['Keys']['corporationDiv'],
      'userName' : event['Keys']['userName'],
      'mailAdress' : event['Keys']['mailAdress'],
      'TelNo1' : event['Keys']['TelNo1'],
      'TelNo2' : event['Keys']['TelNo2'],
      'areaNo1' : event['Keys']['areaNo1'],
      'areaNo2' : event['Keys']['areaNo2'],
      'adress' : event['Keys']['adress'],
      'postCode' : event['Keys']['postCode'],
      'mechanicId' : event['Keys']['mechanicId'],
      'officeId' : event['Keys']['officeId'],
      'baseId' : event['Keys']['baseId'],
      'officeRole' : event['Keys']['officeRole'],
      'profileImageUrl' : event['Keys']['profileImageUrl'],
      'introduction' : event['Keys']['introduction'],
      'publicInfo' : event['Keys']['publicInfo'],
      'updateUserId' : event['Keys']['updateUserId'],
      'created' : event['Keys']['created'],
      'updated' : now.strftime('%x %X')
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
           'userId': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse['ResponseMetadata']['HTTPStatusCode']

