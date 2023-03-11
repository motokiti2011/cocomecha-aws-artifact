import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("userFavorite")

# ���C�ɓ����񕡐��폜
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:
        # �����^�C�v����
        if IndexType != 'MULTIPLEDELETEFAVORITE':
          return

        # �f�[�^�擾
        queryItems =event['Keys']['idList']
        
        if len(queryItems) == 0 :
          return []
        
        # ID�����폜
        for item in queryItems :
          # �폜
          response = operation_delete(item['id']) :
          if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            # �ُ�I���Ƃ��ĕԋp
            return response
          # �H�ꃁ�J�j�b�N���i���̂��C�ɓ��萔���X�V
          # ����
          input_event = {
              "processDiv": '1',
              "serviceId": item['id'],
              "serviceType": item['serviceType'],
              "status": '1'
          }
          Payload = json.dumps(input_event) # json�V���A���C�Y
          # �Ăяo��
          boto3.client('lambda').invoke(
              FunctionName='internalFcMcItemLambda',
              InvocationType='Event',
              Payload=Payload
          )

       # �S���폜�㐳��X�e�[�^�X�ԋp
       return 200

    except Exception as e:
        print("Error Exception.")
        print(e)

# ���R�[�h�폜
def operation_delete(partitionKey):
    delResponse = table.delete_item(
       key={
           'id': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponsee['ResponseMetadata']['HTTPStatusCode'])
    else:
        print('DEL Successed.')
    return delResponsee




