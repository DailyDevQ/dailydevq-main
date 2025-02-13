# backend/functions/email_sender/handler.py
def lambda_handler(event, context):
    # 이메일 발송 로직
    return {
        'statusCode': 200,
        'body': 'Email sent successfully'
    }