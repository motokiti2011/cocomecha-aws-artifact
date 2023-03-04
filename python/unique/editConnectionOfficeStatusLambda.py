import json
import boto3

from boto3.dynamodb.conditions import Key
# Key�I�u�W�F�N�g�𗘗p�ł���悤�ɂ���

# Dynamodb�A�N�Z�X�̂��߂̃I�u�W�F�N�g�擾
dynamodb = boto3.resource('dynamodb')
# �w��e�[�u���̃A�N�Z�X�I�u�W�F�N�g�擾
officeInfo = dynamodb.Table("officeInfo")

# �֘A�H��X�e�[�^�X�ύXLambda
def lambda_handler(event, context) :
    print("Received event: " + json.dumps(event))
    IndexType = event['IndexType']
    adminOfficeId = office['adminOfficeId']
    connectionOffice = office['connectionOffice']

    try:
        # �����^�C�v����
        if IndexType != 'CONNECTIONOFFICESTATUS':
          return

        # �f�[�^�擾
        office = officeInfo_query(adminOfficeId)
        
        connectionData = office['connectionOfficeInfo']
        
        for item in connectionData  :
          if item['officeId'] == connectionOffice['officeId']
            # ���ʂ̊i�[
            result={
              'officeId' :connectionOffice['officeId'],
              'officeName' :connectionOffice['officeName'],
              'officeAssociationDiv' :connectionOffice['officeAssociationDiv'],
              'officeAssociation':connectionOffice['officeAssociation']
            }


        putResponse = officeInfo.put_item(
          Item={
            'officeId' : adminOfficeId,
            'officeName' : office['officeName'],
            'officeTel' : office['officeTel'],
            'officeMailAdress' : office['officeMailAdress'],
            'officeArea1' : office['officeArea1'],
            'officeArea' : office['officeArea'],
            'officeAdress' : office['officeAdress'],
            'officePostCode' : office['officePostCode'],
            'workContentList' : office['workContentList'],
            'businessHours' : office['businessHours'],
            'connectionOfficeInfo' : connectionData,
            'connectionMechanicInfo' : office['connectionMechanicInfo'],
            'adminSettingInfo' : office['adminSettingInfo'],
            'officePR' : office['officePR'],
            'officePRimageURL' : office['officePRimageURL'],
            'officeFormList' : office['officeFormList'],
            'publicInfo' : office['publicInfo'],
            'created' : office['created'],
            'updated' :  now.strftime('%x %X')
          }
        )
        
        if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
          print(putResponse)
        else:
          print('Post Successed.')
        return putResponse['ResponseMetadata']['HTTPStatusCode']


    except Exception as e:
        print("Error Exception.")
        print(e)


# �H���񌟍� officeInfo
def officeInfo_query(adminOfficeId) :
    queryData = officeInfo.query(
        KeyConditionExpression = Key("officeId").eq(adminOfficeId)
    )
    items=queryData['Items']
    print(items)
    return items[0]


