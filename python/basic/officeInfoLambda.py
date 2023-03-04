import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("officeInfo")


# ���R�[�h����
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("officeId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# ���R�[�h�X�V
def put_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'officeId' : PartitionKey,
      'officeName' : event['Keys']['officeName'],
      'officeTel' : event['Keys']['officeTel'],
      'officeMailAdress' : event['Keys']['officeMailAdress'],
      'officeArea1' : event['Keys']['officeArea1'],
      'officeArea' : event['Keys']['officeArea'],
      'officeAdress' : event['Keys']['officeAdress'],
      'officePostCode' : event['Keys']['officePostCode'],
      'workContentList' : event['Keys']['workContentList'],
      'businessHours' : event['Keys']['businessHours'],
      'connectionOfficeInfo' : event['Keys']['connectionOfficeInfo'],
      'connectionMechanicInfo' : event['Keys']['connectionMechanicInfo'],
      'adminSettingInfo' : event['Keys']['adminSettingInfo'],
      'officePR' : event['Keys']['officePR'],
      'officePRimageURL' : event['Keys']['officePRimageURL'],
      'officeFormList' : event['Keys']['officeFormList'],
      'publicInfo' : event['Keys']['publicInfo'],
      'created' : event['Keys']['created'],
      'updated' :  now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['ResponseMetadata']['HTTPStatusCode']



# ���R�[�h�o�^
def post_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'officeId' : PartitionKey,
      'officeName' : event['Keys']['officeName'],
      'officeTel' : event['Keys']['officeTel'],
      'officeMailAdress' : event['Keys']['officeMailAdress'],
      'officeArea1' : event['Keys']['officeArea1'],
      'officeArea' : event['Keys']['officeArea'],
      'officeAdress' : event['Keys']['officeAdress'],
      'officePostCode' : event['Keys']['officePostCode'],
      'workContentList' : event['Keys']['workContentList'],
      'businessHours' : event['Keys']['businessHours'],
      'connectionOfficeInfo' : event['Keys']['connectionOfficeInfo'],
      'connectionMechanicInfo' : event['Keys']['connectionMechanicInfo'],
      'adminSettingInfo' : event['Keys']['adminSettingInfo'],
      'officePR' : event['Keys']['officePR'],
      'officePRimageURL' : event['Keys']['officePRimageURL'],
      'officeFormList' : event['Keys']['officeFormList'],
      'publicInfo' : event['Keys']['publicInfo'],
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
           'officeId': partitionKey,
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
      PartitionKey = event['Keys']['officeId']
      return operation_query(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['officeId']
      return put_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      PartitionKey = event['Keys']['officeId']
      return operation_delete(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = id
      return post_product(PartitionKey, event)

  except Exception as e:
      print("Error Exception.")
      print(e)