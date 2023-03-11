import json
import boto3

from boto3.dynamodb.conditions import Key, Attr

# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
mechanicInfo = dynamodb.Table("mechanicInfo")
officeInfo = dynamodb.Table("officeInfo")

# 工場・メカニック検索Lambda
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    ServiceType = event['ServiceType']
    area1 = event['Keys']['area1']
    area2 = event['Keys']['area2']
    name = event['Keys']['name']
    telNo = event['Keys']['telNo']


    try:
        # 検索タイプ検証
        if IndexType != 'SERCHFCMCINFO':
          return

        # データ取得
        items = []
        serchFilter = createFilter(ServiceType, name, telNo)
        
        if serchFilter != '' :
          options = {
            'IndexName' : 'areaNo1AndAreaNo2-index',
            'KeyConditionExpression': Key("areaNo1").eq(area1) & Key("areaNo2").eq(area2),
            'FilterExpression': serchFilter,
          }
        else :
          options = {
            'IndexName' : 'areaNo1AndAreaNo2-index',
            'KeyConditionExpression': Key("areaNo1").eq(area1) & Key("areaNo2").eq(area2),
          }
        
        resultItems = []
        
        if ServiceType == '1' :
          items = mechanicInfo_query(options)
          # 結果の格納(メカニック)
          for item in items  :
            result={
              'id' :item['officeId'],
              'name' :item['officeName'],
              'tel' :item['officeTel'],
              'mailAdress':item['officeMailAdress'],
              'area1' :item['officeArea1'],
              'area2' :item['officeArea'],
              'adress' :item['officeAdress'],
              'postCode' :item['officePostCode'],
              'introduction' :item['officePR'],
              'PRimageURL' :item['profileImageUrl']
            }
            
            resultItems.append(result)
            
        else :
          items = officeInfo_query(options)
          # 結果の格納(工場)
          for item in items  :
            result={
              'id' :item['mechanicId'],
              'name' :item['mechanicName'],
              'tel' :item['telList'],
              'mailAdress':item['mailAdress'],
              'area1' :item['areaNo1'],
              'area2' :item['areaNo2'],
              'adress' :item['adress'],
              'postCode' :None,
              'introduction' :item['introduction'],
              'PRimageURL' :item['profileImageUrl']
            }
            
            resultItems.append(result)

        return resultItems

# 検索条件作成
def createFilter(ServiceType, name, telNo):

    # 検索条件作成

    # 工場 名称、電話番号なし
    if ServiceType == '2' and name == '' and telNo == '' :
      print('1')
      return ''
    # 工場 名称、電話番号
    if ServiceType == '2' and name != '' and telNo != '' :
      print('2')
      return Attr('name').contains(name) & Attr('telNo').contains(telNo)
    # 工場 名称
    if ServiceType == '2' and name != '' and telNo == '' :
      print('3')
      return Attr('name').contains(name)
    # 工場 電話番号
    if ServiceType == '2' and name == '' and telNo != '' :
      print('4')
      return Attr('telNo').contains(telNo)

    # メカニック, なし
    if ServiceType == '1' and telNo == '' :
      print('5')
      return ''
    # メカニック, 電話番号
    if ServiceType == '1' telNo != '' :
      print('6')
      return Attr('telNo').contains(telNo)
    print('7')
    return ''

# メカニック情報検索
def mechanicInfo_query(options) :
    queryData = mechanicInfo.query(**options)
    items=queryData['Items']
    print(items)
    return items

# 工場情報検索
def officeInfo_query(options) :
    queryData = officeInfo.query(**options)
    items=queryData['Items']
    print(items)
    return items

    except Exception as e:
        print("Error Exception.")
        print(e)