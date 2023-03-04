import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key



dynamodb = boto3.resource('dynamodb')

mechanictable = dynamodb.Table("mechanicInfo")
usertable = dynamodb.Table("userInfo")
officetable = dynamodb.Table("officeInfo")


# 工場テーブル
def office_post(userId, mechanicId, officeId, event):
  
  adminId = [userId]
  employee = [mechanicId]
  putResponse = officetable.put_item(
    Item={
      'officeId' : officeId,
      'officeName' : event['Keys']['officeName'],
      'officeTel' : event['Keys']['officeTel'],
      'officeMailAdress' : event['Keys']['officeMailAdress'],
      'officeArea1' : event['Keys']['officeArea1'],
      'officeArea' : event['Keys']['officeArea'],
      'officeAdress' : event['Keys']['officeAdress'],
      'officePostCode' : event['Keys']['officePostCode'],
      'workContentList' : event['Keys']['workContentList'],
      'businessHours' : event['Keys']['businessHours'],
      'connectionOfficeInfo' : event['Keys']['connectionOfficeInfo'],
      'connectionMechanicInfo' : event['Keys']['connectionMechanicInfo'],
      'adminSettingInfo' : event['Keys']['adminSettingInfo'],
      'officePR' : event['Keys']['officePR'],
      'officePRimageURL' : event['Keys']['officePRimageURL'],
      'officeFormList' : event['Keys']['officeFormList'],
      'publicInfo' : event['Keys']['publicInfo'],
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.offuceM')
    return putResponse


# メカニックテーブル更新(オフィスID追加)
def mechanic_post(mechanicId, officeId,  event):

  print(mechanicId)
  # 更新対象データを取得
  queryData = mechanictable.query(
    KeyConditionExpression = Key("mechanicId").eq(mechanicId)
  )
  items=queryData['Items']

  putResponse = mechanictable.put_item(
    Item={
      'mechanicId' : items[0]['mechanicId'],
      'validDiv' : items[0]['validDiv'],
      'mechanicName' : items[0]['mechanicName'],
      'adminUserId' : items[0]['adminUserId'],
      'adminAddressDiv' : items[0]['adminAddressDiv'],
      'telList' : items[0]['telList'],
      'mailAdress' : items[0]['mailAdress'],
      'officeConnectionDiv' : items[0]['officeConnectionDiv'],
      'officeId' : officeId,
      'qualification' : items[0]['qualification'],
      'specialtyWork' : items[0]['specialtyWork'],
      'profileImageUrl' : items[0]['profileImageUrl'],
      'introduction' : items[0]['introduction'],
      'evaluationInfoIdList' : items[0]['evaluationInfoIdList'],
      'updateUserId' : items[0]['updateUserId'],
      'created' : items[0]['created'],
      'updated' : items[0]['updated']
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.mechanic')
    return putResponse


# ユーザーテーブル(オフィスID追加)
def user_post(userId, officeId, event):
  role = []
  role.append('ADMIN')
  
  # 更新対象データを取得
  queryData = usertable.query(
    KeyConditionExpression = Key("userId").eq(userId)
  )
  items=queryData['Items']

  # 工場ID、ロールを更新  
  putResponse = usertable.put_item(
    Item={
      'userId' : items[0]['userId'],
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
      'mechanicId' : items[0]['mechanicId'],
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

  try:
    officeId = str(uuid.uuid4())

    # initのみ以下の配置となる
    userId = event['Keys']['adminIdList']
    mechanicId = event['Keys']['employeeList']


    # 企業情報を登録
    officeResponse = office_post(userId, mechanicId, officeId, event)
    print(officeResponse)

    if officeResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
      print(officeResponse)
      return officeResponse['ResponseMetadata']['HTTPStatusCode']
    else:
      print('PUT Successed.office')

    # メカニック情報を登録
    mechanicResponse = mechanic_post(mechanicId, officeId, event)
    if mechanicResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
      print(mechanicResponse)
      return mechanicResponse['ResponseMetadata']['HTTPStatusCode']
    else:
      print('PUT Successed.mechanic')

    # メカニック、工場の登録情報をユーザーテーブルに登録
    userResponse = user_post(userId, officeId, event)
    if userResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
      print(userResponse)
      return userResponse['ResponseMetadata']['HTTPStatusCode']
    else:
      print('PUT Successed.user')
        
    return officeResponse['ResponseMetadata']['HTTPStatusCode']

  except Exception as e:
      print("Error Exception.")
      print(e)