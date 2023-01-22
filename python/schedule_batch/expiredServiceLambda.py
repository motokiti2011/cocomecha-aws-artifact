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
userMyList = dynamodb.Table("userMyList")

# �m��T�[�r�X�ڍs

# �`�[���m��`�[���o
def slip_confirm():

    TIMESTAMP = get_timestamp()

    queryData = slipDetailInfo.query(
        IndexName = ' preferredDate-index',
        # �u������v�̃X�e�[�^�X���c���Ă���ꍇ���o
        KeyConditionExpression = Key("processStatus").eq("0")
        & Key("preferredDate").LT(TIMESTAMP)
    )
    items=queryData['Items']
    print(items)
    return items

# �T�[�r�X���i��񒊏o
def service_confirm():

    TIMESTAMP = get_timestamp()

    queryData = salesServiceInfo.query(
        IndexName = ' preferredDate-index',
        # �u�o�i���v�̃X�e�[�^�X���c���Ă���ꍇ���o
        KeyConditionExpression = Key("processStatus").eq("0")
        & Key("preferredDate").LT(TIMESTAMP)
    )
    items=queryData['Items']
    print(items)
    return items


# ������`�[���ɓ`�[����ǉ�
def expiredSlip_query(slip):
  putResponse = slipDetailInfo.put_item(
    Item={
      'slipNo' : PartitionKey,
      'deleteDiv' : slip['deleteDiv'],
      'category' : slip['category'],
      'slipAdminUserId' : slip['slipAdminUserId'],
      'adminDiv' : slip['adminDiv'],
      'title' : slip['title'],
      'areaNo1' : slip['areaNo1'],
      'areaNo2' : slip['areaNo2'],
      'price' : slip['price'],
      'bidMethod' : slip['bidMethod'],
      'bidderId' : slip['bidderId'],
      'bidEndDate' : slip['bidEndDate'],
      'explanation' : slip['explanation'],
      'displayDiv' : slip['displayDiv'],
      'processStatus' : '3',
      'targetService' : slip['targetService'],
      'targetVehicleId' : slip['targetVehicleId'],
      'targetVehicleName' : slip['targetVehicleName'],
      'targetVehicleInfo' : slip['targetVehicleInfo'],
      'workAreaInfo' : slip['workAreaInfo'],
      'preferredDate' : slip['preferredDate'],
      'preferredTime' : slip['preferredTime'],
      'completionDate' : slip['completionDate'],
      'transactionCompletionDate' : slip['transactionCompletionDate'],
      'thumbnailUrl' : slip['thumbnailUrl'],
      'imageUrlList' : slip['imageUrlList'],
      'messageOpenLebel' : slip['messageOpenLebel'],
      'updateUserId' : slip['updateUserId'],
      'created' : slip['created'],
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)


# ������`�[���ɃT�[�r�X����ǉ�
def expiredService_query(service):


  putResponse = transactionSlip.put_item(
    Item={
      'slipNo' : service['slipNo'],
      'deleteDiv' : service['deleteDiv'],
      'category' : service['category'],
      'slipAdminUserId' : service['slipAdminUserId'],
      'slipAdminOfficeId' : service['slipAdminOfficeId'],
      'slipAdminMechanicId' : service['slipAdminMechanicId'],
      'adminDiv' : service['adminDiv'],
      'title' : service['title'],
      'areaNo1' : service['areaNo1'],
      'areaNo2' : service['areaNo2'],
      'price' : service['price'],
      'bidMethod' : service['bidMethod'],
      'bidderId' : service['bidderId'],
      'bidEndDate' : service['bidEndDate'],
      'explanation' : service['explanation'],
      'displayDiv' : service['displayDiv'],
      'processStatus' : '3',
      'targetService' : service['targetService'],
      'targetVehicleId' : service['targetVehicleId'],
      'targetVehicleName' : service['targetVehicleName'],
      'targetVehicleInfo' : service['targetVehicleInfo'],
      'workAreaInfo' : service['workAreaInfo'],
      'preferredDate' : service['preferredDate'],
      'preferredTime' : service['preferredTime'],
      'completionDate' : service['completionDate'],
      'transactionCompletionDate' : service['transactionCompletionDate'],
      'thumbnailUrl' : service['thumbnailUrl'],
      'imageUrlList' : service['imageUrlList'],
      'messageOpenLebel' : service['messageOpenLebel'],
      'updateUserId' : service['updateUserId'],
      'created' : service['created'],
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)



# ���[�U�[�}�C���X�gTBL�`�[(�����؂ꃁ�b�Z�[�W�o�^)
def slipMylistMsg_query(slip):

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
      'category' : '11',
      'message' : 'EXPIRED',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)


# ���[�U�[�}�C���X�gTBL�T�[�r�X���i(�����؂ꃁ�b�Z�[�W�o�^)
def serviceMylistMsg_query(serivice):

  now = datetime.now()

  putResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : serivice['slipAdminUserId'],
      'mechanicId' : serivice['slipAdminMechanicId'],
      'officeId' :serivice['slipAdminOfficeId'],
      'serviceType' : serivice['targetService'],
      'slipNo' : serivice['slipNo'],
      'serviceTitle' : serivice['title'],
      'category' : '11',
      'message' : 'EXPIRED',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)




# �o�b�`���s���̃^�C���X�^���v�쐬
def get_timestamp():
    now = datetime.now()    
    rand_minute = int(random.uniform(0, 59))
    rand_second = int(random.uniform(0, 59))
    nowTime = datetime(now.year, now.month, now.day, now.hour, rand_minute, rand_second)
    return int(nowTime.timestamp()) * 1000


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:
    if OperationType == 'EXPIREDSERVICE':
      # �����؂�`�[�`�F�b�N
      
      # �`�[�`�F�b�N
      expiredSlipData = slip_confirm()

      # �Ώۓ`�[�����݂���ꍇ
      if(len(expiredSlipData) > 0 :
          for slip in expiredSlipData :
            # �Ώۓ`�[�̃X�e�[�^�X���X�V
            expiredSlip_query(slip)
            # �}�C���X�gTBL�Ƀ��b�Z�[�W��ǉ��i�����؂�j
            slipMylistMsg_query(slip['slipNo'])

      # �T�[�r�X���i�`�F�b�N
      expiredServiceData = service_confirm()
      if(len(expiredServiceData) > 0 :
      # �ΏۃT�[�r�X�����݂���ꍇ�폜
          for service in expiredServiceData :
            # �ΏۃT�[�r�X�̃X�e�[�^�X���X�V
            expiredService_query(service)
            # �}�C���X�gTBL�Ƀ��b�Z�[�W��ǉ��i�����؂�j
            serviceMylistMsg_query(service)

  except Exception as e:
      print("Error Exception.")
      print(e)