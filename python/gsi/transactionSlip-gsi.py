import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("transactionSlip")

# ������`�[���GSI����
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    SortKey = event['Keys']['serviceType']

    try:
        PartitionKey = event['Keys']['id']
        if IndexType == 'SLIPUSER-INDEX':

            cognitoUserId = PartitionKey
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

            return slipUser_query(userId,SortKey)

        elif IndexType == 'SLIPOFFICE-INDEX':
          PartitionKey = event['Keys']['id']
          return slipOffice_query(PartitionKey, SortKey)

        elif IndexType == 'SLIPMECHANIC-INDEX':
          PartitionKey = event['Keys']['id']
          return slipMechanic_query(PartitionKey,SortKey)

    except Exception as e:
        print("Error Exception.")
        print(e)



# 1���R�[�h���� slipUserId-index
def slipUser_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 2���R�[�h���� slipOffice-index
def slipOffice_query(partitionKey):
    queryData = table.query(
        IndexName = 'officeId-index',
        KeyConditionExpression = Key("officeId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 3���R�[�h���� slipMechanic-index
def slipMechanic_query(partitionKey):
    queryData = table.query(
        IndexName = 'mechanicId-index',
        KeyConditionExpression = Key("mechanicId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items


