import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
mechanicInfo = dynamodb.Table("mechanicInfo")
officeInfo = dynamodb.Table("officeInfo")

# メカニック情報検索 mechanicInfo
def mechanicInfo_query(id) :
    queryData = userInfo.query(
        KeyConditionExpression = Key("mechanicId").eq(id)
    )
    items=queryData['Items']
    print(items)
    return items


# 工場情報検索 officeInfo
def userInfo_query(id) :
    queryData = officeInfo.query(
        KeyConditionExpression = Key("officeId").eq(id)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    id = event['Keys']['id']
    serviceType = event['Keys']['serviceType']

    try:
        # 検索タイプ検証
        if IndexType != 'SALESADMININFO':
          return

        # データ取得
        queryItems = []
        if serviceType == '1'
          items = mechanicInfo_query(id)
          # 結果の格納
          result={
            'adminId' :items[0]['mechanicId'],
            'adminName' :items[0]['mechanicName'],
            'mail' :items[0]['mailAdress'],
            'telNo':items[0]['telList'],
            'post' :items[0]['introduction'],
            'adless' : None,
            'introduction' :items[0]['introduction'],
            'affiliationOfficeId' :items[0]['officeId'],
            'affiliationOfficeName' :items[0]['associationOfficeList'],
            'qualification' :items[0]['qualification'],
            'specialtyWork' :items[0]['specialtyWork'],
            'workContentList' : None,
            'businessHours' : None,
            'baseInfoList' : None,
            'evaluationInfo' : None,
            'profileImageUrl' :items[0]['profileImageUrl']
          }
        else:
          items = officeInfo_query(id)
          # 結果の格納
          result={
            'adminId' :items[0]['officeId'],
            'adminName' :items[0]['officeName'],
            'mail' :items[0]['officeMailAdress'],
            'telNo': items[0]['userName'],
            'post' : items[0]['officePostCode'],
            'adless' : items[0]['officeArea1'],
            'introduction' : items[0]['introduction'],
            'affiliationOfficeId' : None,
            'affiliationOfficeName' : None,
            'qualification' : None,
            'specialtyWork' : None,
            'workContentList' : items[0]['workContentList'],
            'businessHours' : items[0]['businessHours'],
            'baseInfoList' : items[0]['baseInfoList'],
            'evaluationInfo' : None,
            'profileImageUrl' :items['profileImageUrl']
          }
        

        return result


    except Exception as e:
        print("Error Exception.")
        print(e)