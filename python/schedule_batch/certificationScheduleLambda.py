import json
import boto3

from datetime import datetime, timedelta


from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
certificationManagementInfo = dynamodb.Table("certificationManagementInfo")

# 認証状況切れチェックLambda
def lambda_handler(event, context):
  print(event)
  print('CHACKCERTIFICATIONLAMBDA')

  try:
    # 認証情報管理検索
    certificationData = operation_query()
    if len(certificationData) > 0 :
      for data in certificationData :
        # 認証期限切れデータを削除する
        delete_certificationData(data)

    print('CHACKCERTIFICATIONLAMBDA-DELETE-DATA:' + len(certificationData))

  except Exception as e:
      print("CHACKCERTIFICATIONLAMBDA-Error Exception.")
      print(e)



# 認証状況レコード検索
def operation_query():

    TIMESTAMP = datetime.now()
    print('TIMESTAMP')
    print(TIMESTAMP)
    
    queryData = certificationManagementInfo.query(
        IndexName = 'operationDateTime-index',
        # 現在時刻より以前のデータを抽出
        KeyConditionExpression = Key("operationDate").eq(TIMESTAMP.strftime('%Y%m%d'))
        & Key("operationTime").lt(TIMESTAMP.strftime('%H%M'))
    )
    items=queryData['Items']
    print(items)
    return items



# 期限切れ認証状況削除
def delete_certificationData(data):

    delResponse = certificationManagementInfo.delete_item(
       Key={
           'userId': data['userId'],
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('DEL Error:' + data['userId'])
    return

