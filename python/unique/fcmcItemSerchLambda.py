import json
import boto3

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
mechanicInfo = dynamodb.Table("mechanicInfo")
officeInfo = dynamodb.Table("officeInfo")
factoryMechaInicItem = dynamodb.Table("factoryMechaInicItem")

# 工場メカニック取引商品取得
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:
        # インデックス確認
        if IndexType != 'FCMCITEM':
          return []

        # アクセスしたメカニックIDを取得
        mechanicId =event['Keys']['acceseMechanicId']
        # メカニック情報を取得
        mcInfo = getMechanicInfo(mechanicId) :
        # メカニック情報が取得できなかった場合処理終了
        if len(mcInfo) == 0 :
          return []
        
        resultList = []

        # メカニックIDが管理者の工場メカニックアイテム情報を取得
        resultList += fcMcItem_query(mechanicId) :
        
        # 工場IDを取得
        officeId = mcInfo[0]['officeId']
        if not officeId || officeId == '0' :
            return resultList 
        
        # 工場情報を取得
        fcInfo = getFactorycInfo(officeId) :
        
        # 工場情報が取得できなかった場合処理終了
        if len(fcInfo) == 0 :
          return resultList
        # 工場関連者情報を取得
        connectionMcList = fcInfo[0]['connectionMechanicInfo']

        connectionDiv = False
        # 関連者チェック
        for mc in connectionMcList :
          # 関連者になるかをチェック
          if mc === mechanicId :
              connectionDiv = True

        if connectionDiv :
            # 工場IDで工場メカニックアイテム情報を取得
            resultList += fcMcItem_query(officeId) :

       return resultList

    except Exception as e:
        print("Error Exception.")
        print(e)


# メカニック情報を取得
def getMechanicInfo(mechanicId):
    queryData = mechanicInfo.query(
        KeyConditionExpression = Key("mechanicId").eq(mechanicId)
    )
    items=queryData['Items']
    print(items)
    return items

# メカニック情報に紐づく工場メカニックアイテム情報を取得
def fcMcItem_query(partitionKey):
    queryData = factoryMechaInicItem.query(
        IndexName = 'factoryMechanicId-index',
        KeyConditionExpression = Key("factoryMechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 工場情報を取得
def getFactorycInfo(officeId):
    queryData = officeInfo.query(
        KeyConditionExpression = Key("officeId").eq(officeId)
    )
    items=queryData['Items']
    print(items)
    return items

# 伝票情報を返却情報に加工する
def editItems(service):
    if len(service) == 0 :
        return []
    
    result = []
    for se in service :
    Item={
      'serviceId' : PartitionKey,
      'serviceName' : event['Keys']['officeName'],
      'serviceType' : event['Keys']['officeTel'],
      'transactionStatus' : event['Keys']['officeMailAdress'],
      'browsingCount' : '0',
      'favoriteCount' : '0'
    }

    queryData = table.query(
        IndexName = 'slipAdminOfficeId-index',
        KeyConditionExpression = Key("slipAdminOfficeId").eq(officeId) & Key("deleteDiv").eq('1')
    )
    items=queryData['Items']
    print(items)
    return items