import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("slipQuestion")
slipDetailInfo = dynamodb.Table("slipDetailInfo")
salesServiceInfo = dynamodb.Table("salesServiceInfo")
userMyList = dynamodb.Table("userMyList")

# ���R�[�h�ǉ�
def post_product(PartitionKey, event, adminUser, adminMecha, adminOffice, serviceKey, serviceTitle):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'slipNo' : event['Keys']['slipNo'],
      'slipAdminUser' : adminUser,
      'senderId' : event['Keys']['senderId'],
      'senderName' : event['Keys']['senderName'],
      'senderText' : event['Keys']['senderText'],
      'anserDiv' : event['Keys']['anserDiv'],
      'anserText' : event['Keys']['anserText'],
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('slipQuestion : Post Successed.')



  # �}�C���X�gTBL�̓o�^
  # �}�C���X�gTBL�̓o�^(�`�[�Ǘ���)
  userMyListResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : adminUser,
      'mechanicId' : adminMecha,
      'officeId' :adminOffice,
      'serviceType' : serviceKey,
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : serviceTitle,
      'category' : '2',
      'message' : 'UN_QUESTIONING',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  if userMyListResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListResponse)
  else:
    print('userMyList1 : Post Successed.')



  # �}�C���X�gTBL�̓o�^(�`�[�����)
  sendUserMyListResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : event['Keys']['senderId'],
      'mechanicId' : adminMecha,
      'officeId' : adminOffice,
      'serviceType' : serviceKey,
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : serviceTitle,
      'category' : '1',
      'message' : 'QUESTIONING',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  if sendUserMyListResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(sendUserMyListResponse)
  else:
    print('userMyList2 : Post Successed.')

  return putResponse




# �`�[���擾
def getSlipDitail(PartitionKey):
  queryData = slipDetailInfo.query(
      KeyConditionExpression = Key("slipNo").eq(PartitionKey) & Key("deleteDiv").eq("0")
  )
  if queryData['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(queryData)
    return queryData['Items']
  else:
    print('Post Successed.mechanic')
    return queryData['Items']



# �T�[�r�X���i���擾
def getSalesServiceInfo(PartitionKey):
  queryData = salesServiceInfo.query(
      KeyConditionExpression = Key("slipNo").eq(PartitionKey) & Key("deleteDiv").eq("0")
  )
  if queryData['ResponseMetadata']['HTTPStatusCode'] != 200:
    return queryData['Items']
  else:
    print('Post Successed.mechanic')
    return queryData['Items']


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  OperationType = event['OperationType']
  key = event['Keys']['slipNo']
  serviceKey = event['ServiceType']

  print(event['OperationType'])
  try:
    if OperationType == 'SENDQUESTION':
      if serviceKey == '0':
        slip = getSlipDitail(key)
        adminUser = slip[0]['slipAdminUserId']
        adminMecha = '0'
        adminOffice = '0'
        serviceTitle = slip[0]['title']
      else:
        service = getSalesServiceInfo(key)
        adminUser = service[0]['slipAdminUserId']
        adminMecha = service[0]['slipAdminMechanicId']
        adminOffice = service[0]['slipAdminOfficeId']
        serviceTitle = service[0]['title']
      PartitionKey = str(uuid.uuid4())
      return post_product(PartitionKey, event, adminUser, adminMecha, adminOffice, serviceKey, serviceTitle)

    else:
      return []

  except Exception as e:
      print("Error Exception.")
      print(e)