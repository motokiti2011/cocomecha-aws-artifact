import json
import boto3

from boto3.dynamodb.conditions import Key, Attr
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("salesServiceInfo")


# サービス商品情報検索Lambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  IndexType = event['IndexType']
  try:
    print('LABEL_1')
    # インデックスタイプチェック
    if IndexType == 'SERCH-SERVICE-INDEX':
      print('LABEL_2')
      area2 = event['Keys']['area2']
      # 検索値「エリア2のチェック」
      if area2 == 0:
        print('LABEL_3')
        return areaNo1_query(event)
      else:
        print('LABEL_4')
        return areaNo1AndAreaNo2_query(event)
    else:
      print('LABEL_5')
      return 500
  except Exception as e:
    print("Error Exception.")
    print(e)



# 地域1検索 areaNo1-index
def areaNo1_query(event):
    # 検索条件作成
    serchFilter = createFilter(event)
    print('serchFilter')
    print(serchFilter)

    if serchFilter != '' :
      options = {
        'IndexName' : 'areaNo1-index',
        'KeyConditionExpression': Key("areaNo1").eq(event['Keys']['area1']),
        'FilterExpression': serchFilter,
      }
    else :
      options = {
        'IndexName' : 'areaNo1-index',
        'KeyConditionExpression': Key("areaNo1").eq(event['Keys']['area1']),
      }
    
    print('options:')
    print( options)
    queryData = table.query(**options)
    items=queryData['Items']
    print(items)
    return items


# 地域1.2レコード検索 areaNo1AndAreaNo2-index
def areaNo1AndAreaNo2_query(event):

    # 検索条件作成
    serchFilter = createFilter(event)
    print('serchFilter')
    print(serchFilter)
    
    if serchFilter != '' :
      options = {
        'IndexName' : 'areaNo1AndAreaNo2-index',
        'KeyConditionExpression': Key("areaNo1").eq(event['Keys']['area1']) & Key("areaNo2").eq(event['Keys']['area2']),
        'FilterExpression': serchFilter,
      }
    else :
      options = {
        'IndexName' : 'areaNo1AndAreaNo2-index',
        'KeyConditionExpression': Key("areaNo1").eq(event['Keys']['area1']) & Key("areaNo2").eq(event['Keys']['area2']),
      }

    print('options:')
    print( options)
    queryData = table.query(**options)
    items=queryData['Items']
    print(items)
    return items


# 検索条件作成
def createFilter(event):

    # 検索条件作成
    area2 = event['Keys']['area2']
    category = event['Keys']['category']
    amount1 = event['Keys']['amount1']
    amount2 = event['Keys']['amount2']
    amountSerchDiv = event['Keys']['amountSerchDiv']

    if not(category) :
      print('1222')
      category = '0'

    print(category)
    # その他検索条件がなし
    if category == '0' and amountSerchDiv == False :
      print('1')
      return ''
    # カテゴリーのみ
    if category != '0' and amountSerchDiv == False :
      print('2')
      return Attr('category').eq(category)
    # 金額のみ
    if category == '0' and amountSerchDiv == True :
      print('3')
      return Attr('price').between(amount1, amount2)
    # カテゴリー,金額
    if category != '0' and amountSerchDiv == True :
      print('4')
      return Attr('category').eq(category) & Attr('price').between(amount1, amount2)
    # カテゴリー,金額
    print('5')
    return ''

