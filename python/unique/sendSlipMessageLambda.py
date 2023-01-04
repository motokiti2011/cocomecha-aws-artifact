import json
import boto3
import uuid

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("slipMessageInfo")

# レコード追加
def post_product(PartitionKey, event):
  putResponse = table.put_item(
    Item={
      'messageId' : PartitionKey,
      'slipNo' : event['Keys']['slipNo'],
      'displayOrder' : event['Keys']['displayOrder'],
      'userId' : event['Keys']['userId'],
      'sendUserName' : event['Keys']['sendUserName'],
      'comment' : event['Keys']['comment'],
      'sendAdressId' : event['Keys']['sendAdressId'],
      'logicalDeleteDiv' : event['Keys']['logicalDeleteDiv'],
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse
  

def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  OperationType = event['OperationType']

  try:

    if OperationType == 'SENDMESSAGE':
      PartitionKey = str(uuid.uuid4())
      return post_product(PartitionKey, event)

  except Exception as e:
      print("Error Exception.")
      print(e)