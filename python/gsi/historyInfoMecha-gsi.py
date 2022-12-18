import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("historyInfoMecha")

# ���R�[�h���� historyId-index
def historyId_query(partitionKey):
    queryData = table.query(
        IndexName = 'historyId-index',
        KeyConditionExpression = Key("historyId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# ���R�[�h���� mechanicId-index
def mechanicId_query(partitionKey):
    queryData = table.query(
        IndexName = 'mechanicId-index',
        KeyConditionExpression = Key("mechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['historyId']
        if IndexType == 'HISTORYID-INDEX':
            return historyId_query(PartitionKey)

        elif IndexType == 'MECHANICID-INDEX':
          PartitionKey = event['Keys']['mechanicId']
          return mechanicId_query(PartitionKey)
        
    except Exception as e:
        print("Error Exception.")
        print(e)