import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# ì`ï[ìoò^èââÒ

# Dynamodb
dynamodb = boto3.resource('dynamodb')

table1 = dynamodb.Table("slipDetailInfo")
table2 = dynamodb.Table("slipMegPrmUser")
table3 = dynamodb.Table("transactionSlip")
table4 = dynamodb.Table("userMyList")


def post_product(PartitionKey, event):

  now = datetime.now()

  # slipDetailInfoÇÃPOST
  slipDetailInfoPutResponse = table1.put_item(
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
      'processStatus' : event['Keys']['processStatus'],
      'targetService' : event['Keys']['targetService'],
      'targetVehicleId' : event['Keys']['targetVehicleId'],
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


  # ì`ï[ÉÅÉbÉZÅ[ÉWä«óùÉÜÅ[ÉUÇÃìoò^
  slipMegPrmUserPutResponse = table2.put_item(
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


  # éÊà¯ì`ï[èÓïÒÇÃìoò^
  transactionSlipResponse = table3.put_item(
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
      'completionScheduledDate': '' ,
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if transactionSlipResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(transactionSlipResponse)
  else:
    print('transactionSlip : Post Successed.')


  # É}ÉCÉäÉXÉgTBLÇÃìoò^
  userMyListResponse = table4.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : event['Keys']['slipAdminUserId'],
      'mechanicId': '0',
      'officeId' : '0',
      'serviceType' : '0',
      'slipNo' :PartitionKey,
      'serviceTitle' : event['Keys']['title'],
      'category' : '1',
      'message' : '',
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
    print('userMyList : Post Successed.')
  return userMyListResponse['ResponseMetadata']['HTTPStatusCode']


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
      # ÉAÉNÉZÉXï˚ñ@Ç™Ç®Ç©ÇµÇ¢èÍçá
      print('initPostSlipLambda_Injustice')
      print(str(now))


  except Exception as e:
      print("Error Exception.")
      print(e)