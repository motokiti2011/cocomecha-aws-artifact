import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
factoryMechaInicItem = dynamodb.Table("factoryMechaInicItem")


# 工場メカニック商品の編集を行う
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    processDiv = event['processDiv']

    serviceId = event['serviceId']
    serviceType = event['serviceType']
    status = event['status']

    try:
        # 処理区分が0の場合閲覧履歴情報を操作
        if processDiv == '0':
          editBrowsing_query(event)
        # 処理区分が1の場合お気に入り情報を操作
        elif processDiv == '1':
          editFavorite_query(event)
        # それ以外場合ステータスを操作
        else:
          editStatus_query(event)
    except Exception as e:
        print("Error Exception.")
        print(e)



# 工場メカニック情報取得
def fcmcItem_query(partitionKey,sortKey ) :
    queryData = factoryMechaInicItem.query(
        KeyConditionExpression = Key("serviceId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 工場メカニック情報更新
def put_fcmcItem(PartitionKey, event):
  putResponse = factoryMechaInicItem.put_item(
    Item={
      'serviceId' : PartitionKey,
      'serviceName' : event['Keys']['serviceName'],
      'factoryMechanicId' : event['Keys']['factoryMechanicId'],
      'serviceType' : event['Keys']['serviceType'],
      'transactionStatus' : event['Keys']['transactionStatus'],
      'browsingCount' : event['Keys']['browsingCount'],
      'favoriteCount' : event['Keys']['favoriteCount']
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['ResponseMetadata']['HTTPStatusCode']



# 閲覧履歴数の更新
def editBrowsing_query(event) :
    serviceId = event['serviceId']
    serviceType = event['serviceType']
    status = event['status']

    更新情報の取得
    fcmcItem = fcmcItem_query(serviceId, serviceType)
    if len(fcmcItem) === 0:
      print('閲覧履歴なし処理終了'+ json.dumps(event))
      return
    putItem = fcmcItem[0]
    # 加減を判定
    if status === '0' :
      # 加算
      putItem['browsingCount']+=1
    else:
      # 減算（多分ないが…）
      putItem['browsingCount']-=1
    # 編集情報を更新
    put_fcmcItem(putItem):


# お気に入り数の更新
def editFavorite_query(event) :
    serviceId = event['serviceId']
    serviceType = event['serviceType']
    status = event['status']

    更新情報の取得
    fcmcItem = fcmcItem_query(serviceId, serviceType)
    if len(fcmcItem) === 0:
      print('お気に入り更新情報なし処理終了'+ json.dumps(event))
      return
    putItem = fcmcItem[0]
    # 加減を判定
    if status === '0' :
      # 加算
      putItem['favoriteCount']+=1
    else:
      # 減算
      putItem['favoriteCount']-=1
    # 編集情報を更新
    put_fcmcItem(putItem):

# ステータスの更新
def editStatus_query(event) :
    serviceId = event['serviceId']
    serviceType = event['serviceType']
    status = event['status']

    更新情報の取得
    fcmcItem = fcmcItem_query(serviceId, serviceType)
    if len(fcmcItem) === 0:
      print('ステータス更新情報なし処理終了' + json.dumps(event))
      return
    putItem = fcmcItem[0]
    # ステータスを更新
    putItem['transactionStatus'] = status
    # 編集情報を更新
    put_fcmcItem(putItem):


