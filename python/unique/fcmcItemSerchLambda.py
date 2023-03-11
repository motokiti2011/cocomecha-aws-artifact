import json
import boto3

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
mechanicInfo = dynamodb.Table("mechanicInfo")
officeInfo = dynamodb.Table("officeInfo")
factoryMechaInicItem = dynamodb.Table("factoryMechaInicItem")

# �H�ꃁ�J�j�b�N������i�擾
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:
        # �C���f�b�N�X�m�F
        if IndexType != 'FCMCITEM':
          return []

        # �A�N�Z�X�������J�j�b�NID���擾
        mechanicId =event['Keys']['acceseMechanicId']
        # ���J�j�b�N�����擾
        mcInfo = getMechanicInfo(mechanicId) :
        # ���J�j�b�N��񂪎擾�ł��Ȃ������ꍇ�����I��
        if len(mcInfo) == 0 :
          return []
        
        resultList = []

        # ���J�j�b�NID���Ǘ��҂̍H�ꃁ�J�j�b�N�A�C�e�������擾
        resultList += fcMcItem_query(mechanicId) :
        
        # �H��ID���擾
        officeId = mcInfo[0]['officeId']
        if not officeId || officeId == '0' :
            return resultList 
        
        # �H������擾
        fcInfo = getFactorycInfo(officeId) :
        
        # �H���񂪎擾�ł��Ȃ������ꍇ�����I��
        if len(fcInfo) == 0 :
          return resultList
        # �H��֘A�ҏ����擾
        connectionMcList = fcInfo[0]['connectionMechanicInfo']

        connectionDiv = False
        # �֘A�҃`�F�b�N
        for mc in connectionMcList :
          # �֘A�҂ɂȂ邩���`�F�b�N
          if mc === mechanicId :
              connectionDiv = True

        if connectionDiv :
            # �H��ID�ōH�ꃁ�J�j�b�N�A�C�e�������擾
            resultList += fcMcItem_query(officeId) :

       return resultList

    except Exception as e:
        print("Error Exception.")
        print(e)


# ���J�j�b�N�����擾
def getMechanicInfo(mechanicId):
    queryData = mechanicInfo.query(
        KeyConditionExpression = Key("mechanicId").eq(mechanicId)
    )
    items=queryData['Items']
    print(items)
    return items

# ���J�j�b�N���ɕR�Â��H�ꃁ�J�j�b�N�A�C�e�������擾
def fcMcItem_query(partitionKey):
    queryData = factoryMechaInicItem.query(
        IndexName = 'factoryMechanicId-index',
        KeyConditionExpression = Key("factoryMechanicId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# �H������擾
def getFactorycInfo(officeId):
    queryData = officeInfo.query(
        KeyConditionExpression = Key("officeId").eq(officeId)
    )
    items=queryData['Items']
    print(items)
    return items

# �`�[����ԋp���ɉ��H����
def editItems(service):
    if len(service) == 0 :
        return []
    
    result = []
    for se in service :
    Item={
      'serviceId' : PartitionKey,
      'serviceName' : event['Keys']['officeName'],
      'serviceType' : event['Keys']['officeTel'],
      'transactionStatus' : event['Keys']['officeMailAdress'],
      'browsingCount' : '0',
      'favoriteCount' : '0'
    }

    queryData = table.query(
        IndexName = 'slipAdminOfficeId-index',
        KeyConditionExpression = Key("slipAdminOfficeId").eq(officeId) & Key("deleteDiv").eq('1')
    )
    items=queryData['Items']
    print(items)
    return items