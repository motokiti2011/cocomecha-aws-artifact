import json
import boto3

from datetime import datetime, timedelta


from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
certificationManagementInfo = dynamodb.Table("certificationManagementInfo")
accountUserConneection = dynamodb.Table("accountUserConneection")


# Cognito���[�U�[ID����F�؏��̃��[�U�[���擾Lambda
def lambda_handler(event, context):
  print(event)
  print(event['userId'])

  accountId = event['userId']
  # �A�J�E���g�R�Â���񌟍�
  accountUserConneection = accountUserConneection_query(accountId)  
  print(accountUserConneection)
  if len(accountUserConneection) == 0 :
      return None
  
  PartitionKey = accountUserConneection[0]['userId']
  # �F�؏��Ǘ�����
  certificationData = operation_query(PartitionKey)
  print(certificationData)
  if len(certificationData) > 0 :
    # �F�؏�ԂȂ�A�N�Z�X�󋵂��X�V����
    data = put_certificationData(certificationData[0])
    print(PartitionKey)
    print('ALREADY-CERTIFICATION')
    return PartitionKey
  else :
    print('NOT-ALREADY-CERTIFICATION')

  return None


# �A�J�E���g�R�Â����R�[�h�����i�f�[�^�m�F�j
def accountUserConneection_query(partitionKey):
    queryData = accountUserConneection.query(
        KeyConditionExpression = Key("accountUseId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# �F�؏�񃌃R�[�h�����i�f�[�^�m�F�j
def operation_query(partitionKey):
    queryData = certificationManagementInfo.query(
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# �F�؏��X�V(TTL�֘A�̓����X�V)
def put_certificationData(data):

  # 2���Ԍ�̎�����ݒ�
  dt2 = datetime.now() + timedelta(hours=2)
  
  putResponse = certificationManagementInfo.put_item(
    Item={
      'userId' : data['userId'],
      'accountUseId' : data['accountUseId'],
      'operationDate' :  dt2.strftime('%Y%m%d'),
      'operationTime' :  dt2.strftime('%H%M'),
      'created' :  data['created'],
      'operationDateTime' :  dt2.strftime('%Y%m%d%H%M')
    }
  )
  print('post_accountUserConneection-SUCSESS')
  return putResponse