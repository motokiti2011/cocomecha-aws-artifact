import json
import boto3

from datetime import datetime


from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
certificationManagementInfo = dynamodb.Table("certificationManagementInfo")
accountUserConneection = dynamodb.Table("accountUserConneection")



# ���O�A�E�g���̔F�؏��Ǘ�
def lambda_handler(event, context):
  print(event)
  print(event['userId'])

  PartitionKey = event['userId']
  
  # �A�J�E���g�R�Â����烆�[�U�[ID���擾
  
  accountData = operation_queryConnection(PartitionKey)
  if len(accountData) > 0 :
    userId = accountData[0]['userId']
  else :
    print('USERID-FAILED')
    return
  print('userId')  
  print(userId)
  # �F�؏��Ǘ�����
  certificationData = operation_query(userId)
  if len(certificationData) > 0 :
    delete_certificationData(userId)
    print('USER-DEL-SUCSESS')

  else :
    print('USER-DEL-SUCSESS-ALREADY')

  return


# �A�J�E���g�R�Â����R�[�h�����i�f�[�^�m�F�j
def operation_queryConnection(partitionKey):
    queryData = accountUserConneection.query(
        KeyConditionExpression = Key("accountUseId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# ���R�[�h�����i�f�[�^�m�F�j
def operation_query(partitionKey):
    queryData = certificationManagementInfo.query(
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# �F�؏�񃌃R�[�h�폜
def delete_certificationData(partitionKey):
    delResponse = certificationManagementInfo.delete_item(
       Key={
           'userId': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse


