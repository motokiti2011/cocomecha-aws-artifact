
import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# ì`ï[ìoò^èââÒ

# Dynamodb
dynamodb = boto3.resource('dynamodb')

table1 = dynamodb.Table("slipDetailInfo")
table2 = dynamodb.Table("slipMegPrmUser")



def post_product(PartitionKey, event):
  # slipDetailInfoÇÃPOST
  slipDetailInfoPutResponse = table1.put_item(
    Item={
      'slipNo' : PartitionKey,
      'deleteDiv' : event['Keys']['deleteDiv'],
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
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
    }
  )
  
  if slipDetailInfoPutResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(slipDetailInfoPutResponse)
  else:
    print('slipDetailInfo : Post Successed.')

  
  slipMegPrmUserPutResponse = table2.put_item(
    Item={
      'slipNo' : PartitionKey,
      'slipAdminUserId' : event['Keys']['slipAdminUserId'],
      'slipAdminUserName' : "",
      'permissionUserList' : [],
      'created' : event['Keys']['created'],
      'updated' : event['Keys']['updated']
    }
  )

  if slipMegPrmUserPutResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(slipMegPrmUserPutResponse)
  else:
    print('slipMegPrmUser : Post Successed.')
    return slipMegPrmUserPutResponse['ResponseMetadata']['HTTPStatusCode']



def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  OperationType = event['OperationType']

  try:

    if OperationType == 'INITSLIPPOST':
      PartitionKey = event['Keys']['slipNo'] + str(now)
      return post_product(PartitionKey, event)

  except Exception as e:
      print("Error Exception.")
      print(e)