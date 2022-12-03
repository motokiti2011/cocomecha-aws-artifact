import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("transactionSlip")
# �e�[�u���X�L����
def operation_scan():
    scanData = table.scan()
    items=scanData['Items']
    print(items)
    return scanData

# 1���R�[�h���� slipAdminUserId-index
def slipAdminUserId_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminUserId-index',
        KeyConditionExpression = Key("slipAdminUserId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return queryData

# 2���R�[�h���� slipAdminOffice-index
def slipAdminOffice_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminOffice-index',
        KeyConditionExpression = Key("slipAdminOffice").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return queryData

# 3���R�[�h���� slipAdminBaseId-index
def slipAdminBaseId_query(partitionKey):
    queryData = table.query(
        IndexName = 'slipAdminBaseId-index',
        KeyConditionExpression = Key("slipAdminBaseId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return queryData

# 4���R�[�h���� bidderId-index
def bidderId_query(partitionKey):
    queryData = table.query(
        IndexName = 'categoryAndAreaNo1-index',
        KeyConditionExpression = Key("bidderId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return queryData



def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    OperationType = event['OperationType']
    IndexType = event['IndexType']
    try:
        if OperationType == 'SCAN':
            return operation_scan()

        PartitionKey = event['Keys']['slipAdminUserId']
        if IndexType == 'SLIPADMINUSERID-INDEX':
            return slipAdminUserId_query(PartitionKey)

        elif IndexType == 'SLIPADMINOFFICE-INDEX':
          PartitionKey = event['Keys']['slipAdminOffice']
          return slipAdminOffice_query(PartitionKey, SortKey)

        elif IndexType == 'SLIPADMINBASEID-INDEX':
          PartitionKey = event['Keys']['slipAdminBaseId']
          return slipAdminBaseId_query(PartitionKey)

        elif IndexType == 'BIDDERID-INDEX':
          PartitionKey = event['Keys']['bidderId']
          return bidderId_query(PartitionKey, SortKey)

    except Exception as e:
        print("Error Exception.")
        print(e)