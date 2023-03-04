import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
transactionSlip = dynamodb.Table("transactionSlip")
userMyList = dynamodb.Table("userMyList")



# ����˗�TBL���R�[�h�o�^
def post_transaction(PartitionKey, event):
  now = datetime.now()
  putResponse = transactionSlip.put_item(
    Item={
      'id' : PartitionKey,
      'serviceType' : event['Keys']['serviceType'],
      'userId' : event['Keys']['userId'],
      'mechanicId' : event['Keys']['mechanicId'],
      'officeId' : event['Keys']['officeId'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : event['Keys']['serviceTitle'],
      'slipRelation' : event['Keys']['slipRelation'],
      'slipAdminId' : event['Keys']['slipAdminId'],
      'slipAdminName' : event['Keys']['slipAdminName'],
      'bidderId' : event['Keys']['bidderId'],
      'deleteDiv' : '1',
      'completionScheduledDate' : event['Keys']['completionScheduledDate'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.')



# �`�[�Ǘ��҃}�C���X�g�̍X�V
def put_adminMyList(PartitionKey, event):
  # �}�C���X�gTBL�̓o�^
  # �`�[�Ǘ���
  userMyListAdminResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : event['Keys']['slipAdminUserId'],
      'mechanicId : event['Keys']['slipAdminMechanicId'],
      'officeId' : event['Keys']['slipAdminOfficeId'],
      'serviceType' : event['Keys']['targetService'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : event['Keys']['serviceTitle'],
      'category' : '17',
      'message' : 'TRAN_COMP',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : NONE,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')

    }
  )
  
  if userMyListAdminResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListAdminResponse)
  else:
    print('Post Successed.')



# ����˗��҂̃}�C���X�g�̍X�V
def put_requestMyList(PartitionKey, event):
  userMyListResponse = userMyList.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : event['Keys']['slipAdminUserId'],
      'mechanicId : event['Keys']['slipAdminMechanicId'],
      'officeId' : event['Keys']['slipAdminOfficeId'],
      'serviceType' : event['Keys']['targetService'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : event['Keys']['serviceTitle'],
      'category' : '21',
      'message' : 'EVALUATION_REQ',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'requestInfo' : NONE,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')

    }
  )
  
  if userMyListResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListResponse)
  else:
    print('Post Successed.')
	return


# �`�[�ԍ��ɕR�Â����[�U�[�}�C���X�gTBL���擾
def mylist_slipNo_query(partitionKey):
    queryData = userMyList.query(
        IndexName = 'slipNo-index',
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:
    if OperationType == 'TRANSACTIONEND':
      PartitionKey = event['Keys']['id']
      PartitionKey = id

    post_transaction(PartitionKey, event)
    put_adminMyList(PartitionKey, event)

    # ������̃}�C���X�g�����擾
    requestMyList = mylist_slipNo_query( event['Keys']['slipNo'])

    for item in requestMyList :
      # �Ǘ����[�U�[�ȊO�i�˗��ҁj�̃X�e�[�^�X�X�V
      if adminUser != item['requestId'] :
        if confirmUser != item['requestId'] :
          put_requestMyList(item)
        elif confirmUser == item['requestId'] :
          put_adminMyList(item)

      return post_product(PartitionKey, event)

  except Exception as e:
      print("Error Exception.")
      print(e)