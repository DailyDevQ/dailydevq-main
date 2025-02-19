# backend/functions/email_sender/handler.py

import boto3


def lambda_handler(event, context):
    ses_client = boto3.client("ses")
    response = ses_client.send_email(
        Source="no-reply@example.com",
        Destination={"ToAddresses": [event["to_email"]]},
        Message={
            "Subject": {"Data": event["subject"]},
            "Body": {"Text": {"Data": event["body"]}},
        },
    )
    return {"statusCode": 200, "body": response["MessageId"]}
