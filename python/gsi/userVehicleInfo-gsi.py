import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("userVehicleInfo")

# ���[�U�[�ԗ����GSI����
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        if IndexType == 'USERID-INDEX':
            cognitoUserId = event['Keys']['id']
            # �F�؏��`�F�b�N�テ�[�U�[ID���擾
            # ����
            input_event = {
                "userId": cognitoUserId,
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
            return userId_query(userId)

        elif IndexType == 'VEHICLENO-INDEX':
          PartitionKey = event['Keys']['id']
          return vehicleNo_query(PartitionKey)


    except Exception as e:
        print("Error Exception.")
        print(e)




# ���R�[�h���� userId-index
def userId_query(partitionKey):
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


# ���R�[�h���� vehicleNo-index
def vehicleNo_query(partitionKey):
    queryData = table.query(
        IndexName = 'vehicleNo-index',
        KeyConditionExpression = Key("vehicleNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

