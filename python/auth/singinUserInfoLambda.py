import json
import boto3

from datetime import datetime, timedelta


from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
userInfo = dynamodb.Table("userInfo")
accountUserConneection = dynamodb.Table("accountUserConneection")
certificationManagementInfo = dynamodb.Table("certificationManagementInfo")


# �T�C���C�����g���K�[Lambda
def lambda_handler(event, context):
  print(event)
  print(event['userName'])
  print(event['request'])

  PartitionKey = event['userName']


  # �A�J�E���g�E���[�U�[�R�t�����
  connectionData = operation_query(PartitionKey)
  if len(connectionData) == 0 :
    print('USER-NOT-Failure')
    # ���O�f���ď����I��
    return

  userId = connectionData[0]['userId']
  
  # �F�؏��擾
  certificationData = get_certification(userId)
  if len(certificationData) > 0 :
    # ���łɔF�؂���Ă���ꍇ�X�V����B
    put_certificationData(certificationData[0])
    print('PUT_certification')
  else :
    # ���F�؂̏ꍇ�ǉ�����B
    post_certificationData(connectionData[0])
    print('POST_certification')

  print('SININ-SUCSESS')
  return event


# ���R�[�h�����i�f�[�^�m�F�j
def operation_query(partitionKey):
    queryData = accountUserConneection.query(
        KeyConditionExpression = Key("accountUseId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# �F�؏��擾
def get_certification(userId):
    queryData = certificationManagementInfo.query(
        KeyConditionExpression = Key("userId").eq(userId)
    )
    items=queryData['Items']
    print(items)
    return items



# �F�؏��ǉ�
def post_certificationData(data):

  dt2 = datetime.now() + timedelta(hours=2)
  
  putResponse = certificationManagementInfo.put_item(
    Item={
      'userId' : data['userId'],
      'accountUseId': data['accountUseId'],
      'operationDate':  dt2.strftime('%Y%m%d'),
      'operationTime':  dt2.strftime('%H%M'),
      'created': datetime.now().strftime('%Y%m%d%H%M%S'),
      'operationDateTime':  dt2.strftime('%Y%m%d%H%M')
    }
  )
  print('post_accountUserConneection-SUCSESS')
  return


# �F�؏��X�V
def put_certificationData(data):

  # 2���Ԍ�̎�����ݒ�
  dt2 = datetime.now() + timedelta(hours=2)
  
  putResponse = certificationManagementInfo.put_item(
    Item={
      'userId' : data['userId'],
      'accountUseId': data['accountUseId'],
      'operationDate':  dt2.strftime('%Y%m%d'),
      'operationTime':  dt2.strftime('%H%M'),
      'created':  data['created'],
      'operationDateTime':  dt2.strftime('%Y%m%d%H%M')
    }
  )
  print('post_accountUserConneection-SUCSESS')
  return
