import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("evaluationInfo")


# ���R�[�h���� slipNo-index
def slipNo_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'slipNo-index',
        KeyConditionExpression = Key("slipNo").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items


# ���R�[�h���� mechanicId-index
def mechanicId_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'mechanicId-index',
        KeyConditionExpression = Key("mechanicId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items


# ���R�[�h���� officeId-index
def officeId_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'officeId-index',
        KeyConditionExpression = Key("officeId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['id']
        SortKey = event['Keys']['serviceType']
        if IndexType == 'MECHANICID-INDEX':
            return mechanicId_query(PartitionKey, SortKey)

        elif IndexType == 'OFFICEID-INDEX':
          return officeId_query(PartitionKey, SortKey)

        elif IndexType == 'SLIPNO-INDEX':
          return slipNo_query(PartitionKey, SortKey)

    except Exception as e:
        print("Error Exception.")
        print(e)