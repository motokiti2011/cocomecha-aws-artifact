import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
userMyList = dynamodb.Table("userMyList")

# ���J�j�b�N�\�����ݏ��̎擾Lambda
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    adminOfficeId = event['Keys']['adminOfficeId']

    try:
        # �����^�C�v����
        if IndexType != 'GETREQUESTMECHANICINFO':
          return

        # �f�[�^�擾
        items = userMyList_query(adminOfficeId)

        resultItems = []
        # ���ʂ̊i�[
        for item in items  :

          resultItems.append(item['requestInfo'])

        return resultItems


    except Exception as e:
        print("Error Exception.")
        print(e)


# �}�C���X�g��񌟍� 
def userMyList_query(adminOfficeId) :

    options = {
      'IndexName' : 'officeId-index',
      'KeyConditionExpression': Key("officeId").eq(adminOfficeId),
      'FilterExpression': Attr('category').contains('22'),
    }
    queryData = officeInfo.query(**options)
    items=queryData['Items']
    print(items)
    return items


