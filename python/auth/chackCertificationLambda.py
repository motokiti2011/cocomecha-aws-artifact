import json
import boto3

from datetime import datetime


from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
certificationManagementInfo = dynamodb.Table("certificationManagementInfo")

# �F�؏󋵃`�F�b�NLambda
def lambda_handler(event, context):
  print(event)
  print(event['userId'])

  PartitionKey = event['userId']
  # �F�؏��Ǘ�����
  certificationData = operation_query(PartitionKey)
  if len(certificationData) > 0 :
    # �F�؏�ԂȂ�A�N�Z�X�󋵂��X�V����
    put_certificationData(certificationData[0])
    print('ALREADY-CERTIFICATION')
    return True
  else :
    print('NOT-ALREADY-CERTIFICATION')

  return False

# ���R�[�h�����i�f�[�^�m�F�j
def operation_query(partitionKey):
    queryData = certificationManagementInfo.query(
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# �F�؏��X�V(TTL�֘A�̓����X�V)
def put_certificationData(data):
  putResponse = accountUserConneection.put_item(
    Item={
      'userId' : data['userId'],
      'accountUseId' : data['accountUseId'],
      'operationDate' :  now.strftime('%Y%m%d'),
      'operationTime' :  now.strftime('%H%M'),
      'created' :  data['created'],
      'operationDateTime' :  now.strftime('%Y%m%d%H%M')
    }
  )
  print('post_accountUserConneection-SUCSESS')
  return event