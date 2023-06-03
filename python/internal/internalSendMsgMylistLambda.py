import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
userMyList = dynamodb.Table("userMyList")


# 内部処理 引数に指定されたメッセージをマイリストTBLに登録する
def lambda_handler(event, context) :
  print("Received event: " + json.dumps(event))

  userList = event['userList']

  print(userList)

  try:
    # ユーザーリストの件数分引数で指定されたマイリストMsgに登録する
    for user in userList :
      res = sendMsg_query(event, user)
      if res != 200 :
        return 500
      
    # 全件完了した際に200 を返却
    return 200
  except Exception as e:
      print("Error Exception.")
      print(e)

# ユーザーマイリストTBLメッセージ登録
def sendMsg_query(event, userInfo):
  print('LABEL_1')
  now = datetime.now()
  slipInfo = event['slipInfo']
  category = event['category']
  message = event['message']
  requestInfo = event['requestInfo']

  print('LABEL_2')
  print(userInfo)
  mechenicId = userInfo['mechanicId']
  if mechenicId == None :
    mechenicId = '0'

  print('LABEL_3')
  officeId = userInfo['officeId']
  if officeId == None :
    officeId = '0'

  print('LABEL_4')
  putResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : userInfo['userId'],
      'mechanicId' : mechenicId,
      'officeId' : officeId,
      'serviceType' : slipInfo['serviceType'],
      'slipNo' : slipInfo['slipNo'],
      'serviceTitle' : slipInfo['title'],
      'category' : category,
      'message' : message,
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : requestInfo,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse

  print('LABEL_5')
  return putResponse['ResponseMetadata']['HTTPStatusCode']

