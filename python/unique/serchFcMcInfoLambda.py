import json
import boto3

from boto3.dynamodb.conditions import Key, Attr

# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
mechanicInfo = dynamodb.Table("mechanicInfo")
officeInfo = dynamodb.Table("officeInfo")

# �H��E���J�j�b�N����Lambda
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    ServiceType = event['ServiceType']
    area1 = event['Keys']['area1']
    area2 = event['Keys']['area2']
    name = event['Keys']['name']
    telNo = event['Keys']['telNo']


    try:
        # �����^�C�v����
        if IndexType != 'SERCHFCMCINFO':
          return

        # �f�[�^�擾
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
          # ���ʂ̊i�[(���J�j�b�N)
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
          # ���ʂ̊i�[(�H��)
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

# ���������쐬
def createFilter(ServiceType, name, telNo):

    # ���������쐬

    # �H�� ���́A�d�b�ԍ��Ȃ�
    if ServiceType == '2' and name == '' and telNo == '' :
      print('1')
      return ''
    # �H�� ���́A�d�b�ԍ�
    if ServiceType == '2' and name != '' and telNo != '' :
      print('2')
      return Attr('name').contains(name) & Attr('telNo').contains(telNo)
    # �H�� ����
    if ServiceType == '2' and name != '' and telNo == '' :
      print('3')
      return Attr('name').contains(name)
    # �H�� �d�b�ԍ�
    if ServiceType == '2' and name == '' and telNo != '' :
      print('4')
      return Attr('telNo').contains(telNo)

    # ���J�j�b�N, �Ȃ�
    if ServiceType == '1' and telNo == '' :
      print('5')
      return ''
    # ���J�j�b�N, �d�b�ԍ�
    if ServiceType == '1' telNo != '' :
      print('6')
      return Attr('telNo').contains(telNo)
    print('7')
    return ''

# ���J�j�b�N��񌟍�
def mechanicInfo_query(options) :
    queryData = mechanicInfo.query(**options)
    items=queryData['Items']
    print(items)
    return items

# �H���񌟍�
def officeInfo_query(options) :
    queryData = officeInfo.query(**options)
    items=queryData['Items']
    print(items)
    return items

    except Exception as e:
        print("Error Exception.")
        print(e)