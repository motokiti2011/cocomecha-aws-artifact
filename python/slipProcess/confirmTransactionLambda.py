import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
serviceTransactionRequest = dynamodb.serviceTransactionRequest("serviceTransactionRequest")
userMyList = dynamodb.serviceTransactionRequest("userMyList")
slipDetailInfo = dynamodb.serviceTransactionRequest("slipDetailInfo")
salesServiceInfo = dynamodb.serviceTransactionRequest("salesServiceInfo")
transactionSlip = dynamodb.serviceTransactionRequest("transactionSlip")

# ����˗�TBL
def post_transactionRequest(PartitionKey, event, adminUser, confirmUser):

  # ����˗�TBL(�Ǘ���)
  now = datetime.now()
  putResponse = serviceTransactionRequest.put_item(
    Item={
      'id' : PartitionKey,
      'slipNo' : event['Keys']['slipNo'],
      'requestId' : event['Keys']['requestId'],
      'requestUserName' : event['Keys']['requestUserName'],
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
    print('post_transactionRequest : Post Successed.')


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
def post_myList(PartitionKey, event, adminUser, confirmUser,adminMecha,adminOffice,serviceTitle):
  
  now = datetime.now()
  # �}�C���X�gTBL�̓o�^
  # �`�[�Ǘ���
  userMyListAdminResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : adminUser,
      'mechanicId' : adminMecha,
      'officeId' : adminOffice,
      'serviceType' : event['Keys']['serviceUserType'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : serviceTitle,
      'category' : '10',
      'message' : 'TRAN_ST',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')

    }
  )
  print('2C')
  if userMyListAdminResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListAdminResponse)
  else:
    print('post_myList : Post Successed.')

  print('2D')
  # ������̃}�C���X�g�����擾
  requestMyList = mylist_slipNo_query( event['Keys']['slipNo'])

  for item in requestMyList :
    # �Ǘ����[�U�[�ȊO�i�˗��ҁj�̃X�e�[�^�X�X�V
    if adminUser != item['userId'] :
      if confirmUser != item['userId'] :
        postAnConfirmMylistRequest(item)
      elif confirmUser == item['userId'] :
        postConfirmMylistRequest(item)

  return userMyListAdminResponse


# �`�[�ԍ��ɕR�Â�����˗�TBL���擾
def transactionSlipNo_query(partitionKey):
    queryData = serviceTransactionRequest.query(
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
  putResponse = serviceTransactionRequest.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'requestUserName' : item['requestUserName'],
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
    print('AnConfirmTransactionRequest : Post Successed.')


# ����˗�TBL(�˗���(�m��)�f�[�^�X�V)
def postConfirmTransactionRequest(item):

  # ����˗�TBL(�Ǘ���)
  now = datetime.now()
  putResponse = serviceTransactionRequest.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'requestUserName' : item['requestUserName'],
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
    print('ConfirmTransactionRequest : Post Successed.')


# �`�[�ԍ��ɕR�Â����[�U�[�}�C���X�gTBL���擾
def mylist_slipNo_query(partitionKey):
    queryData = userMyList.query(
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
  putResponse = serviceTransactionRequest.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'requestUserName' : item['requestUserName'],
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
    print('AnConfirmMylistRequest : Post Successed.')


# ���[�U�[�}�C���X�gTBL(�˗��҃f�[�^�X�V)
def postConfirmMylistRequest(item):

  # ����˗�TBL(�Ǘ���)
  now = datetime.now()
  putResponse = serviceTransactionRequest.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'requestUserName' : item['requestUserName'],
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
    print('ConfirmMylistRequest : Post Successed.')



# �`�[���擾
def getSlipDitail(PartitionKey,serviceKey):
  queryData = slipDetailInfo.query(
      KeyConditionExpression = Key("slipNo").eq(PartitionKey) & Key("deleteDiv").eq("0")
  )
  if queryData['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(queryData)
    return queryData['Items']
  else:
    print('Post Successed : slipDetailInfo')
    postTransactionSlip(queryData['Items'],serviceKey)
    return queryData['Items']


# �T�[�r�X���i���擾
def getSalesServiceInfo(PartitionKey,serviceKey):
  queryData = salesServiceInfo.query(
      KeyConditionExpression = Key("slipNo").eq(PartitionKey) & Key("deleteDiv").eq("0")
  )
  if queryData['ResponseMetadata']['HTTPStatusCode'] != 200:
    return queryData['Items']
  else:
    print('Post Successed : salesServiceInfo')
    postTransactionSlip(queryData['Items'],serviceKey)
    return queryData['Items']



# ������`�[���ǉ�
def postTransactionSlip(queryData,serviceKey):

  now = datetime.now()
  print('3A')
  print(queryData)
  if serviceKey == '0':
    adminUser = queryData[0]['slipAdminUserId']
    adminMecha = '0'
    adminOffice = '0'
    adminId = queryData[0]['slipAdminUserId']
  elif serviceKey == '1':
    adminUser = queryData[0]['slipAdminUserId']
    adminMecha = queryData[0]['slipAdminMechanicId']
    adminOffice = queryData[0]['slipAdminOfficeId']
    adminId = queryData[0]['slipAdminOfficeId']
  elif serviceKey == '2':
    adminUser = queryData[0]['slipAdminUserId']
    adminMecha = queryData[0]['slipAdminMechanicId']
    adminOffice = queryData[0]['slipAdminOfficeId']
    adminId = queryData[0]['slipAdminMechanicId']

  print('3B')

  # ����`�[���ɓo�^
  putResponse = transactionSlip.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'serviceType' : serviceKey,
      'userId' : adminUser,
      'mechanicId' : adminMecha,
      'officeId' : adminOffice,
      'slipNo' : queryData[0]['slipNo'],
      'serviceTitle' : queryData[0]['title'],
      'slipRelation' : '1',
      'slipAdminId' : adminId,
      'slipAdminName' : '',
      'bidderId' : queryData[0]['bidderId'],
      'deleteDiv' : '0',
      'completionScheduledDate' : '',
      'created' : now.strftime('%x %X'),
      'updated' :  now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('transactionSlip : Post Successed.')
  return 



# �`�[���F�_���폜
def put_SlipDitail(queryData):
  now = datetime.now()
  putResponse = slipDetailInfo.put_item(
    Item={
      'slipNo' : queryData[0]['slipNo'],
      'deleteDiv' : '1',
      'category' : queryData[0]['category'],
      'slipAdminUserId' :queryData[0]['slipAdminUserId'],
      'adminDiv' : queryData[0]['adminDiv'],
      'title' : queryData[0]['title'],
      'areaNo1' : queryData[0]['areaNo1'],
      'areaNo2' : queryData[0]['areaNo2'],
      'price' : queryData[0]['price'],
      'bidMethod' : queryData[0]['bidMethod'],
      'bidderId' : queryData[0]['bidderId'],
      'bidEndDate' : queryData[0]['bidEndDate'],
      'explanation' : queryData[0]['explanation'],
      'displayDiv' : queryData[0]['displayDiv'],
      'processStatus' : queryData[0]['processStatus'],
      'targetService' : queryData[0]['targetService'],
      'targetVehicleId' : queryData[0]['targetVehicleId'],
      'targetVehicleName' : queryData[0]['targetVehicleName'],
      'targetVehicleInfo' : queryData[0]['targetVehicleInfo'],
      'workAreaInfo' : queryData[0]['workAreaInfo'],
      'preferredDate' : queryData[0]['preferredDate'],
      'preferredTime' : queryData[0]['preferredTime'],
      'completionDate' : queryData[0]['completionDate'],
      'transactionCompletionDate' : queryData[0]['transactionCompletionDate'],
      'thumbnailUrl' : queryData[0]['thumbnailUrl'],
      'imageUrlList' : queryData[0]['imageUrlList'],
      'messageOpenLebel' : queryData[0]['messageOpenLebel'],
      'updateUserId' : queryData[0]['updateUserId'],
      'created' : queryData[0]['created'],
      'updated' :  now.strftime('%x %X')
    }
  )
  print('putRes')
  print(putResponse)

  delResponse = slipDetailInfo.delete_item(
     Key={
         'slipNo': queryData[0]['slipNo'],
         'deleteDiv': '0'
     }
  )
  print('delRes')
  print(delResponse)
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('put_SlipDitail : Post Successed.')
  return 


# �T�[�r�X���i���F�_���폜
def put_SalesServiceInfo(queryData):
  now = datetime.now()
  putResponse = salesServiceInfo.put_item(
    Item={
      'slipNo' : queryData[0]['slipNo'],
      'deleteDiv' : '1',
      'category' : queryData[0]['category'],
      'slipAdminUserId' : queryData[0]['slipAdminUserId'],
      'slipAdminOfficeId' : queryData[0]['slipAdminOfficeId'],
      'slipAdminMechanicId' : queryData[0]['slipAdminMechanicId'],
      'adminDiv' : queryData[0]['adminDiv'],
      'title' : queryData[0]['title'],
      'areaNo1' : queryData[0]['areaNo1'],
      'areaNo2' : queryData[0]['areaNo2'],
      'price' : queryData[0]['price'],
      'bidMethod' : queryData[0]['bidMethod'],
      'bidderId' : queryData[0]['bidderId'],
      'bidEndDate' : queryData[0]['bidEndDate'],
      'explanation' : queryData[0]['explanation'],
      'displayDiv' : queryData[0]['displayDiv'],
      'processStatus' : queryData[0]['processStatus'],
      'targetService' : queryData[0]['targetService'],
      'targetVehicleId' : queryData[0]['targetVehicleId'],
      'targetVehicleName' : queryData[0]['targetVehicleName'],
      'targetVehicleInfo' : queryData[0]['targetVehicleInfo'],
      'workAreaInfo' : queryData[0]['workAreaInfo'],
      'preferredDate' : queryData[0]['preferredDate'],
      'preferredTime' : queryData[0]['preferredTime'],
      'completionDate' : queryData[0]['completionDate'],
      'transactionCompletionDate' : queryData[0]['transactionCompletionDate'],
      'thumbnailUrl' : queryData[0]['thumbnailUrl'],
      'imageUrlList' : queryData[0]['imageUrlList'],
      'messageOpenLebel' : queryData[0]['messageOpenLebel'],
      'updateUserId' : queryData[0]['updateUserId'],
      'created' : queryData[0]['created'],
      'updated' :  now.strftime('%x %X')
    }
  )
  
  delResponse = salesServiceInfo.delete_item(
     Key={
         'slipNo': queryData[0]['slipNo'],
         'deleteDiv': '0'
     }
  )
  print('delRes')
  print(delResponse)
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('put_SlipDitail : Post Successed.')
  return 
  

def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']
  adminUser = event['Keys']['adminUser']
  confirmUser = event['Keys']['confirmUser']
  serviceKey = event['Keys']['serviceUserType']
  key = event['Keys']['slipNo']
  
  try:
    if OperationType == 'CONFIRMTRANSACTION':

      if serviceKey == '0':
        slip = getSlipDitail(key,serviceKey)
        # adminUser = slip[0]['slipAdminUserId']
        adminMecha = '0'
        adminOffice = '0'
        serviceTitle = slip[0]['title']
        # �K�v�f�[�^�擾��ɓ`�[����_���폜
        put_SlipDitail(slip)
      else:
        service = getSalesServiceInfo(key,serviceKey)
        # adminUser = service[0]['slipAdminUserId']
        adminMecha = service[0]['slipAdminMechanicId']
        adminOffice = service[0]['slipAdminOfficeId']
        serviceTitle = service[0]['title']
        # �K�v�f�[�^�擾��ɃT�[�r�X���i��_���폜
        put_SalesServiceInfo(service)

      id = str(uuid.uuid4())
      PartitionKey = id
      print('1A')
      post_transactionRequest(PartitionKey, event, adminUser, confirmUser)
      print('2B')
      post_myList(PartitionKey, event, adminUser, confirmUser,adminMecha,adminOffice, serviceTitle)

  except Exception as e:
      print("Error Exception.")
      print(e)