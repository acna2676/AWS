import json
import boto3  

sqs = boto3.client('sqs')
queue_url = 'https://sqs.ap-northeast-1.amazonaws.com/197052146621/ikkyu-20a'
dlq_url = 'https://sqs.ap-northeast-1.amazonaws.com/197052146621/ikkyu-20a-DLQ'

def lambda_handler(event, context):
    print(event)
    # records = event['Records']
    # for record in records:
    
    while True:  
        response = sqs.receive_message(
        QueueUrl=dlq_url,
        MaxNumberOfMessages=10,
        )
        # print(len(response['Messages']))
        print(response)
        if response.get('Messages') is None:
            break 
        
        for i in range(len(response['Messages'])):
            print('response = ', response)
            message = response['Messages'][i]
            print('message = ', message)
            body = message['Body']
            print('body = ', body)
            
            # sqs.send_message(
            #     QueueUrl=queue_url,
            #     MessageBody=body)
            # # TODO implement
            
            # メッセージを削除するための情報を取得
            receipt_handle = message['ReceiptHandle']
            
            # メッセージを削除
            sqs.delete_message(
                QueueUrl=dlq_url,
                ReceiptHandle=receipt_handle
            )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
