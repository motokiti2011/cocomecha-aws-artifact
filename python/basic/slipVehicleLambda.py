import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("slipVehicle")

# ���R�[�h����
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# ���R�[�h�X�V
def put_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'slipNo' : PartitionKey,
      'vehicleName' : event['Keys']['vehicleName'],
      'vehicleNo' : event['Keys']['vehicleNo'],
      'chassisNo' : event['Keys']['chassisNo'],
      'designatedClassification' : event['Keys']['designatedClassification'],
      'coler' : event['Keys']['coler'],
      'colerNo' : event['Keys']['colerNo'],
      'firstRegistrationDate' : event['Keys']['firstRegistrationDate'],
      'inspectionExpirationDate' : event['Keys']['inspectionExpirationDate'],
      'created' : event['Keys']['created'],
      'updated' :  now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse


# ���R�[�h�ǉ�
def post_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'slipNo' : PartitionKey,
      'vehicleName' : event['Keys']['vehicleName'],
      'vehicleNo' : event['Keys']['vehicleNo'],
      'chassisNo' : event['Keys']['chassisNo'],
      'designatedClassification' : event['Keys']['designatedClassification'],
      'coler' : event['Keys']['coler'],
      'colerNo' : event['Keys']['colerNo'],
      'firstRegistrationDate' : event['Keys']['firstRegistrationDate'],
      'inspectionExpirationDate' : event['Keys']['inspectionExpirationDate'],
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
       Key={
           'slipNo': partitionKey,
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
      PartitionKey = event['Keys']['slipNo']
      return operation_query(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['slipNo']
      return put_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      PartitionKey = event['Keys']['slipNo']
      return operation_delete(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = id
      return post_product(PartitionKey, event)

  except Exception as e:
      print("Error Exception.")
      print(e)