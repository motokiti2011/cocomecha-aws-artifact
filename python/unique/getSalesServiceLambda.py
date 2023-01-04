import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table("salesServiceInfo")

def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("slipNo").eq(partitionKey) & Key("deleteDiv").eq("0")
    )
    items=queryData['Items']
    print(items)
    return items

def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  OperationType = event['OperationType']

  try:
    if OperationType == 'GETSALESSERVICE':
      PartitionKey = event['Keys']['slipNo']
      return operation_query(PartitionKey)


  except Exception as e:
      print("Error Exception.")
      print(e)