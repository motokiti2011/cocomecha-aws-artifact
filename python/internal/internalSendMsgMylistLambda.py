import json
import boto3

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

  try:
    # ユーザーリストの件数分引数で指定されたマイリストMsgに登録する
    for user in userList :
      sendMsg_query(event, user)
  except Exception as e:
      print("Error Exception.")
      print(e)

# ユーザーマイリストTBLメッセージ登録
def sendMsg_query(event, userInfo):

  now = datetime.now()
  slipInfo = event['slipInfo']
  category = event['category']
  message = event['message']
  requestInfo = event['requestInfo']

  mechenicId = userInfo['mechenicId']
  if mechenicId == None :
    mechenicId = '0'

  officeId = userInfo['officeId']
  if officeId == None :
    officeId = '0'

  putResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : userInfo['userId'],
      'mechanicId' : mechenicId,
      'officeId' : officeId,
      'serviceType' : slipInfo['serviceType'],
      'slipNo' : slipInfo['slipNo'],
      'serviceTitle' : slipInfo['serviceTitle'],
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



