import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
salesServiceInfo = dynamodb.Table("salesServiceInfo")
slipDetailInfo = dynamodb.Table("slipDetailInfo")
transactionSlip = dynamodb.Table("transactionSlip")


# �m��T�[�r�X�ڍs

# �`�[���m��`�[���o
def slip_confirm(partitionKey):
    queryData = slipDetailInfo.query(
        IndexName = ' processStatus-index',
        # �u������v�̃X�e�[�^�X���c���Ă���ꍇ���o
        KeyConditionExpression = Key("processStatus").eq("1")
    )
    items=queryData['Items']
    print(items)
    return items

# �T�[�r�X���i��񒊏o
def service_confirm(partitionKey):
    queryData = salesServiceInfo.query(
        IndexName = ' processStatus-index',
        # �u������v�̃X�e�[�^�X���c���Ă���ꍇ���o
        KeyConditionExpression = Key("processStatus").eq("1")
    )
    items=queryData['Items']
    print(items)
    return items


# �`�[���폜
#def slipconfirm_delete(slipNo):
#    delResponse = slipDetailInfo.delete_item(
#       Key={
#           'slipNo': slipNo,
#       }
#    )
#    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
#        print(delResponse)
#
# �T�[�r�X���i�폜
#def serviceconfirm_delete(slipNo):
#    delResponse = salesServiceInfo.delete_item(
#       Key={
#           'slipNo': slipNo,
#       }
#    )
#    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
#        print(delResponse)


# ������`�[���ɓ`�[����ǉ�
def slipconfirm_post(slip):
  putResponse = transactionSlip.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'serviceType' : '0',
      'userId' : slip['slipAdminUserId'],
      'mechanicId' : '0',
      'officeId' : '0',
      'slipNo' : slip['slipNo'],
      'serviceTitle' : slip['title'],
      'slipRelation' : '0',
      'slipAdminId' : slip['slipAdminUserId'],
      'slipAdminName' : '',
      'bidderId' : slip['bidderId'],
      'deleteDiv' : '0',
      'completionScheduledDate' : 0,
      'ttlDate' : 0,
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)


# ������`�[���ɃT�[�r�X����ǉ�
def serviceconfirm_post(service):

  adminId = service['slipAdminUserId']
  if  service['targetService'] == 2:
    adminId = service['slipAdminOfficeId']
  elif service['targetService'] == 3:
    adminId = service['slipAdminMechanicId']

  putResponse = transactionSlip.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'serviceType' : service['targetService'],
      'userId' : service['slipAdminUserId'],
      'mechanicId' : service['slipAdminMechanicId'],
      'officeId' : service['slipAdminOfficeId'],
      'slipNo' : service['slipNo'],
      'serviceTitle' : service['title'],
      'slipRelation' : '0',
      'slipAdminId' : adminId,
      'slipAdminName' :  '',
      'bidderId' : service['bidderId'],
      'deleteDiv' : '0',
      'completionScheduledDate' : 0,
      'ttlDate' : 0,
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:
    if OperationType == 'CONFIRMMIGRATIONSERVICE':
      # �m��T�[�r�X�ڍs
      
      # �`�[�`�F�b�N
      confirmSlipData = slip_confirm()

      # �Ώۓ`�[�����݂���ꍇ
      if(len(confirmSlipData) > 0 :

          for slip in confirmSlipData :
            # �Ώۓ`�[���폜(�ۗ�)
            #slipconfirm_delete(slip['slipNo'])
            # �Ώۓ`�[��������`�[�ɒǉ�
            slipconfirm_post(slip)


      # �T�[�r�X���i�`�F�b�N
      confirmServiceData = service_confirm()

      if(len(confirmServiceData) > 0 :
      # �ΏۃT�[�r�X�����݂���ꍇ�폜
          for service in confirmServiceData :
            # �ΏۃT�[�r�X���폜(�ۗ�)
            #serviceconfirm_delete(service['slipNo'])
            # �ΏۃT�[�r�X��������`�[�ɒǉ�
            serviceconfirm_post(service)



  except Exception as e:
      print("Error Exception.")
      print(e)