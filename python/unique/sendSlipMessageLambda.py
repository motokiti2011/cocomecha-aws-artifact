import json
import boto3
import uuid

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("slipMessageInfo")

# ���R�[�h�ǉ�
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