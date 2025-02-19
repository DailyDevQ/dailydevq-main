# ./src/tests/test_email_sender.py

import pytest
from unittest.mock import patch
from src.backend.functions.email_sender.handler import lambda_handler

@patch("boto3.client")
def test_lambda_handler(mock_boto_client):
    """Lambda 핸들러가 정상적으로 이메일을 발송하는지 테스트"""

    # Mock SES 클라이언트 설정
    mock_ses = mock_boto_client.return_value
    mock_ses.send_email.return_value = {"MessageId": "12345"}

    # 이벤트 객체 (예제)
    event = {
        "to_email": "test@example.com",
        "subject": "Test Subject",
        "body": "This is a test email."
    }

    response = lambda_handler(event, None)

    # 예상 결과 확인
    assert response["statusCode"] == 200
    assert response["body"] == "12345"

    # SES의 send_email 호출 여부 확인
    mock_ses.send_email.assert_called_once()
