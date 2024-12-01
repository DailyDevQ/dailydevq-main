# ./backend/functions/user_service.py

import boto3
import uuid
import os
from datetime import datetime
from botocore.exceptions import ClientError

# DynamoDB 클라이언트 생성
dynamodb = boto3.resource(
    "dynamodb", 
    region_name="ap-northeast-2",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
users_table = dynamodb.Table("Users")  # 테이블 이름 확인

def save_user(email, name, profile_url, login_type):
    """
    DynamoDB에 사용자 정보를 저장합니다.
    중복된 이메일이 있으면 새로운 데이터로 업데이트합니다.
    """
    # 중복 확인
    existing_user = get_user_by_email(email)
    timestamp = datetime.utcnow().isoformat()

    if existing_user:
        # 사용자 정보 업데이트
        try:
            users_table.update_item(
                Key={"id": existing_user["id"]},
                UpdateExpression=(
                    "SET #name = :name, profile_url = :profile_url, "
                    "login_type = :login_type, updated_at = :updated_at"
                ),
                ExpressionAttributeNames={"#name": "name"},
                ExpressionAttributeValues={
                    ":name": name,
                    ":profile_url": profile_url,
                    ":login_type": login_type,
                    ":updated_at": timestamp,
                },
            )
            print(f"사용자 {email} 정보가 업데이트되었습니다.")
        except ClientError as e:
            print(f"사용자 정보를 업데이트하는 중 오류가 발생했습니다: {e}")
            raise
    else:
        # 새 사용자 저장
        user_id = str(uuid.uuid4())
        user_data = {
            "id": user_id,
            "email": email,
            "name": name or "Unknown",  # 이름 누락 시 기본값 설정,
            "profile_url": profile_url or "",
            "login_type": login_type,
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        try:
            users_table.put_item(Item=user_data)
            print(f"사용자 {email} 정보가 저장되었습니다.")
        except Exception as e:
            print(f"사용자 정보를 저장하는 중 오류가 발생했습니다: {e}")
            raise

        return user_data

def get_user_from_db(user_id):
    """
    DynamoDB에서 사용자 정보를 검색합니다.
    :param user_id: 검색할 사용자 ID
    :return: 사용자 정보 딕셔너리 또는 None
    """
    try:
        response = users_table.get_item(Key={"id": user_id})
        return response.get("Item")  # 사용자 정보 반환
    except Exception as e:
        print(f"사용자 정보를 검색하는 중 오류가 발생했습니다: {e}")
        return None


def get_user_by_email(email):
    try:
        print(f"요청된 이메일: {email}")  # 요청된 이메일 출력
        response = users_table.query(
            IndexName="email-index",
            KeyConditionExpression="email = :email",
            ExpressionAttributeValues={":email": email},
        )
        items = response.get("Items", [])
        if not items:
            return None
        # 최신 데이터를 반환
        sorted_items = sorted(items, key=lambda x: x["updated_at"], reverse=True)
        return sorted_items[0]  # 가장 최근 항목 반환
    except ClientError as e:
        print(f"사용자 정보를 검색하는 중 오류가 발생했습니다: {e}")
        return None


def get_user_by_id(user_id):
    """
    사용자 ID를 기준으로 사용자 정보를 검색합니다.
    """
    try:
        response = users_table.get_item(Key={"id": user_id})
        return response.get("Item")  # 사용자 정보 반환
    except ClientError as e:
        print(f"사용자 정보를 검색하는 중 오류가 발생했습니다: {e}")
        return None

def delete_user(user_id):
    """
    사용자 ID를 기준으로 사용자 정보를 삭제합니다.
    """
    try:
        users_table.delete_item(Key={"id": user_id})
        print(f"사용자 ID {user_id} 정보가 삭제되었습니다.")
    except ClientError as e:
        print(f"사용자 정보를 삭제하는 중 오류가 발생했습니다: {e}")
        raise