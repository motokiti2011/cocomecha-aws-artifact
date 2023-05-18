import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
userInfo = dynamodb.Table("userInfo")
mechanicInfo = dynamodb.Table("mechanicInfo")
officeInfo = dynamodb.Table("officeInfo")

def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    adminId = event['adminId']
    serviceType = event['serviceType']
    accessUser = event['accessUser']

    try:

        adminInfo = ''
        # サービスタイプがユーザーの場合
        if serviceType == '0':
          adminInfo = userInfo_query(adminId)
        # サービスタイプがメカニックの場合
        elif serviceType == '1':
          adminInfo = mechanicInfo_query(adminId)
        # サービスタイプが工場の場合
        else:
          adminInfo = officeInfo_query(adminId)

        # アクセスユーザー情報取得
        accessUserInfo = []
        # ユーザーまたはメカニックの場合ユーザー情報からID判定する
        if serviceType != '2':
          accessUserInfo = userInfo_query(accessUser)
        else:
          accessUserInfo = officeInfo_query(accessUser)


        # 判定
        # サービスタイプがユーザーの場合
        idList = []
        if serviceType == '0':

          if adminInfo[0]['userId'] == accessUserInfo[0]['userId']:
            return True
          else:
            return False
        # サービスタイプがメカニックの場合
        elif serviceType == '1':
          if adminInfo[0]['mechanicId'] == accessUserInfo[0]['mechanicId']:
            return True
          else:
            return False
        # サービスタイプが工場の場合
        else:
          checkList = accessUserInfo[0]['adminIdList']
          
          return adminInfo[0]['officeId'] in checkList

    except Exception as e:
        print("Error Exception.")
        print(e)



# ユーザー情報検索
def userInfo_query(id) :
    queryData = userInfo.query(
        KeyConditionExpression = Key("userId").eq(id) & Key("userValidDiv").eq("0")
    )
    items=queryData['Items']
    print(items)
    return items

# メカニック情報検索
def mechanicInfo_query(id) :
    queryData = mechanicInfo.query(
        KeyConditionExpression = Key("mechanicId").eq(id)
    )
    items=queryData['Items']
    print(items)
    return items

# 工場情報検索
def officeInfo_query(id) :
    queryData = officeInfo.query(
        KeyConditionExpression = Key("officeId").eq(id)
    )
    items=queryData['Items']
    print(items)
    return items



