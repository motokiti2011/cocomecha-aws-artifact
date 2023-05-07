import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("slipMegPrmUser")


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))

  OperationType = event['OperationType']

  try:
    if OperationType == 'CHECK':
      PartitionKey = event['Keys']['slipNo']

      cognitoUserId = event['Keys']['userId']
      # �F�؏��`�F�b�N�テ�[�U�[ID���擾
      # ����
      input_event = {
          "userId": cognitoUserId,
      }
      Payload = json.dumps(input_event) # json�V���A���C�Y
      # ���������ŌĂяo��
      response = boto3.client('lambda').invoke(
          FunctionName='CertificationLambda',
          InvocationType='RequestResponse',
          Payload=Payload
      )
      body = json.loads(response['Payload'].read())
      print(body)
      # ���[�U�[���̃��[�U�[ID���擾
      if body != None :
        userId = body
      else :
        print('NOT-CERTIFICATION')
        return

      return operation_query(PartitionKey, userId)

  except Exception as e:
      print("Error Exception.")
      print(e)


# ���R�[�h����
def operation_query(partitionKey, checkKey):
    queryData = table.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']

    if len(items) == 0:
      return False

    item = items[0]
    
    if item['slipAdminUserId'] == checkKey :
      return True
    else :
      return False

