# ./backend/functions/user_service.py

import boto3
import uuid
from datetime import datetime

# DynamoDB 클라이언트 생성
dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
users_table = dynamodb.Table("Users")  # 테이블 이름 확인

def save_user(email, name, profile_url, login_type):
    user_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    user_data = {
        "id": user_id,
        "email": email,
        "name": name,
        "profile_url": profile_url,
        "login_type": login_type,
        "created_at": timestamp,
        "updated_at": timestamp,
    }

    try:
        # DynamoDB에 데이터 저장
        users_table.put_item(Item=user_data)
        print(f"사용자 {email} 정보가 저장되었습니다.")
    except Exception as e:
        print(f"사용자 정보를 저장하는 중 오류가 발생했습니다: {e}")
        raise

    return user_data
