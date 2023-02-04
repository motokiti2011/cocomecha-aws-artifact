import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("slipDetailInfo")

# 地域1検索 areaNo1-index
def areaNo1_query(event):

    # 検索条件作成
    serchFilter = createFilter(event)

    queryData = table.query(
        IndexName = 'areaNo1-index',
        KeyConditionExpression = Key("areaNo1").eq(event['Keys']['areaNo1'])
        FilterExpression: serchFilter,
    )
    items=queryData['Items']
    print(items)
    return items


# 地域1.2レコード検索 areaNo1AndAreaNo2-index
def areaNo1AndAreaNo2_query(event):

    # 検索条件作成
    serchFilter = createFilter(event)

    queryData = table.query(
        IndexName = 'areaNo1AndAreaNo2-index',
        KeyConditionExpression = Key("areaNo2").eq(event['Keys']['areaNo1']) & Key("areaNo2").eq(event['Keys']['areaNo2']),
        FilterExpression: serchFilter,
    )
    items=queryData['Items']
    print(items)
    return items


# 検索条件作成
def createFilter(event):

    # 検索条件作成
    area2 : event['Keys']['areaNo2']
    category : event['Keys']['category']
    amount1 : event['Keys']['amount1']
    amount2 : event['Keys']['amount2']
    amountSerchDiv : event['Keys']['amountSerchDiv']
    
    # その他検索条件がなし
    if area2 == '0' && category == '0' && amountSerchDiv == false :
      return ''

    # 地域2情報のみ
    if area2 != '0' && category == '0' && amountSerchDiv == false :
      return Attr('area2').eq(area2)

    # カテゴリーのみ
    if area2 == '0' && category != '0' && amountSerchDiv == false :
      return Attr('category').eq(category)

    # 金額のみ
    if area2 == '0' && category == '0' && amountSerchDiv == true :
      return Attr('amount').GE(amount1) & Attr('amount').LE(amount2)

    # 地域2,カテゴリー
    if area2 != '0' && category != '0' && amountSerchDiv == false :
      return Attr('area2').eq(area2) & Attr('category').eq(category)

    # 地域2,金額
    if area2 != '0' && category == '0' && amountSerchDiv == true :
      return Attr('area2').eq(area2) & Attr('amount').GE(amount1) & Attr('amount').LE(amount2)

    # カテゴリー,金額
    if area2 == '0' && category != '0' && amountSerchDiv == true :
      return Attr('category').eq(category) & Attr('amount').GE(amount1) & Attr('amount').LE(amount2)

    # 地域2,カテゴリー,金額
    if area2 == '0' && category != '0' && amountSerchDiv == true :
      return Attr('area2').eq(area2) & Attr('category').eq(category) & Attr('amount').GE(amount1) & Attr('amount').LE(amount2)

    return ''


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        # インデックスタイプチェック
        if IndexType == 'SERCH-SLIP-INDEX':
            area2 = event['Keys']['areaNo2']
            # 検索値「エリア2のチェック」
            if area2 == 0:
                return areaNo1_query(event)
            else:
                return areaNo1AndAreaNo2_query(event)
        elif:
          return 500



    except Exception as e:
        print("Error Exception.")
        print(e)