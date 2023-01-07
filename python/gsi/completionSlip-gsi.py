import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("completionSlip")

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
def slipAdminBaseId_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminBaseId-index',
        KeyConditionExpression = Key("slipAdminMechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['slipAdminUserId']
        if IndexType == 'SLIPADMINUSERID-INDEX':
            return slipAdminUserId_query(PartitionKey)

        elif IndexType == 'SLIPADMINOFFICE-INDEX':
          PartitionKey = event['Keys']['slipAdminOfficeId']
          return slipAdminOffice_query(PartitionKey, SortKey)

        elif IndexType == 'SLIPADMINMECHANIC-INDEX':
          PartitionKey = event['Keys']['slipAdminMechanicId']
          return slipAdminBaseId_query(PartitionKey)

    except Exception as e:
        print("Error Exception.")
        print(e)