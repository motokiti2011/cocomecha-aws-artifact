import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table("slipDetailInfo")
userInfo = dynamodb.Table("userInfo")

def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey) & Key("deleteDiv").eq("0")
    )
    items=queryData['Items']
    print(items)
    
    userData = userInfo.query(
        KeyConditionExpression = Key("userId").eq(items[0]['slipAdminUserId']) & Key("userValidDiv").eq("0")
    )
    user=userData['Items']
    print(user)

    result={
      'slipNo' :items[0]['slipNo'],
      'deleteDiv' :items[0]['deleteDiv'],
      'category' :items[0]['category'],
      'slipAdminUserId' :items[0]['slipAdminUserId'],
      'slipAdminUserName' :user[0]['userName'],
      'adminDiv' :items[0]['adminDiv'],
      'title' :items[0]['title'],
      'areaNo1' :items[0]['areaNo1'],
      'areaNo2' :items[0]['areaNo2'],
      'price' :items[0]['price'],
      'bidMethod' :items[0]['bidMethod'],
      'bidderId' :items[0]['bidderId'],
      'bidEndDate' :items[0]['bidEndDate'],
      'explanation' :items[0]['explanation'],
      'displayDiv' :items[0]['displayDiv'],
      'processStatus' :items[0]['processStatus'],
      'targetService' :items[0]['targetService'],
      'targetVehicleId' :items[0]['targetVehicleId'],
      'targetVehicleDiv' :items[0]['targetVehicleDiv'],
      'targetVehicleName' :items[0]['targetVehicleName'],
      'targetVehicleInfo' :items[0]['targetVehicleInfo'],
      'workAreaInfo' :items[0]['workAreaInfo'],
      'preferredDate' :items[0]['preferredDate'],
      'preferredTime' :items[0]['preferredTime'],
      'completionDate' :items[0]['completionDate'],
      'transactionCompletionDate' :items[0]['transactionCompletionDate'],
      'thumbnailUrl' :items[0]['thumbnailUrl'],
      'imageUrlList' :items[0]['imageUrlList'],
      'messageOpenLebel' :items[0]['messageOpenLebel'],
      'updateUserId' :items[0]['updateUserId'],
      'created' :items[0]['created'],
      'updated' :items[0]['updated']
    }

    print(result)
    return result

def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  OperationType = event['OperationType']

  try:
    if OperationType == 'GETSLIP':
      PartitionKey = event['Keys']['slipNo']
      return operation_query(PartitionKey)


  except Exception as e:
      print("Error Exception.")
      print(e)