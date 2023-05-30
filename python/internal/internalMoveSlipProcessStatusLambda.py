import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
slipDetailInfo = dynamodb.Table("slipDetailInfo")
salesServiceInfo = dynamodb.Table("salesServiceInfo")
transactionSlip = dynamodb.Table("transactionSlip")
completionSlip = dynamodb.Table("completionSlip")


# 内部処理 引数に指定された操作で伝票の工程ステータス遷移処理を行う
def lambda_handler(event, context) :
  print("Received event: " + json.dumps(event))

  # 操作ステータス
  OperationStatus = event['OperationStatus']
  try:
    # 取引開始（ステータス0→1）
    if OperationStatus == 'StartTrading' :
      print('LABEL_1')
      startTramsaction(event)
    # 取引完了（ステータス1→2）
    elif OperationStatus == 'EndOfTransaction' :
      print('LABEL_2')
      endTransaction(event)

  except Exception as e:
      print("Error Exception.")
      print(e)



# 取引開始処理
def startTramsaction(event) :
  
  processStatus = '1'
  slipNo = event['slipNo']
  serviceType = event['serviceType']

  # 対象伝票のステータスを更新する
  slip = moveProcessStatus(slipNo, serviceType, processStatus)

  # 取引伝票情報を作成する
  postTransaction_query(slip)


# 取引完了処理
def endTransaction(event)

  processStatus = '1'
  slipNo = event['slipNo']
  serviceType = event['serviceType']

  # 対象伝票のステータスを更新する
  slip = moveProcessStatus(slipNo, serviceType, processStatus)

  # 取引伝票情報を論理削除する
  deleteTransaction_query(slip)

  # 完了済伝票情報を作成する
  postCompletionSlip(slip)



# 対象の伝票情報を取得
def moveProcessStatus(slipNo, serviceType, processStatus):

  if serviceType = '0' :
    slipDitailStatusMove_query(slipNo, processStatus)
  else :
    salesServiceStatusMove_query(slipNo, processStatus)


# 伝票情報のステータス操作
def slipDitailStatusMove_query(slipNo, processStatus) :
  


