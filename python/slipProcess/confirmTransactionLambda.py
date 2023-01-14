import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("serviceTransactionRequest")
table2 = dynamodb.Table("userMyList")


# 取引依頼TBL
def post_transactionRequest(PartitionKey, event, adminUser, confirmUser):

  # 取引依頼TBL(管理者)
  now = datetime.now()
  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'slipNo' : event['Keys']['slipNo'],
      'requestId' : event['Keys']['requestId'],
      'serviceUserType' : event['Keys']['serviceUserType'],
      'requestType' : event['Keys']['requestType'],
      'files' : event['Keys']['files'],
      'requestStatus' : event['Keys']['requestStatus'],
      'confirmDiv' : '1',
      'deadline' : event['Keys']['deadline'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')


  # 伝票情報に紐づく依頼者情報を取得
  PartitionKey = event['Keys']['slipNo']
  requestUserTransaction = transactionSlipNo_query(PartitionKey)


  for item in requestUserTransaction :
    # 管理ユーザー以外（依頼者）のステータス更新
    if adminUser != item['requestId'] :
      if confirmUser != item['requestId'] :
        postAnConfirmTransactionRequest(item)
      elif confirmUser == item['requestId'] :
        postConfirmTransactionRequest(item)

  return putResponse


# マイリストTBL
def post_myList(PartitionKey, event, adminUser, confirmUser)):
  # マイリストTBLの登録
  # 伝票管理者
  userMyListAdminResponse = table2.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : event['Keys']['slipAdminUserId'],
      'mechanicId : event['Keys']['slipAdminMechanicId'],
      'officeId' : event['Keys']['slipAdminOfficeId'],
      'serviceType' : event['Keys']['targetService'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : event['Keys']['serviceTitle'],
      'category' : '10',
      'message' : '',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')

    }
  )
  
  if userMyListAdminResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListAdminResponse)
  else:
    print('Post Successed.')


  # 取引中のマイリスト情報を取得
  requestMyList = mylist_slipNo_query( event['Keys']['slipNo'])

  for item in requestMyList :
    # 管理ユーザー以外（依頼者）のステータス更新
    if adminUser != item['requestId'] :
      if confirmUser != item['requestId'] :
        postAnConfirmMylistRequest(item)
      elif confirmUser == item['requestId'] :
        postConfirmMylistRequest(item)

  return userMyListAdminResponse


# 伝票番号に紐づく取引依頼TBL情報取得
def transactionSlipNo_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipNo-index',
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# 取引依頼TBL(依頼者(確定以外)データ更新)
def postAnConfirmTransactionRequest(item):

  # 取引依頼TBL(管理者)
  now = datetime.now()
  putResponse = table.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'serviceUserType' : item['serviceUserType'],
      'requestType' : item['requestType'],
      'files' : item['files'],
      'requestStatus' : item['requestStatus'],
      'confirmDiv' : '9',
      'deadline' : item['deadline'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.')


# 取引依頼TBL(依頼者(確定)データ更新)
def postConfirmTransactionRequest(item):

  # 取引依頼TBL(管理者)
  now = datetime.now()
  putResponse = table.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'serviceUserType' : item['serviceUserType'],
      'requestType' : item['requestType'],
      'files' : item['files'],
      'requestStatus' : item['requestStatus'],
      'confirmDiv' : '1',
      'deadline' : item['deadline'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.')


# 伝票番号に紐づくユーザーマイリストTBL情報取得
def mylist_slipNo_query(partitionKey):
    queryData = table2.query(
        IndexName = 'slipNo-index',
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# ユーザーマイリストTBL(依頼者データ更新)
def postAnConfirmMylistRequest(item):

  # 取引依頼TBL(管理者)
  now = datetime.now()
  putResponse = table2.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'serviceUserType' : item['serviceUserType'],
      'requestType' : item['requestType'],
      'files' : item['files'],
      'requestStatus' : '16',
      'confirmDiv' : '0',
      'deadline' : item['deadline'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.')


# ユーザーマイリストTBL(依頼者データ更新)
def postConfirmMylistRequest(item):

  # 取引依頼TBL(管理者)
  now = datetime.now()
  putResponse = table2.put_item(
    Item={
      'id' : item['id'],
      'slipNo' : item['slipNo'],
      'requestId' : item['requestId'],
      'serviceUserType' : item['serviceUserType'],
      'requestType' : item['requestType'],
      'files' : item['files'],
      'requestStatus' : '15',
      'confirmDiv' : '1',
      'deadline' : item['deadline'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.')


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']
  adminUser = event['AdminUser']
  confirmUser = event['confirmUser']
  try:
    if OperationType == 'CONFIRMTRANSACTION':
      id = str(uuid.uuid4())
      PartitionKey = id
      post_transactionRequest(PartitionKey, event, adminUser, confirmUser)
      post_myList(PartitionKey, event, adminUser, confirmUser)

  except Exception as e:
      print("Error Exception.")
      print(e)