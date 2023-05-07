import json
import boto3
import uuid

from datetime import datetime


from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
userInfo = dynamodb.Table("userInfo")
accountUserConneection = dynamodb.Table("accountUserConneection")

# �T�C���A�b�vLambda
def lambda_handler(event, context):
  print(event)
  print(event['userName'])
  print(event['request'])
  print(event['request']['userAttributes']['email'])
  print(event['triggerSource'])

  PartitionKey = event['userName']
  mailAdless = event['request']['userAttributes']['email']
  triggerSource = event['triggerSource']
  
  # �p�X���[�h���Z�b�g�ȊO�̏ꍇ���[�U�[�ǉ�
  if triggerSource != 'PostConfirmation_ConfirmForgotPassword' :
    userId = str(uuid.uuid4())
    post_accountUserConneection(PartitionKey, userId)
    post_userInfo(userId, mailAdless)
    print('USER-ADD-SUCSESS')
  else :
    print('USER-NOT-ADD')

  return event


# ���[�U�[TBL���R�[�h�ǉ�
def post_userInfo(userId, mailAdless):
  putResponse = userInfo.put_item(
    Item={
      'userId' : userId,
      'userValidDiv' : '0',
      'mailAdress' : mailAdless
    }
  )
  print('post_userInfo-SUCSESS')



# �A�J�E���g���[�U�[�R�Â�TBL���R�[�h�ǉ�
def post_accountUserConneection(PartitionKey, userId):
  putResponse = accountUserConneection.put_item(
    Item={
      'accountUseId' : PartitionKey,
      'userId' : userId,
      'created' :  datetime.now().strftime('%x %X')
    }
  )
  print('post_accountUserConneection-SUCSESS')



