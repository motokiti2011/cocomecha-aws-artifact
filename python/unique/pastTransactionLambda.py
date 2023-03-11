import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("completionSlip")

# �ߋ�������擾
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    id = event['Keys']['adminId']
    serviceType = event['Keys']['serviceType']
    accessUser = event['Keys']['accessUser']


    try:
        # �����^�C�v����
        if IndexType != 'PASTTRANSACTION':
          return


        #�Ǘ��҃`�F�b�N
        # ����
        input_event = {
            "adminId": id,
            "serviceType": serviceType,
            "accessUser": accessUser
        }
        Payload = json.dumps(input_event) # json�V���A���C�Y
        print("---01: Payload:", Payload)
        # �Ăяo��
        response = boto3.client('lambda').invoke(
            FunctionName='internalAdminCheckLambda',
            InvocationType='RequestResponse',
            Payload=Payload
        )

        body = json.loads(response['Payload'].read()) #�ǂ����HTTP�w�b�_�[�͓���Ȍ`�����Ă���悤�ŁA���ʂ�json.
        print("---03: body:", body)

        print(id)

        resultItems = []

        # �f�[�^�擾
        if serviceType == '0':
          resultItems = slipAdminUserId_query(id)
        elif serviceType == '1':
          resultItems = slipAdminMechanicId_query(id)
        else:
          resultItems = slipAdminOffice_query(id)
        
        # ���ʂ̊i�[
        if body:
          # �Ǘ��҂̏ꍇ�S�f�[�^�ԋp
          return resultItems
        else :
          # ����ȊO�̓f�[�^�ҏW�ԋp
          return setItems(resultItems)

    except Exception as e:
        print("Error Exception.")
        print(e)



# 1���R�[�h���� slipAdminUserId-index
def slipAdminUserId_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminUserId-index',
        KeyConditionExpression = Key("slipAdminUserId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 2���R�[�h���� slipAdminOfficeId-index
def slipAdminOffice_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminOffice-index',
        KeyConditionExpression = Key("slipAdminOfficeId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 3���R�[�h���� slipAdminMechanicId-index
def slipAdminMechanicId_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminMechanicId-index',
        KeyConditionExpression = Key("slipAdminMechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items# ���[�U�[��񌟍� userInfo


# �Ǘ��җp�f�[�^�Z�b�g
def setItems(itemList) :

    resultList = []
    for item in itemList :
      # �f�[�^�Z�b�g
      resultList.append(dataItem={
        'slipNo' : item[slipNo],
        'slipAdminUserId' : '',
        'slipAdminOfficeId' : '',
        'slipAdminMechanicId' : '',
        'adminDiv' : '',
        'title' : item['title'],
        'price' : item['price'],
        'bidMethod' : item['bidMethod'],
        'bidderId' : '',
        'bidEndDate' : item['bidEndDate'],
        'explanation' : item['explanation'],
        'targetService' : item['targetService'],
        'targetVehicleId' : '',
        'targetVehicleName' : item['targetVehicleName'],
        'targetVehicleInfo' : None,
        'workAreaInfo' : None,
        'evaluationId' : item['evaluationId'],
        'completionDate' : item['completionDate'],
        'transactionCompletionDate' : item['transactionCompletionDate'],
        'thumbnailUrl' : item['thumbnailUrl'],
        'imageUrlList' : [],
        'created' : '',
        'updated' : ''
      })

    return resultList