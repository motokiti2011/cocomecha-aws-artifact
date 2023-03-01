import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
userInfo = dynamodb.Table("userInfo")


# ���[�U�[��񌟍� userInfo
def userInfo_query(id) :
    queryData = userInfo.query(
        KeyConditionExpression = Key("userId").eq(id) & Key("userValidDiv").eq("0")
    )
    items=queryData['Items']
    print(items)
    return items[0]


def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    id = event['Keys']['id']

    try:
        # �����^�C�v����
        if IndexType != 'SLIPADMININFO':
          return

        # �f�[�^�擾
        items = userInfo_query(id)
        
        resultItems = []
        
        # ���ʂ̊i�[
        result={
          'adminId' :items['userId'],
          'adminName' :items['userName'],
          'mail' :None,
          'telNo':None,
          'post' :None,
          'adless' :items['areaNo1'],
          'introduction' :items['introduction'],
          'affiliationOfficeId' :None,
          'affiliationOfficeName' :None,
          'qualification' :None,
          'specialtyWork' :None,
          'workContentList' :None,
          'businessHours' :None,
          'baseInfoList' :None,
          'evaluationInfo' :None,
          'profileImageUrl' :items['profileImageUrl']
        }

        return result


    except Exception as e:
        print("Error Exception.")
        print(e)