import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
transactionSlip = dynamodb.Table("transactionSlip")
slipDetailInfo = dynamodb.Table("slipDetailInfo")
salesServiceInfo = dynamodb.Table("salesServiceInfo")
userMyList = dynamodb.Table("userMyList")
completionSlip = dynamodb.Table("completionSlip")


# �X�P�W���[���o�b�` ��������`�[�̒��o
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  print('TRANSACTIONEND')

  try:
    # ����������z��������𒊏o
    endTransaction = delete_transaction_query()
    if(len(endTransaction) > 0 :
      for service in endTransaction :
        # �������_���폜
        logcaldelete_query(service)
        if service['serviceType'] == '0':
          # �`�[�����擾���_���폜����
          slip = slipDetailInfo_query(service['slipNo'])
          # ����I��TBL�ɏ���o�^����
          completionSlip_query(slip)
          # �}�C���X�gTBL�Ƀ��b�Z�[�W��ݒ肷��(����������b�Z�[�W�{�]���˗����b�Z�[�W)
          setMyListMsg_query(slip)
        elif service['serviceType'] == '1' or '2':
          # �T�[�r�X���i���擾���_���폜����
          salesService = salesServiceInfo_query(service['slipNo'])
          # ����I��TBL�ɏ���o�^����
          completionSalesService_query(salesService)
          # �}�C���X�gTBL�Ƀ��b�Z�[�W��ݒ肷��(����������b�Z�[�W�{�]���˗����b�Z�[�W)
          setMyListMsgSales_query(salesService)
  except Exception as e:
      print("Error Exception.")
      print(e)


# ������`�[���̍폜�Ώۂ̏��𒊏o
def delete_transaction_query():

    TIMESTAMP = get_timestamp()

    queryData = transactionSlip.query(
        IndexName = 'ttlDate-index',
        KeyConditionExpression = Key("deleteDiv").eq("0") & Key("ttlDate").LT(TIMESTAMP)
    )
    items=queryData['Items']
    print(items)
    return items


# �`�[���𒊏o���_���폜����
def slipDetailInfo_query(partitionKey):

    TIMESTAMP = get_timestamp()

    queryData = slipDetailInfo.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey) & Key("deleteDiv").eq("0")
    )
    items=queryData['Items']

    putResponse = table.put_item(
      Item={
        'slipNo' : items['0']['slipNo'],
        'deleteDiv' : '1',
        'category' : items['0']['category'],
        'slipAdminUserId' : items['0']['slipAdminUserId'],
        'adminDiv' : items['0']['adminDiv'],
        'title' : items['0']['title'],
        'areaNo1' : items['0']['areaNo1'],
        'areaNo2' : items['0']['areaNo2'],
        'price' : items['0']['price'],
        'bidMethod' : items['0']['bidMethod'],
        'bidderId' : items['0']['bidderId'],
        'bidEndDate' : items['0']['bidEndDate'],
        'explanation' : items['0']['explanation'],
        'displayDiv' : items['0']['displayDiv'],
        'processStatus' : items['0']['processStatus'],
        'targetService' : items['0']['targetService'],
        'targetVehicleId' : items['0']['targetVehicleId'],
        'targetVehicleName' : items['0']['targetVehicleName'],
        'targetVehicleInfo' : items['0']['targetVehicleInfo'],
        'workAreaInfo' : items['0']['workAreaInfo'],
        'preferredDate' : items['0']['preferredDate'],
        'preferredTime' : items['0']['preferredTime'],
        'completionDate' : items['0']['completionDate'],
        'transactionCompletionDate' : items['0']['transactionCompletionDate'],
        'thumbnailUrl' : items['0']['thumbnailUrl'],
        'imageUrlList' : items['0']['imageUrlList'],
        'messageOpenLebel' : items['0']['messageOpenLebel'],
        'updateUserId' : items['0']['updateUserId'],
        'created' : items['0']['created'],
        'updated' : items['0']['updated']
    }
  )

    return items['0']


# �T�[�r�X���i���𒊏o���_���폜����
def salesServiceInfo_query(primaryKey):

    TIMESTAMP = get_timestamp()

    queryData = salesServiceInfo.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey) & Key("deleteDiv").eq("0")
    )
    items=queryData['Items']

    putResponse = table.put_item(
      Item={
        'slipNo' : items['0']['slipNo'],
        'deleteDiv' : '1',
        'category' : items['0']['category'],
        'slipAdminUserId' : items['0']['slipAdminUserId'],
        'slipAdminOfficeId' : items['0']['slipAdminOfficeId'],
        'slipAdminMechanicId' : items['0']['slipAdminMechanicId'],
        'adminDiv' : items['0']['adminDiv'],
        'title' : items['0']['title'],
        'areaNo1' : items['0']['areaNo1'],
        'areaNo2' : items['0']['areaNo2'],
        'price' : items['0']['price'],
        'bidMethod' : items['0']['bidMethod'],
        'bidderId' : items['0']['bidderId'],
        'bidEndDate' : items['0']['bidEndDate'],
        'explanation' : items['0']['explanation'],
        'displayDiv' : items['0']['displayDiv'],
        'processStatus' : items['0']['processStatus'],
        'targetService' : items['0']['targetService'],
        'targetVehicleId' : items['0']['targetVehicleId'],
        'targetVehicleName' : items['0']['targetVehicleName'],
        'targetVehicleInfo' : items['0']['targetVehicleInfo'],
        'workAreaInfo' : items['0']['workAreaInfo'],
        'preferredDate' : items['0']['preferredDate'],
        'preferredTime' : items['0']['preferredTime'],
        'completionDate' : items['0']['completionDate'],
        'transactionCompletionDate' : items['0']['transactionCompletionDate'],
        'thumbnailUrl' : items['0']['thumbnailUrl'],
        'imageUrlList' : items['0']['imageUrlList'],
        'messageOpenLebel' : items['0']['messageOpenLebel'],
        'updateUserId' : items['0']['updateUserId'],
        'created' : items['0']['created'],
        'updated' : datetime.now()
      }
    )

    return items['0']


# ����`�[���_���폜
def logcaldelete_query(service):
  putResponse = transactionSlip.put_item(
    Item={
      'id' : service['id'],
      'serviceType' : service['serviceType'],
      'userId' : service['userId'],
      'mechanicId' : service['mechanicId'],
      'officeId' : service['officeId'],
      'slipNo' : service['slipNo'],
      'serviceTitle' : service['serviceTitle'],
      'slipRelation' : service['slipRelation'],
      'slipAdminId' : service['slipAdminId'],
      'slipAdminName' :  service['slipAdminName'],
      'bidderId' : service['bidderId'],
      'deleteDiv' : '1',
      'completionScheduledDate' : service['completionScheduledDate'],
      'ttlDate' : service['ttlDate'],
      'created' : event['Keys']['created'],
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)


# ��������`�[���o�^(�`�[)
def completionSlip_query(slip):

  now = datetime.now()

  putResponse = transactionSlip.put_item(
    Item={
      'slipNo' : slip['slipNo'],
      'slipAdminUserId' : slip['slipAdminUserId'],
      'slipAdminOfficeId' : '0',
      'slipAdminMechanicId' : '0',
      'adminDiv' : slip['adminDiv'],
      'title' : slip['title'],
      'price' : slip['price'],
      'bidMethod' : slip['bidMethod'],
      'bidderId' : slip['bidderId'],
      'bidEndDate' : slip['bidEndDate'],
      'explanation' : slip['explanation'],
      'targetService' : slip['targetService'],
      'targetVehicleId' : slip['targetVehicleId'],
      'targetVehicleName' : slip['targetVehicleName'],
      'targetVehicleInfo' : slip['targetVehicleInfo'],
      'workAreaInfo' : slip['workAreaInfo'],
      'evaluationId' :'0',
      'completionDate' : slip['completionDate'],
      'transactionCompletionDate' : slip['transactionCompletionDate'],
      'thumbnailUrl' : slip['thumbnailUrl'],
      'imageUrlList' : slip['imageUrlList'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )

  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)



# ��������`�[���o�^�i�T�[�r�X���i�j
def completionSlip_query(service):

  now = datetime.now()

  putResponse = salesServiceInfo.put_item(
    Item={
      'slipNo' : service['slipNo'],
      'slipAdminUserId' : service['slipAdminUserId'],
      'slipAdminOfficeId' : service['slipAdminOfficeId'],
      'slipAdminMechanicId' : service['slipAdminMechanicId'],
      'adminDiv' : service['adminDiv'],
      'title' : service['title'],
      'price' : service['price'],
      'bidMethod' : service['bidMethod'],
      'bidderId' : service['bidderId'],
      'bidEndDate' : service['bidEndDate'],
      'explanation' : service['explanation'],
      'targetService' : service['targetService'],
      'targetVehicleId' : service['targetVehicleId'],
      'targetVehicleName' : service['targetVehicleName'],
      'targetVehicleInfo' : service['targetVehicleInfo'],
      'workAreaInfo' : service['workAreaInfo'],
      'evaluationId' :'0',
      'completionDate' : service['completionDate'],
      'transactionCompletionDate' : service['transactionCompletionDate'],
      'thumbnailUrl' : service['thumbnailUrl'],
      'imageUrlList' : service['imageUrlList'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )

  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)



# ���[�U�[�}�C���X�gTBL�`�[(����������b�Z�[�W�{�]���˗����b�Z�[�W)
def setMyListMsg_query(slip):

  now = datetime.now()

  putResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : slip['slipAdminUserId'],
      'mechanicId' : '0',
      'officeId' : '0',
      'serviceType' : '0',
      'slipNo' : slip['slipNo'],
      'serviceTitle' : slip['title'],
      'category' : '17',
      'message' : 'TRAN_COMP',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse2['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)

  putResponse2 = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : slip['slipAdminUserId'],
      'mechanicId' : '0',
      'officeId' : '0',
      'serviceType' : '0',
      'slipNo' : slip['slipNo'],
      'serviceTitle' : slip['title'],
      'category' : '21',
      'message' : 'EVALUATION_REQ',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)


# ���[�U�[�}�C���X�gTBL�`�[(����������b�Z�[�W�{�]���˗����b�Z�[�W)
def setMyListMsgSales_query(service):

  now = datetime.now()

  putResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : service['slipAdminUserId'],
      'mechanicId' : service['slipAdminMechanicId'],
      'officeId' : service['slipAdminOfficeId'],
      'serviceType' : service['targetService'],
      'slipNo' : service['slipNo'],
      'serviceTitle' : service['title'],
      'category' : '17',
      'message' : 'TRAN_COMP',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)

  putResponse2 = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : service['slipAdminUserId'],
      'mechanicId' : service['slipAdminMechanicId'],
      'officeId' : service['slipAdminOfficeId'],
      'serviceType' : service['targetService'],
      'slipNo' : service['slipNo'],
      'serviceTitle' : service['title'],
      'category' : '21',
      'message' : 'EVALUATION_REQ',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse2['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)




# �o�b�`���s���̃^�C���X�^���v�쐬
def get_timestamp():
    now = datetime.now()
    rand_minute = int(random.uniform(0, 59))
    rand_second = int(random.uniform(0, 59))
    nowTime = datetime(now.year, now.month, now.day, now.hour, rand_minute, rand_second)
    return int(nowTime.timestamp()) * 1000


