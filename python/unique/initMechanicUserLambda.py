import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key



dynamodb = boto3.resource('dynamodb')

mechanictable = dynamodb.Table("mechanicInfo")
usertable = dynamodb.Table("userInfo")
officetable = dynamodb.Table("officeInfo")

# ���J�j�b�N�e�[�u���X�V
def mechanic_post(PartitionKey, officeId, event):
  putResponse = mechanictable.put_item(
    Item={
      'mechanicId' : PartitionKey,
      'validDiv' : event['Keys']['validDiv'],
      'mechanicName' : event['Keys']['mechanicName'],
      'adminUserId' : event['Keys']['adminUserId'],
      'adminAddressDiv' : event['Keys']['adminAddressDiv'],
      'telList' : event['Keys']['telList'],
      'mailAdress' : event['Keys']['mailAdress'],
      'areaNo1' : event['Keys']['areaNo1'],
      'areaNo2' : event['Keys']['areaNo2'],
      'adress' : event['Keys']['adress'],
      'officeConnectionDiv' : event['Keys']['officeConnectionDiv'],
      'officeId' : officeId,
      'qualification' : event['Keys']['qualification'],
      'specialtyWork' : event['Keys']['specialtyWork'],
      'profileImageUrl' : event['Keys']['profileImageUrl'],
      'introduction' : event['Keys']['introduction'],
      'evaluationInfoIdList' : event['Keys']['evaluationInfoIdList'],
      'updateUserId' : event['Keys']['updateUserId'],
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.mechanic')
    return putResponse


# �H��e�[�u��
def office_post(userId, mechanicId, officeId, event):
  
  adminId = [userId]
  employee = [mechanicId]
  
  mechanicInfoList = [{
    mechanicId: mechanicId
    mechanicName: event['Keys']['mechanicName'],
    belongsDiv: : NONE, 
    belongs: : NONE
  }]
  
  adminInfoList = [{
    mechanicId : mechanicId,
    mechanicName : event['Keys']['mechanicName'],
    belongsDiv : NONE,
    belongs : NONE,
    role : '�Ǘ���',
    roleDiv : '�Ǘ���'
  }]


  putResponse = officetable.put_item(
    Item={
      'officeId' : officeId,
      'connectionMechanicInfo' : mechanicInfoList,
      'adminSettingInfo' : adminInfoList,
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.mechanic')
    return putResponse


# ���[�U�[�e�[�u��
def user_post(userId, mechanicId, officeId, officeDiv, event):
  role = []
  if officeDiv == '1':
    role.append('ADMIN')
  
  # �X�V�Ώۃf�[�^���擾
  queryData = usertable.query(
    KeyConditionExpression = Key("userId").eq(userId)
  )
  items=queryData['Items']

  # ���J�j�b�NID�A�H��ID�A���[�����X�V  
  putResponse = usertable.put_item(
    Item={
      'userId' : userId,
      'userValidDiv' : items[0]['userValidDiv'],
      'corporationDiv' : items[0]['corporationDiv'],
      'userName' : items[0]['userName'],
      'mailAdress' : items[0]['mailAdress'],
      'TelNo1' : items[0]['TelNo1'],
      'TelNo2' : items[0]['TelNo2'],
      'areaNo1' : items[0]['areaNo1'],
      'areaNo2' : items[0]['areaNo2'],
      'adress' : items[0]['adress'],
      'postCode' : items[0]['postCode'],
      'mechanicId' : mechanicId,
      'officeId' : officeId,
      'baseId' : items[0]['baseId'],
      'officeRole' : role,
      'profileImageUrl' : items[0]['profileImageUrl'],
      'introduction' : items[0]['introduction'],
      'updateUserId' : items[0]['updateUserId'],
      'created' : items[0]['created'],
      'updated' : items[0]['updated']
    }
  )

  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
      print(putResponse)
  else:
      print('PUT Successed.userInfo')
  return putResponse


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  officeDiv = '0'
  print(now)
  OperationType = event['OperationType']
  id = str(uuid.uuid4())

  try:
    mechanicId = id
    officeId = '0'
    # ���J�j�b�N�o�^
    if OperationType == 'INITMECHANIC':
      officeDiv = '0'
    # ��Ɠo�^�������Ȃ��ꍇ
    elif OperationType == 'INITMECHANICANDOFFICE':
      officeDiv = '1'
      officeId = str(uuid.uuid4())

    # ���J�j�b�N����o�^
    mechanicResponse = mechanic_post(mechanicId, officeId, event)
    if mechanicResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
      print(mechanicResponse)
      return mechanicResponse['ResponseMetadata']['HTTPStatusCode']
    else:
      print('PUT Successed.mechanic')

    # ��Ə��Ƀ��J�j�b�N����ǉ�
    if officeDiv == '1':
      officeResponse = office_post(userId, mechanicId, event)
      print(officeResponse)

      if officeResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(officeResponse)
        return officeResponse['ResponseMetadata']['HTTPStatusCode']
      else:
        print('PUT Successed.office')

    # ���J�j�b�N�A�H��̓o�^�������[�U�[�e�[�u���ɓo�^
    userId = event['Keys']['adminUserId']
    userResponse = user_post(userId, mechanicId, officeId, officeDiv, event)
    if userResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
      print(userResponse)
      return userResponse['ResponseMetadata']['HTTPStatusCode']
    else:
      print('PUT Successed.user')
        
    return mechanicResponse['ResponseMetadata']['HTTPStatusCode']

  except Exception as e:
      print("Error Exception.")
      print(e)