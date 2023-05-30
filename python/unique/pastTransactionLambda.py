import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("completionSlip")

# 過去取引情報取得
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    id = event['Keys']['adminId']
    serviceType = event['Keys']['serviceType']
    accessUser = event['Keys']['accessUser']


    try:
        # 検索タイプ検証
        if IndexType != 'PASTTRANSACTION':
          return


        #管理者チェック
        # 引数
        input_event = {
            "adminId": id,
            "serviceType": serviceType,
            "accessUser": accessUser
        }
        Payload = json.dumps(input_event) # jsonシリアライズ
        print("---01: Payload:", Payload)
        # 呼び出し
        response = boto3.client('lambda').invoke(
            FunctionName='internalAdminCheckLambda',
            InvocationType='RequestResponse',
            Payload=Payload
        )

        body = json.loads(response['Payload'].read()) #どうやらHTTPヘッダーは特殊な形をしているようで、普通にjson.
        print("---03: body:", body)

        print(id)

        resultItems = []

        # データ取得
        if serviceType == '0':
          resultItems = slipAdminUserId_query(id)
        elif serviceType == '1':
          resultItems = slipAdminMechanicId_query(id)
        else:
          resultItems = slipAdminOffice_query(id)
        
        # 結果の格納
        if body:
          # 管理者の場合全データ返却
          return resultItems
        else :
          # それ以外はデータ編集返却
          return setItems(resultItems)

    except Exception as e:
        print("Error Exception.")
        print(e)



# 1レコード検索 slipAdminUserId-index
def slipAdminUserId_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminUserId-index',
        KeyConditionExpression = Key("slipAdminUserId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 2レコード検索 slipAdminOfficeId-index
def slipAdminOffice_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminOffice-index',
        KeyConditionExpression = Key("slipAdminOfficeId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 3レコード検索 slipAdminMechanicId-index
def slipAdminMechanicId_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminMechanicId-index',
        KeyConditionExpression = Key("slipAdminMechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items# ユーザー情報検索 userInfo


# 管理者用データセット
def setItems(itemList) :

    resultList = []
    for item in itemList :
      # データセット
      resultList.append(dataItem={
        'slipNo' : item[slipNo],
        'slipAdminUserId' : '',
        'slipAdminOfficeId' : '',
        'slipAdminMechanicId' : '',
        'adminDiv' : '',
        'title' : item['title'],
        'price' : item['price'],
        'bidMethod' : item['bidMethod'],
        'bidderId' : '',
        'bidEndDate' : item['bidEndDate'],
        'explanation' : item['explanation'],
        'serviceType' : item['serviceType'],
        'targetVehicleId' : '',
        'targetVehicleName' : item['targetVehicleName'],
        'targetVehicleInfo' : None,
        'workAreaInfo' : None,
        'evaluationId' : item['evaluationId'],
        'completionDate' : item['completionDate'],
        'transactionCompletionDate' : item['transactionCompletionDate'],
        'thumbnailUrl' : item['thumbnailUrl'],
        'imageUrlList' : [],
        'created' : '',
        'updated' : ''
      })

    return resultList