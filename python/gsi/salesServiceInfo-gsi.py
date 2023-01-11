import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("salesServiceInfo")

# 1���R�[�h���� areaNo1-index
def areaNo1_query(partitionKey):
    queryData = table.query(
        IndexName = 'areaNo1-index',
        KeyConditionExpression = Key("areaNo1").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# 2���R�[�h���� areaNo1AndAreaNo2-index
def areaNo1AndAreaNo2_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'areaNo1AndAreaNo2-index',
        KeyConditionExpression = Key("officeId").eq(partitionKey) & Key("areaNo2").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return items


# 3���R�[�h���� slipAdminOffice-Index
def slipAdminOffice_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'slipAdminOfficeId-index',
        KeyConditionExpression = Key("slipAdminOfficeId").eq(partitionKey) & Key("deleteDiv").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return items


# 4���R�[�h���� slipAdminMechanic-Index
def slipAdminMechanic_query(partitionKey, sortKey):
    queryData = table.query(
        IndexName = 'slipAdminMechanic-index',
        KeyConditionExpression = Key("slipAdminMechanicId").eq(partitionKey) & Key("deleteDiv").eq("sortKey")
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        PartitionKey = event['Keys']['areaNo1']
        if IndexType == 'AREANO1-INDEX':
            return areaNo1_query(PartitionKey)

        elif IndexType == 'AREANO1ANDAREANO2-INDEX':
          PartitionKey = event['Keys']['areaNo1']
          SortKey = event['Keys']['areaNo2']
          return areaNo1AndAreaNo2_query(PartitionKey, SortKey)

        elif IndexType == 'SLIPADMINOFFICEID-INDEX':
          PartitionKey = event['Keys']['slipAdminOfficeId']
          SortKey = event['Keys']['deleteDiv']
          return slipAdminOffice_query(PartitionKey, SortKey)

        elif IndexType == 'SLIPADMINMECHANIC-INDEX':
          PartitionKey = event['Keys']['slipAdminMechanicId']
          SortKey = event['Keys']['deleteDiv']
          return slipAdminMechanic_query(PartitionKey, SortKey)

    except Exception as e:
        print("Error Exception.")
        print(e)