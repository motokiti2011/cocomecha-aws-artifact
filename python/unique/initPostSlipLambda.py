import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# 伝票登録初回

# Dynamodb
dynamodb = boto3.resource('dynamodb')

slipDetailInfo = dynamodb.Table("slipDetailInfo")
slipMegPrmUser = dynamodb.Table("slipMegPrmUser")
transactionSlip = dynamodb.Table("transactionSlip")
userMyList = dynamodb.Table("userMyList")


# 伝票情報初期登録Lambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  OperationType = event['OperationType']

  try:
    if OperationType == 'INITSLIPPOST':
      id = str(uuid.uuid4())
      PartitionKey = id
      return post_product(PartitionKey, event)

    else :
      # アクセス方法がおかしい場合
      print('initPostSlipLambda_Injustice')
      print(str(now))


  except Exception as e:
      print("Error Exception.")
      print(e)

# 伝票情報の登録
def post_product(PartitionKey, event):

  now = datetime.now()

  # slipDetailInfoのPOST
  slipDetailInfoPutResponse = slipDetailInfo.put_item(
    Item={
      'slipNo' : PartitionKey,
      'deleteDiv' : '0',
      'category' : event['Keys']['category'],
      'slipAdminUserId' : event['Keys']['slipAdminUserId'],
      'adminDiv' : event['Keys']['adminDiv'],
      'title' : event['Keys']['title'],
      'areaNo1' : event['Keys']['areaNo1'],
      'areaNo2' : event['Keys']['areaNo2'],
      'price' : event['Keys']['price'],
      'bidMethod' : event['Keys']['bidMethod'],
      'bidderId' : event['Keys']['bidderId'],
      'bidEndDate' : event['Keys']['bidEndDate'],
      'explanation' : event['Keys']['explanation'],
      'displayDiv' : event['Keys']['displayDiv'],
      'processStatus' : '1',
      'targetService' : event['Keys']['targetService'],
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
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if slipDetailInfoPutResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(slipDetailInfoPutResponse)
  else:
    print('slipDetailInfo : Post Successed.')


  # 伝票メッセージ管理ユーザの登録
  slipMegPrmUserPutResponse = slipMegPrmUser.put_item(
    Item={
      'slipNo' : PartitionKey,
      'slipAdminUserId' : event['Keys']['slipAdminUserId'],
      'slipAdminUserName' : "",
      'permissionUserList' : [],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
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
      'mechanicId' : '0',
      'officeId' : '0',
      'slipNo' : PartitionKey,
      'serviceTitle' : event['Keys']['title'],
      'slipRelation' : '0',
      'slipAdminId' : event['Keys']['slipAdminUserId'],
      'slipAdminName' : event['Keys']['slipAdminUserName'],
      'bidderId' : event['Keys']['bidderId'],
      'deleteDiv' : '0',
      'completionScheduledDate': event['Keys']['completionDate'] ,
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if transactionSlipResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(transactionSlipResponse)
  else:
    print('transactionSlip : Post Successed.')


  # マイリストTBLの登録
  userMyListResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : event['Keys']['slipAdminUserId'],
      'mechanicId': '0',
      'officeId' : '0',
      'serviceType' : '0',
      'slipNo' :PartitionKey,
      'serviceTitle' : event['Keys']['title'],
      'category' : '9',
      'message' : 'EXHIBITING',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')

    }
  )
  
  if userMyListResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListResponse)
  else:
    print('userMyList : Post Successed.')
  return userMyListResponse['ResponseMetadata']['HTTPStatusCode']


