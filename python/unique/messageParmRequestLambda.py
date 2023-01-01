import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("slipMegPrmUser")


# ���R�[�h����
def post_product(partitionKey, updateId, updateName):
    # �Ώۃ��R�[�h�擾
    queryData = table.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']

    if len(items) == 0:
      # �擾�ł��Ȃ������ꍇ
      return False

    item = items[0]

    # ���σ��[�U�[���X�g���擾
    userList = item['permissionUserList']
    data = {'userId':updateId ,'userName':updateName, 'parmissionDiv': '0'}
    # ���σ��[�U�[���X�g����̏ꍇ
    if len(userList) == 0:
      userList.append(data)
     
    else:
      inListDiv = True
      count = 0
      target = 0
      for list in userList:
        if(list['userId'] == updateId):
          # ���X�g�ɂ��łɊ܂܂��ꍇ,�\���������Ƃ��č폜
          inListDiv = False
          target = count
        count += 1
            

      if(inListDiv):
        userList.append(data)
      else:
        userList.pop(target)
        

    # ���R�[�h�X�V
    putResponse = table.put_item(
      Item={
        'slipNo' : PartitionKey,
        'slipAdminUserId' : item['slipAdminUserId'],
        'slipAdminUserName' : item['slipAdminUserName'],
        'permissionUserList' : userList,
        'created' : item['created'],
        'updated' : datetime.now()
      }
    )
  
    if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
      print(putResponse)
    else:
      print('Post Successed.')
    return putResponse
  


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:

    if OperationType == 'MESSAGEREQ':
      PartitionKey = event['Keys']['slipNo']
      updateId = event['Keys']['userId']
      updateName = event['Keys']['userName']
      return post_product(PartitionKey, updateId, updateName)


  except Exception as e:
      print("Error Exception.")
      print(e)