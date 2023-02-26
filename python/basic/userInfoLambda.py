import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("userInfo")


# ���R�[�h����
def operation_query(partitionKey, sortKey):
    queryData = table.query(
        KeyConditionExpression = Key("userId").eq(partitionKey) & Key("userValidDiv").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items

# ���R�[�h�ǉ�
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
  return putResponse
  
  # ���R�[�h�폜
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
    return delResponse


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['userId']
      sortKey = event['Keys']['userValidDiv']
      return operation_query(PartitionKey, sortKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['userId']
      return post_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      PartitionKey = event['Keys']['userId']
      return operation_delete(PartitionKey)

  except Exception as e:
      print("Error Exception.")
      print(e)