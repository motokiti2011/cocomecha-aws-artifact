import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
userInfo = dynamodb.Table("userInfo")
mechanicInfo = dynamodb.Table("mechanicInfo")
officeInfo = dynamodb.Table("officeInfo")


def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    OperationType = event['OperationType']
    adminId = event['Keys']['adminId']
    serviceType = event['Keys']['serviceType']
    accessUser = event['Keys']['accessUser']

    try:
        # �A�N�Z�X���@�����������ꍇ�����I��
        if OperationType != 'CHECKACCESEADMIN':
          return

        print('1')
        adminInfo = ''
        # �T�[�r�X�^�C�v�����[�U�[�̏ꍇ
        if serviceType == '0':
          adminInfo = userInfo_query(adminId)
        # �T�[�r�X�^�C�v�����J�j�b�N�̏ꍇ
        elif serviceType == '1':
          adminInfo = mechanicInfo_query(adminId)
        # �T�[�r�X�^�C�v���H��̏ꍇ
        else:
          adminInfo = officeInfo_query(adminId)

        # �A�N�Z�X���[�U�[���擾
        accessUserInfo = []
        # ���[�U�[�܂��̓��J�j�b�N�̏ꍇ���[�U�[��񂩂�ID���肷��
        if serviceType != '2':

          # �F�؏��`�F�b�N�テ�[�U�[ID���擾
          # ����
          input_event = {
              "userId": accessUser,
          }
          Payload = json.dumps(input_event) # json�V���A���C�Y
          # ���������ŌĂяo��
          response = boto3.client('lambda').invoke(
              FunctionName='CertificationLambda',
              InvocationType='RequestResponse',
              Payload=Payload
          )
          body = json.loads(response['Payload'].read())
          print(body)
          # ���[�U�[���̃��[�U�[ID���擾
          if body != None :
            userId = body
          else :
            print('NOT-CERTIFICATION')
            return

          accessUserInfo = userInfo_query(userId)
        else:
          accessUserInfo = officeInfo_query(accessUser)

        print('2')
        print(adminInfo)
        print(accessUserInfo)

        # ����
        # �T�[�r�X�^�C�v�����[�U�[�̏ꍇ
        idList = []
        if serviceType == '0':
          print('3')
          if adminInfo[0]['userId'] == accessUserInfo[0]['userId']:
            return True
          else:
            return False
        # �T�[�r�X�^�C�v�����J�j�b�N�̏ꍇ
        elif serviceType == '1':
          print('4')
          if adminInfo[0]['mechanicId'] == accessUserInfo[0]['mechanicId']:
            return True
          else:
            return False
        # �T�[�r�X�^�C�v���H��̏ꍇ
        else:
          print('5')
          checkList = accessUserInfo[0]['adminIdList']
          
          return adminInfo[0]['officeId'] in checkList

    except Exception as e:
        print("Error Exception.")
        print(e)



# ���[�U�[��񌟍�
def userInfo_query(id) :
    queryData = userInfo.query(
        KeyConditionExpression = Key("userId").eq(id) & Key("userValidDiv").eq("0")
    )
    items=queryData['Items']
    print(items)
    return items

# ���J�j�b�N��񌟍�
def mechanicInfo_query(id) :
    queryData = mechanicInfo.query(
        KeyConditionExpression = Key("mechanicId").eq(id)
    )
    items=queryData['Items']
    print(items)
    return items

# �H���񌟍�
def officeInfo_query(id) :
    queryData = officeInfo.query(
        KeyConditionExpression = Key("officeId").eq(id)
    )
    items=queryData['Items']
    print(items)
    return items



