import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("serviceTransactionRequest")
table2 = dynamodb.Table("userMyList")


# ����˗�TBL
def post_transactionRequest(PartitionKey, event, adminUser, confirmUser):

  # ����˗�TBL(�Ǘ���)
  now = datetime.now()
  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'slipNo' : event['Keys']['slipNo'],
      'requestId' : event['Keys']['requestId'],
      'serviceUserType' : event['Keys']['serviceUserType'],
      'requestType' : event['Keys']['requestType'],
      'files' : event['Keys']['files'],
      'requestStatus' : event['Keys']['requestStatus'],
      'confirmDiv' : '1',
      'deadline' : event['Keys']['deadline'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')


  # �`�[���ɕR�Â��˗��ҏ����擾
  PartitionKey = event['Keys']['slipNo']
  requestUserTransaction = transactionSlipNo_query(PartitionKey)


  for item in requestUserTransaction :
    # �Ǘ����[�U�[�ȊO�i�˗��ҁj�̃X�e�[�^�X�X�V
    if adminUser != item['requestId'] :
      if confirmUser != item['requestId'] :
        postAnConfirmTransactionRequest(item)
      elif confirmUser == item['requestId'] :
        postConfirmTransactionRequest(item)

  return putResponse


# �}�C���X�gTBL
def post_myList(PartitionKey, event, adminUser, confirmUser)):
  # �}�C���X�gTBL�̓o�^
  # �`�[�Ǘ���
  userMyListAdminResponse = table2.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : event['Keys']['slipAdminUserId'],
      'mechanicId : event['Keys']['slipAdminMechanicId'],
      'officeId' : event['Keys']['slipAdminOfficeId'],
      'serviceType' : event['Keys']['targetService'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : event['Keys']['serviceTitle'],
      'category' : '10',
      'message' : '',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')

    }
  )
  
  if userMyListAdminResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListAdminResponse)
  else:
    print('Post Successed.')


  # ������̃}�C���X�g�����擾
  requestMyList = mylist_slipNo_query( event['Keys']['slipNo'])

  for item in requestMyList :
    # �Ǘ����[�U�[�ȊO�i�˗��ҁj�̃X�e�[�^�X�X�V
    if adminUser != item['requestId'] :
      if confirmUser != item['requestId'] :
        postAnConfirmMylistRequest(item)
      elif confirmUser == item['requestId'] :
        postConfirmMylistRequest(item)

  return userMyListAdminResponse


# �`�[�ԍ��ɕR�Â�����˗�TBL���擾
def transactionSlipNo_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipNo-index',
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# ����˗�TBL(�˗���(�m��ȊO)�f�[�^�X�V)
def postAnConfirmTransactionRequest(item):

  # ����˗�TBL(�Ǘ���)
  now = datetime.now()
  putResponse = table.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'serviceUserType' : item['serviceUserType'],
      'requestType' : item['requestType'],
      'files' : item['files'],
      'requestStatus' : item['requestStatus'],
      'confirmDiv' : '9',
      'deadline' : item['deadline'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.')


# ����˗�TBL(�˗���(�m��)�f�[�^�X�V)
def postConfirmTransactionRequest(item):

  # ����˗�TBL(�Ǘ���)
  now = datetime.now()
  putResponse = table.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'serviceUserType' : item['serviceUserType'],
      'requestType' : item['requestType'],
      'files' : item['files'],
      'requestStatus' : item['requestStatus'],
      'confirmDiv' : '1',
      'deadline' : item['deadline'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.')


# �`�[�ԍ��ɕR�Â����[�U�[�}�C���X�gTBL���擾
def mylist_slipNo_query(partitionKey):
    queryData = table2.query(
        IndexName = 'slipNo-index',
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# ���[�U�[�}�C���X�gTBL(�˗��҃f�[�^�X�V)
def postAnConfirmMylistRequest(item):

  # ����˗�TBL(�Ǘ���)
  now = datetime.now()
  putResponse = table2.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'serviceUserType' : item['serviceUserType'],
      'requestType' : item['requestType'],
      'files' : item['files'],
      'requestStatus' : '16',
      'confirmDiv' : '0',
      'deadline' : item['deadline'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.')


# ���[�U�[�}�C���X�gTBL(�˗��҃f�[�^�X�V)
def postConfirmMylistRequest(item):

  # ����˗�TBL(�Ǘ���)
  now = datetime.now()
  putResponse = table2.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'serviceUserType' : item['serviceUserType'],
      'requestType' : item['requestType'],
      'files' : item['files'],
      'requestStatus' : '15',
      'confirmDiv' : '1',
      'deadline' : item['deadline'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.')


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']
  adminUser = event['AdminUser']
  confirmUser = event['confirmUser']
  try:
    if OperationType == 'CONFIRMTRANSACTION':
      id = str(uuid.uuid4())
      PartitionKey = id
      post_transactionRequest(PartitionKey, event, adminUser, confirmUser)
      post_myList(PartitionKey, event, adminUser, confirmUser)

  except Exception as e:
      print("Error Exception.")
      print(e)