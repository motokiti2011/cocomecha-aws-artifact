import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
factoryMechaInicItem = dynamodb.Table("factoryMechaInicItem")


# �H�ꃁ�J�j�b�N���i�̕ҏW���s��
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    processDiv = event['processDiv']

    serviceId = event['serviceId']
    serviceType = event['serviceType']
    status = event['status']

    try:
        # �����敪��0�̏ꍇ�{���������𑀍�
        if processDiv == '0':
          editBrowsing_query(event)
        # �����敪��1�̏ꍇ���C�ɓ�����𑀍�
        elif processDiv == '1':
          editFavorite_query(event)
        # ����ȊO�ꍇ�X�e�[�^�X�𑀍�
        else:
          editStatus_query(event)
    except Exception as e:
        print("Error Exception.")
        print(e)



# �H�ꃁ�J�j�b�N���擾
def fcmcItem_query(partitionKey,sortKey ) :
    queryData = factoryMechaInicItem.query(
        KeyConditionExpression = Key("serviceId").eq(partitionKey) & Key("serviceType").eq(sortKey)
    )
    items=queryData['Items']
    print(items)
    return items

# �H�ꃁ�J�j�b�N���X�V
def put_fcmcItem(PartitionKey, event):
  putResponse = factoryMechaInicItem.put_item(
    Item={
      'serviceId' : PartitionKey,
      'serviceName' : event['Keys']['serviceName'],
      'factoryMechanicId' : event['Keys']['factoryMechanicId'],
      'serviceType' : event['Keys']['serviceType'],
      'transactionStatus' : event['Keys']['transactionStatus'],
      'browsingCount' : event['Keys']['browsingCount'],
      'favoriteCount' : event['Keys']['favoriteCount']
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse['ResponseMetadata']['HTTPStatusCode']



# �{�����𐔂̍X�V
def editBrowsing_query(event) :
    serviceId = event['serviceId']
    serviceType = event['serviceType']
    status = event['status']

    �X�V���̎擾
    fcmcItem = fcmcItem_query(serviceId, serviceType)
    if len(fcmcItem) === 0:
      print('�{�������Ȃ������I��'+ json.dumps(event))
      return
    putItem = fcmcItem[0]
    # �����𔻒�
    if status === '0' :
      # ���Z
      putItem['browsingCount']+=1
    else:
      # ���Z�i�����Ȃ����c�j
      putItem['browsingCount']-=1
    # �ҏW�����X�V
    put_fcmcItem(putItem):


# ���C�ɓ��萔�̍X�V
def editFavorite_query(event) :
    serviceId = event['serviceId']
    serviceType = event['serviceType']
    status = event['status']

    �X�V���̎擾
    fcmcItem = fcmcItem_query(serviceId, serviceType)
    if len(fcmcItem) === 0:
      print('���C�ɓ���X�V���Ȃ������I��'+ json.dumps(event))
      return
    putItem = fcmcItem[0]
    # �����𔻒�
    if status === '0' :
      # ���Z
      putItem['favoriteCount']+=1
    else:
      # ���Z
      putItem['favoriteCount']-=1
    # �ҏW�����X�V
    put_fcmcItem(putItem):

# �X�e�[�^�X�̍X�V
def editStatus_query(event) :
    serviceId = event['serviceId']
    serviceType = event['serviceType']
    status = event['status']

    �X�V���̎擾
    fcmcItem = fcmcItem_query(serviceId, serviceType)
    if len(fcmcItem) === 0:
      print('�X�e�[�^�X�X�V���Ȃ������I��' + json.dumps(event))
      return
    putItem = fcmcItem[0]
    # �X�e�[�^�X���X�V
    putItem['transactionStatus'] = status
    # �ҏW�����X�V
    put_fcmcItem(putItem):


