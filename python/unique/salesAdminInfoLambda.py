import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
mechanicInfo = dynamodb.Table("mechanicInfo")
officeInfo = dynamodb.Table("officeInfo")

# ���J�j�b�N��񌟍� mechanicInfo
def mechanicInfo_query(id) :
    queryData = userInfo.query(
        KeyConditionExpression = Key("mechanicId").eq(id)
    )
    items=queryData['Items']
    print(items)
    return items


# �H���񌟍� officeInfo
def userInfo_query(id) :
    queryData = officeInfo.query(
        KeyConditionExpression = Key("officeId").eq(id)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    id = event['Keys']['id']
    serviceType = event['Keys']['serviceType']

    try:
        # �����^�C�v����
        if IndexType != 'SALESADMININFO':
          return

        # �f�[�^�擾
        queryItems = []
        if serviceType == '1'
          items = mechanicInfo_query(id)
          # ���ʂ̊i�[
          result={
            'adminId' :items[0]['mechanicId'],
            'adminName' :items[0]['mechanicName'],
            'mail' :items[0]['mailAdress'],
            'telNo':items[0]['telList'],
            'post' :items[0]['introduction'],
            'adless' : None,
            'introduction' :items[0]['introduction'],
            'affiliationOfficeId' :items[0]['officeId'],
            'affiliationOfficeName' :items[0]['associationOfficeList'],
            'qualification' :items[0]['qualification'],
            'specialtyWork' :items[0]['specialtyWork'],
            'workContentList' : None,
            'businessHours' : None,
            'baseInfoList' : None,
            'evaluationInfo' : None,
            'profileImageUrl' :items[0]['profileImageUrl']
          }
        else:
          items = officeInfo_query(id)
          # ���ʂ̊i�[
          result={
            'adminId' :items[0]['officeId'],
            'adminName' :items[0]['officeName'],
            'mail' :items[0]['officeMailAdress'],
            'telNo': items[0]['userName'],
            'post' : items[0]['officePostCode'],
            'adless' : items[0]['officeArea1'],
            'introduction' : items[0]['introduction'],
            'affiliationOfficeId' : None,
            'affiliationOfficeName' : None,
            'qualification' : None,
            'specialtyWork' : None,
            'workContentList' : items[0]['workContentList'],
            'businessHours' : items[0]['businessHours'],
            'baseInfoList' : items[0]['baseInfoList'],
            'evaluationInfo' : None,
            'profileImageUrl' :items['profileImageUrl']
          }
        

        return result


    except Exception as e:
        print("Error Exception.")
        print(e)