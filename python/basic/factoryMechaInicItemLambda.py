import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("factoryMechaInicItem")


# ���R�[�h����
def operation_query(partitionKey, sortKey):
    queryData = table.query(
        KeyConditionExpression = Key("serviceId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items

# ���R�[�h�X�V
def put_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'serviceId' : PartitionKey,
      'serviceName' : event['Keys']['serviceName'],
      'factoryMechanicId' : event['Keys']['factoryMechanicId'],
      'serviceType' : event['Keys']['serviceType'],
      'transactionStatus' : event['Keys']['transactionStatus'],
      'browsingCount' : event['Keys']['browsingCount'],
      'favoriteCount' : event['Keys']['favoriteCount']
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['ResponseMetadata']['HTTPStatusCode']


# ���R�[�h�ǉ�
def post_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'serviceId' : PartitionKey,
      'serviceName' : event['Keys']['serviceName'],
      'factoryMechanicId' : event['Keys']['factoryMechanicId'],
      'serviceType' : event['Keys']['serviceType'],
      'transactionStatus' : event['Keys']['transactionStatus'],
      'browsingCount' : event['Keys']['browsingCount'],
      'favoriteCount' : event['Keys']['favoriteCount']
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['ResponseMetadata']['HTTPStatusCode']



# ���R�[�h�폜
def operation_delete(partitionKey):
    delResponse = table.delete_item(
       Key={
           'serviceId': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['serviceId']
      sortKey = event['Keys']['serviceType']
      return operation_query(PartitionKey, sortKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['serviceId']
      return put_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      return operation_delete(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = event['Keys']['serviceId']
      return post_product(PartitionKey, event)


  except Exception as e:
      print("Error Exception.")
      print(e)