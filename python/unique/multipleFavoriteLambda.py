import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("userFavorite")

# お気に入り情報複数削除
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:
        # 検索タイプ検証
        if IndexType != 'MULTIPLEDELETEFAVORITE':
          return

        # データ取得
        queryItems =event['Keys']['idList']
        
        if len(queryItems) == 0 :
          return []
        
        # ID数分削除
        for item in queryItems :
          # 削除
          response = operation_delete(item['id']) :
          if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            # 異常終了として返却
            return response
          # 工場メカニック商品情報のお気に入り数を更新
          # 引数
          input_event = {
              "processDiv": '1',
              "serviceId": item['id'],
              "serviceType": item['serviceType'],
              "status": '1'
          }
          Payload = json.dumps(input_event) # jsonシリアライズ
          # 呼び出し
          boto3.client('lambda').invoke(
              FunctionName='internalFcMcItemLambda',
              InvocationType='Event',
              Payload=Payload
          )

       # 全件削除後正常ステータス返却
       return 200

    except Exception as e:
        print("Error Exception.")
        print(e)

# レコード削除
def operation_delete(partitionKey):
    delResponse = table.delete_item(
       key={
           'id': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponsee['ResponseMetadata']['HTTPStatusCode'])
    else:
        print('DEL Successed.')
    return delResponsee




