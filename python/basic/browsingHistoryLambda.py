import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("browsingHistory")

# �{��������񑀍�Lambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  OperationType = event['OperationType']

  try:

    if OperationType == 'QUERY':
      PartitionKey = event['Keys']['id']
      return operation_query(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['id']
      return put_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      return operation_delete(PartitionKey)

    elif OperationType == 'POST':
      id = str(uuid.uuid4())
      PartitionKey = id
      
      # �d���`�F�b�N
      uniqCheck = browsingUniqCheck(event)
      
      if uniqCheck:
        # �X�V
        return put_product(PartitionKey, event)
      else :
        # �H�ꃁ�J�j�b�N���i���̉{�����𐔂��X�V
        # ����
        input_event = {
            "processDiv": '0',
            "serviceId": event['Keys']['slipNo'],
            "serviceType": event['Keys']['serviceType'],
            "status": '0'
        }
        Payload = json.dumps(input_event) # json�V���A���C�Y
        # �Ăяo��
        boto3.client('lambda').invoke(
            FunctionName='internalFcMcItemLambda',
            InvocationType='Event',
            Payload=Payload
        )
        # �o�^
        return post_product(PartitionKey, event)

  except Exception as e:
      print("Error Exception.")
      print(e)



# ���R�[�h����
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("id").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# ���R�[�h�X�V
def put_product(PartitionKey, event):
  # �F�؏��`�F�b�N
  userId = CertificationUserId(event)
  if userId == None :
    print('NOT-CERTIFICATION')
    return 500

  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'userId' : userId,
      'slipNo' : event['Keys']['slipNo'],
      'title' : event['Keys']['title'],
      'price' : event['Keys']['price'],
      'whet' : event['Keys']['whet'],
      'endDate' : event['Keys']['endDate'],
      'imageUrl' : event['Keys']['imageUrl'],
      'serviceType' : event['Keys']['serviceType'],
      'created' : event['Keys']['created'],
      'updated' : datetime.now().strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse
  
  # ���R�[�h�폜
def operation_delete(partitionKey):
    delResponse = table.delete_item(
       Key={
           'id': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse


# ���R�[�h�ǉ�
def post_product(PartitionKey, event):
  # �F�؏��`�F�b�N
  userId = CertificationUserId(event)
  if userId == None :
    print('NOT-CERTIFICATION')
    return 500

  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'userId' : userId,
      'slipNo' : event['Keys']['slipNo'],
      'title' : event['Keys']['title'],
      'price' : event['Keys']['price'],
      'whet' : event['Keys']['whet'],
      'endDate' : event['Keys']['endDate'],
      'imageUrl' : event['Keys']['imageUrl'],
      'serviceType' : event['Keys']['serviceType'],
      'created' : datetime.now().strftime('%x %X'),
      'updated' : datetime.now().strftime('%x %X')

    }
  )


# �d���`�F�b�N
def browsingUniqCheck(event):
    # �X�V�Ώۂ̃��[�U�[ID�œo�^���̉{�����������擾����
    queryData = table.query(
        IndexName = 'userId-index',
        KeyConditionExpression = Key("userId").eq(event['Keys']['userId'])
    )
    items=queryData['Items']
    
    # ���擾�̏ꍇ�`�F�b�N���I������B
    if len(items) == 0 :
      return False
    
    for item in items :
      # �`�[�ԍ����d�������ꍇ�X�V
      if item['slipNo'] == event['Keys']['slipNo'] :
        return True
    # �d���Ȃ��̏ꍇ�o�^
    return False

# �F�؏�񂩂烆�[�U�[���擾
def CertificationUserId(event):
    cognitoUserId = event['Keys']['userId']
    # �F�؏��`�F�b�N�テ�[�U�[ID���擾
    # ����
    input_event = {
        "userId": cognitoUserId,
    }
    Payload = json.dumps(input_event) # json�V���A���C�Y
    # ���������ŌĂяo��
    response = boto3.client('lambda').invoke(
        FunctionName='CertificationLambda',
        InvocationType='RequestResponse',
        Payload=Payload
    )
    body = json.loads(response['Payload'].read())
    print(body)
    # ���[�U�[���̃��[�U�[ID���擾
    if body != None :
      return body
    else :
      print('NOT-CERTIFICATION')
      return None

