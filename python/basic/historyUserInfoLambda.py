import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("historyUserInfo")

# ���R�[�h����
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("historyId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# ���R�[�h�X�V
def post_product(PartitionKey, event):

  now = datetime.now(JST)

  putResponse = table.put_item(
    Item={
      'historyId' : PartitionKey,
      'userId' : event['Keys']['userId'],
      'vehicleId' : event['Keys']['vehicleId'],
      'slipNo' : event['Keys']['slipNo'],
      'slipTitle' : event['Keys']['slipTitle'],
      'officeId' : event['Keys']['officeId'],
      'mechanicId' : event['Keys']['mechanicId'],
      'completionDate' : event['Keys']['completionDate'],
      'displayDiv' : event['Keys']['displayDiv'],
      'created' : event['Keys']['created'],
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse


# ���R�[�h�ǉ�
def operation_post(PartitionKey, event):

  now = datetime.now(JST)

  putResponse = table.put_item(
    Item={
      'historyId' : PartitionKey,
      'userId' : event['Keys']['userId'],
      'vehicleId' : event['Keys']['vehicleId'],
      'slipNo' : event['Keys']['slipNo'],
      'slipTitle' : event['Keys']['slipTitle'],
      'officeId' : event['Keys']['officeId'],
      'mechanicId' : event['Keys']['mechanicId'],
      'completionDate' : event['Keys']['completionDate'],
      'displayDiv' : event['Keys']['displayDiv'],
      'created' : now.strftime('%x %X'),
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
       key={
           'historyId': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse['Items']


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['historyId']
      return operation_query(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['historyId']
      return post_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      PartitionKey = event['Keys']['historyId']
      return operation_delete(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = id
      return operation_post(PartitionKey, event)


  except Exception as e:
      print("Error Exception.")
      print(e)