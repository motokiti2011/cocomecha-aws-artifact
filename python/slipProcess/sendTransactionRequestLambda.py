import json
import boto3
import uuid

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("serviceTransactionRequest")
table2 = dynamodb.Table("userMyList")


# ����˗�TBL���R�[�h�o�^
def post_product(PartitionKey, event):

  now = datetime.now()

  putResponse = table.put_item(
    Item={
      'id' : PartitionKey,
      'slipNo' : event['Keys']['slipNo'],
      'requestId' : event['Keys']['requestId'],
      'serviceUserType' : event['Keys']['serviceUserType'],
      'requestType' : event['Keys']['requestType'],
      'files' : event['Keys']['files'],
      'requestStatus' : event['Keys']['requestStatus'],
      'confirmDiv' : event['Keys']['confirmDiv'],
      'deadline' : event['Keys']['deadline'],
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
    return putResponse
  else:
    print('Post Successed.')




  # �}�C���X�gTBL�̓o�^
  # �`�[�Ǘ���
  userMyListAdminResponse = table2.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : event['Keys']['slipAdminUserId'],
      'mechanicId : event['Keys']['slipAdminMechanicId'],
      'officeId' : event['Keys']['slipAdminOfficeId'],
      'serviceType' : event['Keys']['targetService'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : event['Keys']['serviceTitle'],
      'category' : '7',
      'message' : '',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
      'deleteDiv' : '0',
      'created' : now.strftime('%x %X'),
      'updated' : now.strftime('%x %X')

    }
  )
  
  if userMyListAdminResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(userMyListAdminResponse)
  else:
    print('Post Successed.')


  # ����˗���
  userMyListResponse = table2.put_item(
    Item={
      'id' : str(uuid.uuid4()),
      'userId' : event['Keys']['slipAdminUserId'],
      'mechanicId : event['Keys']['slipAdminMechanicId'],
      'officeId' : event['Keys']['slipAdminOfficeId'],
      'serviceType' : event['Keys']['targetService'],
      'slipNo' : event['Keys']['slipNo'],
      'serviceTitle' : event['Keys']['serviceTitle'],
      'category' : '13',
      'message' : '',
      'readDiv' : '0',
      'messageDate' : now.strftime('%x %X'),
      'messageOrQuastionId' : '' ,
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


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:
    if OperationType == 'TRANSACTIONREQUEST':
      id = str(uuid.uuid4())
      PartitionKey = id
      return post_product(PartitionKey, event)


  except Exception as e:
      print("Error Exception.")
      print(e)