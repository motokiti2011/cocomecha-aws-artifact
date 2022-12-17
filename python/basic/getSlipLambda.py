import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table("slipDetailInfo")

def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return queryData

def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  OperationType = event['OperationType']

  try:
    if OperationType == 'GETSLIP':
      PartitionKey = event['Keys']['slipNo']
      return operation_query(PartitionKey)


  except Exception as e:
      print("Error Exception.")
      print(e)