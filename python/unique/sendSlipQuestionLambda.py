import json
import boto3
import uuid

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("slipQuestion")
slipDetailInfo = dynamodb.Table("slipDetailInfo")
salesServiceInfo = dynamodb.Table("salesServiceInfo")


# レコード追加
def post_product(PartitionKey, event, adminUser):

  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'slipNo' : event['Keys']['slipNo'],
      'slipAdminUser' : adminUser,
      'senderId' : event['Keys']['senderId'],
      'senderName' : event['Keys']['senderName'],
      'senderText' : event['Keys']['senderText'],
      'anserDiv' : event['Keys']['anserDiv'],
      'anserText' : event['Keys']['anserText'],
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse


# 伝票情報取得
def getSlipDitail(PartitionKey):
  queryData = slipDetailInfo.query(
      KeyConditionExpression = Key("slipNo").eq(PartitionKey) & Key("deleteDiv").eq("0")
  )
  if queryData['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(queryData)
    return queryData['Items']
  else:
    print('Post Successed.mechanic')
    return queryData['Items']


# サービス商品情報取得
def getSalesServiceInfo(PartitionKey):
  queryData = salesServiceInfo.query(
      KeyConditionExpression = Key("slipNo").eq(PartitionKey) & Key("deleteDiv").eq("0")
  )
  if queryData['ResponseMetadata']['HTTPStatusCode'] != 200:
    return queryData['Items']
  else:
    print('Post Successed.mechanic')
    return queryData['Items']

def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  OperationType = event['OperationType']
  key = event['Keys']['slipNo']
  serviceKey = event['ServiceType']

  print(event['OperationType'])
  try:
    if OperationType == 'SENDQUESTION':
      if serviceKey == '0':
        slip = getSlipDitail(key)
        adminUser = slip[0]['slipAdminUserId'],
      else:
        service = getSalesServiceInfo(key)
        adminUser = service[0]['slipAdminUserId'],
      PartitionKey = str(uuid.uuid4())
      return post_product(PartitionKey, event, adminUser)
    else:
      return []
  except Exception as e:
      print("Error Exception.")
      print(e)