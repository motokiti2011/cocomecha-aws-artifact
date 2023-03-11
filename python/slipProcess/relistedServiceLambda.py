import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
slipDetailInfo = dynamodb.Table("slipDetailInfo")
salesServiceInfo = dynamodb.Table("salesServiceInfo")
userMyList = dynamodb.Table("userMyList")




# 伝票情報レコード更新
def put_slip(event):
  putResponse = slipDetailInfo.put_item(
    Item={
      'slipNo' : event['Keys']['slipNo'],
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
      'processStatus' :'0',
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
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('put_slip : Post Successed.')
  return putResponse['Item']



# サービス商品レコード更新
def put_serviceContents(PartitionKey, event):
  putResponse = salesServiceInfo.put_item(
    Item={
      'slipNo' : event['Keys']['slipNo'],
      'deleteDiv' : event['Keys']['deleteDiv'],
      'category' : event['Keys']['category'],
      'slipAdminUserId' : event['Keys']['slipAdminUserId'],
      'slipAdminOfficeId' : event['Keys']['slipAdminOfficeId'],
      'slipAdminMechanicId' : event['Keys']['slipAdminMechanicId'],
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
      'processStatus' : '0',
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
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('put_serviceContents : Post Successed.')
  return putResponse['Item']



# 伝票管理者マイリストの更新
def put_slipMyList(event):
  # マイリストTBLの登録
  # 伝票管理者
  userMyListAdminResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : event['Keys']['slipAdminUserId'],
      'mechanicId '0',
      'officeId' : '0',
      'serviceType' : event['Keys']['serviceType'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : event['Keys']['title'],
      'category' : '22',
      'message' : 'RELISTED_SERVICE',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')

    }
  )
  
  if userMyListAdminResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListAdminResponse)
  else:
    print('Post Successed.')



# マイリスト更新（再出品：伝票）
def put_serviceContentsMyList(event):
  userMyListResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : event['Keys']['slipAdminUserId'],
      'mechanicId : event['Keys']['slipAdminMechanicId'],
      'officeId' : event['Keys']['slipAdminOfficeId'],
      'serviceType' : event['Keys']['serviceType'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : event['Keys']['title'],
      'category' : '22',
      'message' : 'RELISTED_SERVICE',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')

    }
  )
  
  if userMyListResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListResponse)
  else:
    print('Post Successed.')
	return


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:
    if OperationType == 'RELISTEDSERVICE':

      serviceType = event['Keys']['serviceType']

      if serviceType == '0':
        # 伝票情報を更新
        response = put_slip(event)
        # マイリストにメッセージ追加
        put_slipMyList(event)
        return response
        
      else :
        # サービスコンテンツ更新
        response = put_serviceContents(event)
        # マイリストにメッセージ追加
        put_serviceContentsMyList(event)
        return response

  except Exception as e:
      print("Error Exception.")
      print(e)