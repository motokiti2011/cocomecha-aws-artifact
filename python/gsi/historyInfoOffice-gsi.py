import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("historyInfoOffice")
# �e�[�u���X�L����
def operation_scan():
    scanData = table.scan()
    items=scanData['Items']
    print(items)
    return scanData

# ���R�[�h���� historyId-index
def historyId_query(partitionKey):
    queryData = table.query(
        IndexName = 'historyId-index',
        KeyConditionExpression = Key("historyId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return queryData

# ���R�[�h���� officeId-index
def officeId_query(partitionKey):
    queryData = table.query(
        IndexName = 'officeId-index',
        KeyConditionExpression = Key("officeId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return queryData


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['historyId']
        if IndexType == 'HISTORYID-INDEX':
            return historyId_query(PartitionKey)

        elif IndexType == 'OFFICEID-INDEX':
          PartitionKey = event['Keys']['officeId']
          return officeId_query(PartitionKey)
        
    except Exception as e:
        print("Error Exception.")
        print(e)