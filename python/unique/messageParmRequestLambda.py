import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("slipMegPrmUser")


# レコード検索
def post_product(partitionKey, updateId, updateName):
    # 対象レコード取得
    queryData = table.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']

    if len(items) == 0:
      # 取得できなかった場合
      return False

    item = items[0]

    # 許可済ユーザーリストを取得
    userList = item['permissionUserList']
    data = {'userId':updateId ,'userName':updateName, 'parmissionDiv': '0'}
    # 許可済ユーザーリストが空の場合
    if len(userList) == 0:
      userList.append(data)
     
    else:
      inListDiv = True
      count = 0
      target = 0
      for list in userList:
        if(list['userId'] == updateId):
          # リストにすでに含まれる場合,申請取り消しとして削除
          inListDiv = False
          target = count
        count += 1
            

      if(inListDiv):
        userList.append(data)
      else:
        userList.pop(target)
        

    # レコード更新
    putResponse = table.put_item(
      Item={
        'slipNo' : PartitionKey,
        'slipAdminUserId' : item['slipAdminUserId'],
        'slipAdminUserName' : item['slipAdminUserName'],
        'permissionUserList' : userList,
        'created' : item['created'],
        'updated' : datetime.now()
      }
    )
  
    if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
      print(putResponse)
    else:
      print('Post Successed.')
    return putResponse
  


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:

    if OperationType == 'MESSAGEREQ':
      PartitionKey = event['Keys']['slipNo']
      updateId = event['Keys']['userId']
      updateName = event['Keys']['userName']
      return post_product(PartitionKey, updateId, updateName)


  except Exception as e:
      print("Error Exception.")
      print(e)