import json
import boto3

from datetime import datetime
from boto3.dynamodb.conditions import Key


# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("salesServiceInfo")

# 1レコード検索 areaNo1-index
def areaNo1_query(partitionKey) :
    queryData = table.query(
        IndexName = 'areaNo1AndAreaNo2-index',
        KeyConditionExpression = Key("areaNo1").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items



# 2レコード検索 areaNo1AndAreaNo2-index
def areaNo1AndAreaNo2_query(partitionKey, sortKey) :
    queryData = table.query(
        IndexName = 'areaNo1AndAreaNo2-index',
        KeyConditionExpression = Key("areaNo1").eq(partitionKey) & Key("areaNo2").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return items


# タイトルチェック serchTitle
def serchTitle(checkTitle, title) :
    # 部分一致チェック
    if checkTitle in title :
      return False
    else :
      return True



# 価格チェック serchPrice
def serchPrice(price, priceB, priceU) :
    # 価格範囲チェック
    # 絞り込み条件がない場合
    if priceB == priceU == '' :
      return False
    if priceB == '' :
      priceB = '0'
    if priceU == '' :
      priceU = '0'
    if price >= priceB :
      if price <= priceU :
        return False
      else :
        return True
    else :
      return True


# 日付チェック serchDate
def serchDate(preferredDate, date1, date2, dateKey) :
    # 検索方法（範囲）
    if dateKey == '0' :
      if preferredDate >= date1 :
        if preferredDate <= date2 :
          return False
        else :
          return True
      else :
        return True

    # 検索方法（以上）
    if dateKey == '1' :
      if preferredDate >= date1 :
          return False
      else :
        return True

    # 検索方法（未満）
    if dateKey == '2' :
      if preferredDate <= date2 :
          return False
      else :
        return True

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:
        # 削除区分
        deleteDiv = '0'
        # リクエストボディをパラメータに割り振る
        # サービスカテゴリー
        category = event['Keys']['category']
        # タイトル
        title = event['Keys']['title']
        # サービス地域1
        areaNo1 = event['Keys']['areaNo1']
        # サービス地域2
        areaNo2 = event['Keys']['areaNo2']
        # 価格下限
        priceB = event['Keys']['priceBottom']
        # 価格上限
        priceU = event['Keys']['priceUpper']
        # 入札方式
        bidMethod = event['Keys']['bidMethod']
        # 工程ステータス
        processStatus = event['Keys']['processStatus']
        # 対象車両情報
        targetVehicleInfo = event['Keys']['targetVehicleInfo']
        # 作業場所情報
        workAreaInfo = event['Keys']['workAreaInfo']
        # 希望日1
        date1 = event['Keys']['date']
        # 希望日2
        date2 = event['Keys']['date2']
        # 希望日検索キー
        preferredDateKey = event['Keys']['preferredDateKey']

        # 処理時間
        
        SERCHDATE = int(datetime.now().strftime('%Y%m%d'))
        print('SERCHDATE')
        print(SERCHDATE)
        
        TIMESTAMP = datetime.now().strftime('%H')
        print('TIMESTAMP')
        print(TIMESTAMP)
        
        
        
        
        # 検索タイプ検証
        if IndexType != 'SERCHSLIPCONTENTS':
          return

        # データ取得
        queryItems = []
        if not areaNo2 :
         queryItems = areaNo1_query(areaNo1)
        else :
         queryItems = areaNo1AndAreaNo2_query(areaNo1, areaNo2)
        
        
        resultItems = []
        
        # 絞り込み
        for item in queryItems :
          # カテゴリー
          if category != "0" :
            if category != item['category'] :
              continue
          # 入札方式
          if bidMethod != "" :
            if bidMethod != item['bidMethod'] :
              continue

          # 削除区分
          if item['deleteDiv'] != "0" :
            continue

          # 工程ステータス
          if processStatus != "" :
            if processStatus != item['processStatus'] :
              continue

          # 対象車両情報
          if targetVehicleInfo != "" :
            if targetVehicleInfo != item['targetVehicleInfo'] :
              continue

          # 作業場所情報
          if workAreaInfo != "" :
            if workAreaInfo != item['workAreaInfo'] :
              continue

          # タイトル（部分一致）
          if title != "" :
            if serchTitle(item['title'], title) :
              continue

          # 価格
          if serchPrice(item['price'], priceB, priceU) :
            continue          
          
          # 希望日
          if preferredDateKey != "" :
            if serchDate(item['preferredDate'], date1, date2, preferredDateKey) :
              continue

          # 期限切れチェック
          if SERCHDATE > item['preferredDate'] :
            if TIMESTAMP > item['preferredTime'] :
              continue
          # チェック後値を格納
          resultItems.append(item)

        return resultItems


    except Exception as e:
        print("Error Exception.")
        print(e)