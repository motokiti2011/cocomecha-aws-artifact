import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
table = dynamodb.Table("slipDetailInfo")

# �n��1���� areaNo1-index
def areaNo1_query(event):

    # ���������쐬
    serchFilter = createFilter(event)

    queryData = table.query(
        IndexName = 'areaNo1-index',
        KeyConditionExpression = Key("areaNo1").eq(event['Keys']['areaNo1'])
        FilterExpression: serchFilter,
    )
    items=queryData['Items']
    print(items)
    return items


# �n��1.2���R�[�h���� areaNo1AndAreaNo2-index
def areaNo1AndAreaNo2_query(event):

    # ���������쐬
    serchFilter = createFilter(event)

    queryData = table.query(
        IndexName = 'areaNo1AndAreaNo2-index',
        KeyConditionExpression = Key("areaNo2").eq(event['Keys']['areaNo1']) & Key("areaNo2").eq(event['Keys']['areaNo2']),
        FilterExpression: serchFilter,
    )
    items=queryData['Items']
    print(items)
    return items


# ���������쐬
def createFilter(event):

    # ���������쐬
    area2 : event['Keys']['areaNo2']
    category : event['Keys']['category']
    amount1 : event['Keys']['amount1']
    amount2 : event['Keys']['amount2']
    amountSerchDiv : event['Keys']['amountSerchDiv']
    
    # ���̑������������Ȃ�
    if area2 == '0' && category == '0' && amountSerchDiv == false :
      return ''

    # �n��2���̂�
    if area2 != '0' && category == '0' && amountSerchDiv == false :
      return Attr('area2').eq(area2)

    # �J�e�S���[�̂�
    if area2 == '0' && category != '0' && amountSerchDiv == false :
      return Attr('category').eq(category)

    # ���z�̂�
    if area2 == '0' && category == '0' && amountSerchDiv == true :
      return Attr('amount').GE(amount1) & Attr('amount').LE(amount2)

    # �n��2,�J�e�S���[
    if area2 != '0' && category != '0' && amountSerchDiv == false :
      return Attr('area2').eq(area2) & Attr('category').eq(category)

    # �n��2,���z
    if area2 != '0' && category == '0' && amountSerchDiv == true :
      return Attr('area2').eq(area2) & Attr('amount').GE(amount1) & Attr('amount').LE(amount2)

    # �J�e�S���[,���z
    if area2 == '0' && category != '0' && amountSerchDiv == true :
      return Attr('category').eq(category) & Attr('amount').GE(amount1) & Attr('amount').LE(amount2)

    # �n��2,�J�e�S���[,���z
    if area2 == '0' && category != '0' && amountSerchDiv == true :
      return Attr('area2').eq(area2) & Attr('category').eq(category) & Attr('amount').GE(amount1) & Attr('amount').LE(amount2)

    return ''


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    try:

        # �C���f�b�N�X�^�C�v�`�F�b�N
        if IndexType == 'SERCH-SLIP-INDEX':
            area2 = event['Keys']['areaNo2']
            # �����l�u�G���A2�̃`�F�b�N�v
            if area2 == 0:
                return areaNo1_query(event)
            else:
                return areaNo1AndAreaNo2_query(event)
        elif:
          return 500



    except Exception as e:
        print("Error Exception.")
        print(e)