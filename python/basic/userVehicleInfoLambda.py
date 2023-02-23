import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("userVehicleInfo")


# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード更新
def put_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'vehicleId' : PartitionKey,
      'userId' : event['Keys']['userId'],
      'vehicleName' : event['Keys']['vehicleName'],
      'vehicleDiv' : event['Keys']['vehicleDiv'],
      'vehicleNo' : event['Keys']['vehicleNo'],
      'vehicleNoAreaName' : event['Keys']['vehicleNoAreaName'],
      'vehicleNoClassificationNum' : event['Keys']['vehicleNoClassificationNum'],
      'vehicleNoKana' : event['Keys']['vehicleNoKana'],
      'vehicleNoSerialNum' : event['Keys']['vehicleNoSerialNum'],
      'chassisNo' : event['Keys']['chassisNo'],
      'designatedClassification' : event['Keys']['designatedClassification'],
      'maker' : event['Keys']['maker'],
      'form' : event['Keys']['form'],
      'coler' : event['Keys']['coler'],
      'colerNo' : event['Keys']['colerNo'],
      'mileage' : event['Keys']['mileage'],
      'firstRegistrationDate' : event['Keys']['firstRegistrationDate'],
      'InspectionExpirationDate' : event['Keys']['InspectionExpirationDate'],
      'updateUserId' : event['Keys']['updateUserId'],
      'created' : event['Keys']['created'],
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['ResponseMetadata']['HTTPStatusCode']


# レコード追加
def post_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'vehicleId' : PartitionKey,
      'userId' : event['Keys']['userId'],
      'vehicleName' : event['Keys']['vehicleName'],
      'vehicleNo' : event['Keys']['vehicleNo'],
      'vehicleNoAreaName' : event['Keys']['vehicleNoAreaName'],
      'vehicleNoClassificationNum' : event['Keys']['vehicleNoClassificationNum'],
      'vehicleNoKana' : event['Keys']['vehicleNoKana'],
      'vehicleNoSerialNum' : event['Keys']['vehicleNoSerialNum'],
      'chassisNo' : event['Keys']['chassisNo'],
      'designatedClassification' : event['Keys']['designatedClassification'],
      'maker' : event['Keys']['maker'],
      'form' : event['Keys']['form'],
      'coler' : event['Keys']['coler'],
      'colerNo' : event['Keys']['colerNo'],
      'mileage' : event['Keys']['mileage'],
      'firstRegistrationDate' : event['Keys']['firstRegistrationDate'],
      'InspectionExpirationDate' : event['Keys']['InspectionExpirationDate'],
      'updateUserId' : event['Keys']['updateUserId'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['ResponseMetadata']['HTTPStatusCode']



# レコード削除
def operation_delete(partitionKey):
    delResponse = table.delete_item(
       Key={
           'userId': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['vehicleId']
      return operation_query(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['vehicleId']
      return put_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      return operation_delete(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = id
      return post_product(PartitionKey, event)


  except Exception as e:
      print("Error Exception.")
      print(e)