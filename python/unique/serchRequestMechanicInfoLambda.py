import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
userMyList = dynamodb.Table("userMyList")

# メカニック申し込み情報の取得Lambda
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    adminOfficeId = event['Keys']['adminOfficeId']

    try:
        # 検索タイプ検証
        if IndexType != 'GETREQUESTMECHANICINFO':
          return

        # データ取得
        items = userMyList_query(adminOfficeId)

        resultItems = []
        # 結果の格納
        for item in items  :

          resultItems.append(item['requestInfo'])

        return resultItems


    except Exception as e:
        print("Error Exception.")
        print(e)


# マイリスト情報検索 
def userMyList_query(adminOfficeId) :

    options = {
      'IndexName' : 'officeId-index',
      'KeyConditionExpression': Key("officeId").eq(adminOfficeId),
      'FilterExpression': Attr('category').contains('22'),
    }
    queryData = officeInfo.query(**options)
    items=queryData['Items']
    print(items)
    return items


