import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("browsingHistory")

# �{��������񑀍�Lambda
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
      
      # �H�ꃁ�J�j�b�N���i���̉{�����𐔂��X�V
      # ����
      input_event = {
          "processDiv": '0',
          "serviceId": event['Keys']['slipNo'],
          "serviceType": event['Keys']['serviceType'],
          "status": '0'
      }
      Payload = json.dumps(input_event) # json�V���A���C�Y
      # �Ăяo��
      boto3.client('lambda').invoke(
          FunctionName='internalFcMcItemLambda',
          InvocationType='Event',
          Payload=Payload
      )
      
      return post_product(PartitionKey, event)

  except Exception as e:
      print("Error Exception.")
      print(e)



# ���R�[�h����
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("id").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# ���R�[�h�X�V
def put_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'userId' : event['Keys']['userId'],
      'slipNo' : event['Keys']['slipNo'],
      'title' : event['Keys']['title'],
      'price' : event['Keys']['price'],
      'whet' : event['Keys']['whet'],
      'endDate' : event['Keys']['endDate'],
      'imageUrl' : event['Keys']['imageUrl'],
      'serviceType' : event['Keys']['serviceType'],
      'created' : event['Keys']['created'],
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse
  
  # ���R�[�h�폜
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


# ���R�[�h�ǉ�
def post_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'userId' : event['Keys']['userId'],
      'slipNo' : event['Keys']['slipNo'],
      'title' : event['Keys']['title'],
      'price' : event['Keys']['price'],
      'whet' : event['Keys']['whet'],
      'endDate' : event['Keys']['endDate'],
      'imageUrl' : event['Keys']['imageUrl'],
      'serviceType' : event['Keys']['serviceType'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')

    }
  )

