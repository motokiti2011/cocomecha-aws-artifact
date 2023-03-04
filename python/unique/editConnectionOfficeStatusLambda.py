import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
officeInfo = dynamodb.Table("officeInfo")

# 関連工場ステータス変更Lambda
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    adminOfficeId = office['adminOfficeId']
    connectionOffice = office['connectionOffice']

    try:
        # 検索タイプ検証
        if IndexType != 'CONNECTIONOFFICESTATUS':
          return

        # データ取得
        office = officeInfo_query(adminOfficeId)
        
        connectionData = office['connectionOfficeInfo']
        
        for item in connectionData  :
          if item['officeId'] == connectionOffice['officeId']
            # 結果の格納
            result={
              'officeId' :connectionOffice['officeId'],
              'officeName' :connectionOffice['officeName'],
              'officeAssociationDiv' :connectionOffice['officeAssociationDiv'],
              'officeAssociation':connectionOffice['officeAssociation']
            }


        putResponse = officeInfo.put_item(
          Item={
            'officeId' : adminOfficeId,
            'officeName' : office['officeName'],
            'officeTel' : office['officeTel'],
            'officeMailAdress' : office['officeMailAdress'],
            'officeArea1' : office['officeArea1'],
            'officeArea' : office['officeArea'],
            'officeAdress' : office['officeAdress'],
            'officePostCode' : office['officePostCode'],
            'workContentList' : office['workContentList'],
            'businessHours' : office['businessHours'],
            'connectionOfficeInfo' : connectionData,
            'connectionMechanicInfo' : office['connectionMechanicInfo'],
            'adminSettingInfo' : office['adminSettingInfo'],
            'officePR' : office['officePR'],
            'officePRimageURL' : office['officePRimageURL'],
            'officeFormList' : office['officeFormList'],
            'publicInfo' : office['publicInfo'],
            'created' : office['created'],
            'updated' :  now.strftime('%x %X')
          }
        )
        
        if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
          print(putResponse)
        else:
          print('Post Successed.')
        return putResponse['ResponseMetadata']['HTTPStatusCode']


    except Exception as e:
        print("Error Exception.")
        print(e)


# 工場情報検索 officeInfo
def officeInfo_query(adminOfficeId) :
    queryData = officeInfo.query(
        KeyConditionExpression = Key("officeId").eq(adminOfficeId)
    )
    items=queryData['Items']
    print(items)
    return items[0]


