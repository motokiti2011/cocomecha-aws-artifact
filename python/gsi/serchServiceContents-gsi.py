import json
import boto3

from boto3.dynamodb.conditions import Key, Attr
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("salesServiceInfo")

# �n��1���� areaNo1-index
def areaNo1_query(event):

    # ���������쐬
    serchFilter = createFilter(event)
    print('serchFilter')
    print(serchFilter)

    if serchFilter != '' :
      options = {
        'IndexName' : 'areaNo1-index',
        'KeyConditionExpression': Key("areaNo1").eq(event['Keys']['area1']),
        'FilterExpression': createFilter(event),
      }
    else :
      options = {
        'IndexName' : 'areaNo1-index',
        'KeyConditionExpression': Key("areaNo1").eq(event['Keys']['area1']),
      }
    
    print('options:')
    print( options)
    queryData = table.query(**options)
    items=queryData['Items']
    print(items)
    return items


# �n��1.2���R�[�h���� areaNo1AndAreaNo2-index
def areaNo1AndAreaNo2_query(event):

    # ���������쐬
    serchFilter = createFilter(event)
    print('serchFilter')
    print(serchFilter)
    
    if serchFilter != '' :
      options = {
        'IndexName' : 'areaNo1AndAreaNo2-index',
        'KeyConditionExpression': Key("areaNo1").eq(event['Keys']['area1']) & Key("areaNo2").eq(event['Keys']['area2']),
        'FilterExpression': createFilter(event),
      }
    else :
      options = {
        'IndexName' : 'areaNo1AndAreaNo2-index',
        'KeyConditionExpression': Key("areaNo1").eq(event['Keys']['area1']) & Key("areaNo2").eq(event['Keys']['area2']),
      }

    print('options:')
    print( options)
    queryData = table.query(**options)
    items=queryData['Items']
    print(items)
    return items


# ���������쐬
def createFilter(event):

    # ���������쐬
    area2 = event['Keys']['area2']
    category = event['Keys']['category']
    amount1 = event['Keys']['amount1']
    amount2 = event['Keys']['amount2']
    amountSerchDiv = event['Keys']['amountSerchDiv']

    # ���̑������������Ȃ�
    if category == '0' and amountSerchDiv == True :
      print('1')
      return ''
    # �J�e�S���[�̂�
    if category != '0' and amountSerchDiv == True :
      print('2')
      return Attr('category').eq(category)
    # ���z�̂�
    if category == '0' and amountSerchDiv == False :
      print('3')
      return Attr('amount').GE(amount1) & Attr('amount').LE(amount2)
    # �J�e�S���[,���z
    if category != '0' and amountSerchDiv == False :
      print('4')
      return Attr('category').eq(category) & Attr('amount').GE(amount1) & Attr('amount').LE(amount2)
    # �J�e�S���[,���z
    print('5')
    return ''


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        # �C���f�b�N�X�^�C�v�`�F�b�N
        if IndexType == 'SERCH-SLIP-INDEX':
            area2 = event['Keys']['area2']
            # �����l�u�G���A2�̃`�F�b�N�v
            if area2 == 0:
                return areaNo1_query(event)
            else:
                return areaNo1AndAreaNo2_query(event)
        else:
          return 500



    except Exception as e:
        print("Error Exception.")
        print(e)