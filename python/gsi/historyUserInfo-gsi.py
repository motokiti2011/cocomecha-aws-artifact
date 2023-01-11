import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("historyUserInfo")

# ���R�[�h���� userId-index
def userId_query(partitionKey):
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# ���R�[�h���� slipNo-index
def slipNo_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipNo-index',
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# ���R�[�h���� officeId-index
def officeId_query(partitionKey):
    queryData = table.query(
        IndexName = 'officeId-index',
        KeyConditionExpression = Key("officeId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['id']
        if IndexType == 'USERID-INDEX':
            return userId_query(PartitionKey)

        elif IndexType == 'SLIPNO-INDEX':
          PartitionKey = event['Keys']['id']
          return slipNo_query(PartitionKey)

        elif IndexType == 'OFFICEID-INDEX':
          PartitionKey = event['Keys']['id']
          return officeId_query(PartitionKey)

    except Exception as e:
        print("Error Exception.")
        print(e)