import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# サービス商品初回

# Dynamodb
dynamodb = boto3.resource('dynamodb')

salesServiceInfo = dynamodb.Table("salesServiceInfo")
slipMegPrmUser = dynamodb.Table("slipMegPrmUser")
transactionSlip = dynamodb.Table("transactionSlip")
userMyList = dynamodb.Table("userMyList")
officeInfo = dynamodb.Table("officeInfo")
mechanicInfo = dynamodb.Table("mechanicInfo")
factoryMechaInicItem = dynamodb.Table("factoryMechaInicItem")

# サービス商品初回登録Lambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  OperationType = event['OperationType']
  try:
    if OperationType == 'INITSALESSERVICEPOST':
      id = str(uuid.uuid4())
      PartitionKey = id
      return post_product(PartitionKey, event)

    else :
      print('INITSALESSERVICEPOST_Injustice')

  except Exception as e:
      print("Error Exception.")
      print(e)


# salesServiceのPOST
def post_product(PartitionKey, event):
  
  
  mechanicId = event['Keys']['slipAdminMechanicId']
  officeId = event['Keys']['slipAdminOfficeId']
  
  if not mechanicId:
    mechanicId = '0'
    mechanicName = ''
  else:
    queryData = mechanicInfo.query(
        KeyConditionExpression = Key("mechanicId").eq(event['Keys']['slipAdminMechanicId'])
    )
    mechanic = queryData['Items']
    mechanicName = mechanic[0]['mechanicName']

  if not officeId:
    officeId = '0'
    officeName = ''
  else:
    queryData = officeInfo.query(
        KeyConditionExpression = Key("officeId").eq(event['Keys']['slipAdminOfficeId'])
    )
    office = queryData['Items']
    officeName = office[0]['officeName']

  print(event['Keys']['slipAdminMechanicId'])
  print(mechanicName)
  print(officeName)
  print(event['Keys']['slipAdminOfficeId'])


  putResponse = salesServiceInfo.put_item(
    Item={
      'slipNo' : PartitionKey,
      'deleteDiv' : event['Keys']['deleteDiv'],
      'category' : event['Keys']['category'],
      'slipAdminUserId' : event['Keys']['slipAdminUserId'],
      'slipAdminUserName' : event['Keys']['slipAdminUserName'],
      'slipAdminOfficeId' : officeId,
      'slipAdminOfficeName' : officeName,
      'slipAdminMechanicId' : mechanicId,
      'slipAdminMechanicName' : mechanicName,
      'adminDiv' : event['Keys']['adminDiv'],
      'title' : event['Keys']['title'],
      'areaNo1' : event['Keys']['areaNo1'],
      'areaNo2' : event['Keys']['areaNo2'],
      'price' : event['Keys']['price'],
      'bidMethod' : event['Keys']['bidMethod'],
      'bidUserType':  '0',
      'bidderId' : '0',
      'bidEndDate' : event['Keys']['bidEndDate'],
      'explanation' : event['Keys']['explanation'],
      'displayDiv' : event['Keys']['displayDiv'],
      'processStatus' : '0',
      'serviceType' : event['Keys']['serviceType'],
      'targetVehicleId' : event['Keys']['targetVehicleId'],
      'targetVehicleDiv' : event['Keys']['targetVehicleDiv'],
      'targetVehicleName' : event['Keys']['targetVehicleName'],
      'targetVehicleInfo' : event['Keys']['targetVehicleInfo'],
      'workAreaInfo' : event['Keys']['workAreaInfo'],
      'preferredDate' : event['Keys']['preferredDate'],
      'preferredTime' : event['Keys']['preferredTime'],
      'completionDate' : event['Keys']['completionDate'],
      'transactionCompletionDate' : event['Keys']['transactionCompletionDate'],
      'thumbnailUrl' : event['Keys']['thumbnailUrl'],
      'imageUrlList' : event['Keys']['imageUrlList'],
      'messageOpenLebel' : event['Keys']['messageOpenLebel'],
      'updateUserId' : event['Keys']['updateUserId'],
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
    }
  )

  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('salesService : Post Successed.')

  # 伝票メッセージ管理ユーザの登録
  slipMegPrmUserPutResponse = slipMegPrmUser.put_item(
    Item={
      'slipNo' : PartitionKey,
      'slipAdminUserId' : event['Keys']['slipAdminUserId'],
      'slipAdminUserName' : event['Keys']['slipAdminUserName'],
      'permissionUserList' : [],
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
    }
  )

  if slipMegPrmUserPutResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(slipMegPrmUserPutResponse)
  else:
    print('slipMegPrmUser : Post Successed.')
  
  # 取引伝票情報の登録
  transactionSlipResponse = transactionSlip.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'serviceType' : '0',
      'userId' : event['Keys']['slipAdminUserId'],
      'mechanicId' : mechanicId,
      'officeId' : officeId,
      'slipNo' : PartitionKey,
      'serviceTitle' : event['Keys']['title'],
      'slipRelation' : '0',
      'slipAdminId' : event['Keys']['slipAdminUserId'],
      'slipAdminName' : event['Keys']['slipAdminUserName'],
      'bidderId' : event['Keys']['bidderId'],
      'deleteDiv' : '0',
      'completionScheduledDate' : event['Keys']['completionDate'],
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if transactionSlipResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(transactionSlipResponse)
  else:
    print('Post Successed.')


  # マイリストTBLの登録
  userMyListResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : event['Keys']['slipAdminUserId'],
      'mechanicId' : mechanicId,
      'officeId' : officeId,
      'serviceType' : event['Keys']['serviceType'],
      'slipNo' :PartitionKey,
      'serviceTitle' : event['Keys']['title'],
      'category' : '9',
      'message' : 'EXHIBITING',
      'readDiv' : '0',
      'messageDate' : datetime.now().strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')

    }
  )
  
  # 工場メカニックアイテムの登録
  if event['Keys']['serviceType'] == '1':
    fcmcId = officeId
  else :
    fcmcId = mechanicId
  
  putResponse = factoryMechaInicItem.put_item(
    Item={
      'serviceId' : PartitionKey,
      'serviceName' : event['Keys']['title'],
      'factoryMechanicId' : fcmcId,
      'serviceType' : event['Keys']['serviceType'],
      'transactionStatus' : '1',
      'browsingCount' : 0,
      'favoriteCount' : 0
    }
  )
  
  if userMyListResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListResponse)
  else:
    print('Post Successed.')
  return userMyListResponse['ResponseMetadata']['HTTPStatusCode']
