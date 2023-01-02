import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("salesServiceInfo")

# 1���R�[�h���� areaNo1-index
def areaNo1_query(partitionKey) :
    queryData = table.query(
        IndexName = 'areaNo1AndAreaNo2-index',
        KeyConditionExpression = Key("areaNo1").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items



# 2���R�[�h���� areaNo1AndAreaNo2-index
def areaNo1AndAreaNo2_query(partitionKey, sortKey) :
    queryData = table.query(
        IndexName = 'areaNo1AndAreaNo2-index',
        KeyConditionExpression = Key("areaNo1").eq(partitionKey) & Key("areaNo2").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return items


# �^�C�g���`�F�b�N serchTitle
def serchTitle(checkTitle, title) :
    # ������v�`�F�b�N
    if checkTitle in title :
      return false
    else :
      return true



# ���i�`�F�b�N serchPrice
def serchPrice(price, priceB, priceU) :
    # ���i�͈̓`�F�b�N
    if price >= priceB :
      if price <= priceU :
        return false
      else :
        return true
    else :
      return true


# ���t�`�F�b�N serchDate
def serchDate(preferredDate, date1, date2, dateKey) :
    # �������@�i�͈́j
    if dateKey == '0' :
      if preferredDate >= date1 :
        if preferredDate <= date2 :
          return false
        else :
          return true
      else :
        return true

    # �������@�i�ȏ�j
    if dateKey == '1' :
      if preferredDate >= date1 :
          return false
      else :
        return true

    # �������@�i�����j
    if dateKey == '2' :
      if preferredDate <= date2 :
          return false
      else :
        return true

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:
        # �폜�敪
        deleteDiv = '0'
        # ���N�G�X�g�{�f�B���p�����[�^�Ɋ���U��
        # �T�[�r�X�J�e�S���[
        category = event['Keys']['category']
        # �^�C�g��
        title = event['Keys']['title']
        # �T�[�r�X�n��1
        areaNo1 = event['Keys']['areaNo1']
        # �T�[�r�X�n��2
        areaNo2 = event['Keys']['areaNo2']
        # ���i����
        priceB = event['Keys']['priceBottom']
        # ���i���
        priceU = event['Keys']['priceUpper']
        # ���D����
        bidMethod = event['Keys']['bidMethod']
        # �H���X�e�[�^�X
        processStatus = event['Keys']['processStatus']
        # �Ώێԗ����
        targetVehicleInfo = event['Keys']['targetVehicleInfo']
        # ��Əꏊ���
        workAreaInfo = event['Keys']['workAreaInfo']
        # ��]��1
        date1 = event['Keys']['date']
        # ��]��2
        date2 = event['Keys']['date2']
        # ��]�������L�[
        preferredDateKey = event['Keys']['preferredDateKey']

        # �����^�C�v����
        if IndexType != 'SERCHSLIPCONTENTS':
          return

        # �f�[�^�擾
        queryItems = []
        if not areaNo2 :
         queryItems = areaNo1_query(areaNo1)
        else :
         queryItems = areaNo1AndAreaNo2_query(areaNo1, areaNo2)
        
        
        resultItems = []
        
        # �i�荞��
        for item in queryItems :
          # �J�e�S���[
          if category != "" :
            if category != item['category'] :
              continue
          # ���D����
          if bidMethod != "" :
            if bidMethod != item['bidMethod'] :
              continue

          # �폜�敪
          if item[deleteDiv] != "0" :
            continue

          # �H���X�e�[�^�X
          if processStatus != "" :
            if processStatus != item['processStatus'] :
              continue

          # �Ώێԗ����
          if targetVehicleInfo != "" :
            if targetVehicleInfo != item['targetVehicleInfo'] :
              continue

          # ��Əꏊ���
          if workAreaInfo != "" :
            if workAreaInfo != item['workAreaInfo'] :
              continue

          # �^�C�g���i������v�j
          if title != "" :
            if serchTitle(item['title'], title) :
              continue

          # ���i
          if serchPrice(item['price'], priceB, priceU) :
            continue          
          
          # ��]��
          if preferredDateKey != "" :
            if serchDate(item['preferredDate'], date1, date2, preferredDateKey) :
              continue

          # �`�F�b�N��l���i�[
          resultItems.append(item)

        return resultItems


    except Exception as e:
        print("Error Exception.")
        print(e)