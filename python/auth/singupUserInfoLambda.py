import json
import boto3

from datetime import datetime


from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
userInfo = dynamodb.Table("userInfo")
accountUserConneection = dynamodb.Table("accountUserConneection")


def lambda_handler(event, context):
  print(event)
  print(event['userName'])
  print(event['request'])

  PartitionKey = event['userName']

  connectionData = operation_query(PartitionKey)
  if len(connectionData) > 0 :
    print('user-ADD-SUCSESS')
    userId = id = str(uuid.uuid4())
    
    post_accountUserConneection(PartitionKey, userId)
    post_userInfo(userId, event)
  else :
    print('USER-NOT-ADD')

  return



# ���R�[�h�����i�f�[�^�m�F�j
def operation_query(partitionKey):
    queryData = accountUserConneection.query(
        KeyConditionExpression = Key("accountUseId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# ���[�U�[TBL���R�[�h�ǉ�
def post_userInfo(userId, event):
  putResponse = userInfo.put_item(
    Item={
      'userId' : userId,
      'userValidDiv' : '0',
      'mailAdress' : event['request']['userAttributes']['email']
    }
  )
  print('post_userInfo-SUCSESS')
  return


# �A�J�E���g���[�U�[�R�Â�TBL���R�[�h�ǉ�
def post_accountUserConneection(PartitionKey, userId):
  putResponse = accountUserConneection.put_item(
    Item={
      'accountUseId' : PartitionKey,
      'userId' : userId,
      'created' :  now.strftime('%x %X')
    }
  )
  print('post_accountUserConneection-SUCSESS')
  return event


