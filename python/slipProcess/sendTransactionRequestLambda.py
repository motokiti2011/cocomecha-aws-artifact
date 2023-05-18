import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
serviceTransactionRequest = dynamodb.Table("serviceTransactionRequest")
userMyList = dynamodb.Table("userMyList")
slipDetailInfo = dynamodb.Table("slipDetailInfo")
salesServiceInfo = dynamodb.Table("salesServiceInfo")

# 取引依頼TBLレコード登録
def post_product(PartitionKey, event, adminUser, adminMecha, adminOffice, serviceTitle):

  now = datetime.now()

  putResponse = serviceTransactionRequest.put_item(
    Item={
      'id' : PartitionKey,
      'slipNo' : event['Keys']['slipNo'],
      'requestId' : event['Keys']['requestId'],
      'requestUserName' : event['Keys']['requestUserName'],
      'serviceUserType' : event['Keys']['serviceUserType'],
      'requestType' : event['Keys']['requestType'],
      'files' : event['Keys']['files'],
      'requestStatus' : event['Keys']['requestStatus'],
      'confirmDiv' : event['Keys']['confirmDiv'],
      'deadline' : event['Keys']['deadline'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.')




  # マイリストTBLの登録
  # 伝票管理者
  userMyListAdminResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' :adminUser,
      'mechanicId' :adminMecha,
      'officeId' : adminOffice,
      'serviceType' : event['Keys']['serviceUserType'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : serviceTitle,
      'category' : '7',
      'message' : 'TRAN_RES',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : None,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')

    }
  )
  
  if userMyListAdminResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListAdminResponse)
  else:
    print('Post Successed.')


  # 取引依頼者
  userMyListResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' :adminUser,
      'mechanicId' :adminMecha,
      'officeId' : adminOffice,
      'serviceType' : event['Keys']['serviceUserType'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' :serviceTitle,
      'category' : '13',
      'message' : 'TRAN_REQ',
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
    print('Post Successed.')
	return


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']
  key = event['Keys']['slipNo']
  serviceKey = event['Keys']['serviceUserType']

  try:
    if OperationType == 'TRANSACTIONREQUEST':
      if serviceKey == '0':
        slip = getSlipDitail(key)
        adminUser = slip[0]['slipAdminUserId']
        adminMecha = '0'
        adminOffice = '0'
        serviceTitle = slip[0]['title']
      else:
        service = getSalesServiceInfo(key)
        adminUser = service[0]['slipAdminUserId']
        adminMecha = service[0]['slipAdminMechanicId']
        adminOffice = service[0]['slipAdminOfficeId']
        serviceTitle = service[0]['title']

      id = str(uuid.uuid4())
      PartitionKey = id
      return post_product(PartitionKey, event, adminUser, adminMecha, adminOffice, serviceTitle)


  except Exception as e:
      print("Error Exception.")
      print(e)