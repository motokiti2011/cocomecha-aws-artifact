import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
userInfo = dynamodb.Table("userInfo")


# ユーザー情報検索 userInfo
def userInfo_query(id) :
    queryData = userInfo.query(
        KeyConditionExpression = Key("userId").eq(id) & Key("userValidDiv").eq("0")
    )
    items=queryData['Items']
    print(items)
    return items[0]


def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    id = event['Keys']['id']

    try:
        # 検索タイプ検証
        if IndexType != 'SLIPADMININFO':
          return

        # データ取得
        items = userInfo_query(id)
        
        resultItems = []
        
        # 結果の格納
        result={
          'adminId' :items['userId'],
          'adminName' :items['userName'],
          'mail' :None,
          'telNo':None,
          'post' :None,
          'adless' :items['areaNo1'],
          'introduction' :items['introduction'],
          'affiliationOfficeId' :None,
          'affiliationOfficeName' :None,
          'qualification' :None,
          'specialtyWork' :None,
          'workContentList' :None,
          'businessHours' :None,
          'baseInfoList' :None,
          'evaluationInfo' :None,
          'profileImageUrl' :items['profileImageUrl']
        }

        return result


    except Exception as e:
        print("Error Exception.")
        print(e)