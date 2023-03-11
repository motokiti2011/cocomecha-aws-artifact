import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("factoryMechaInicItem")

# ���R�[�h���� factoryMechanicId-index
def userId_query(partitionKey):
    queryData = table.query(
        IndexName = 'factoryMechanicId-index',
        KeyConditionExpression = Key("factoryMechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['factoryMechanicId']
        if IndexType == 'USERID-INDEX':
            return factoryMechanicId_query(PartitionKey)

        elif IndexType == 'FACTORYMECHANICID-INDEX':
          PartitionKey = event['Keys']['factoryMechanicId']
          return vehicleNo_query(PartitionKey)

    except Exception as e:
        print("Error Exception.")
        print(e)