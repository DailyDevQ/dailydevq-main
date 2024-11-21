# ./frontend/app/app.py

from flask import Flask, render_template, redirect, request, url_for
import os
from dotenv import load_dotenv
import requests
from backend.functions.user_service import save_user

# .env 파일 로드
load_dotenv()

# Flask 앱 초기화
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))  # 고정된 SECRET_KEY 설정

# 환경 변수 가져오기 함수
def get_env_var(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"환경 변수 {name}이(가) 설정되지 않았습니다.")
    return value

# OAuth 클라이언트 설정
GOOGLE_CLIENT_ID = get_env_var('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = get_env_var('GOOGLE_CLIENT_SECRET')
GITHUB_CLIENT_ID = get_env_var('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = get_env_var('GITHUB_CLIENT_SECRET')
KAKAO_CLIENT_ID = get_env_var('KAKAO_CLIENT_ID')
NAVER_CLIENT_ID = get_env_var('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = get_env_var('NAVER_CLIENT_SECRET')

# 리다이렉트 URI 설정
GOOGLE_REDIRECT_URI = get_env_var('GOOGLE_REDIRECT_URI')
GITHUB_REDIRECT_URI = get_env_var('GITHUB_REDIRECT_URI')
KAKAO_REDIRECT_URI = get_env_var('KAKAO_REDIRECT_URI')
NAVER_REDIRECT_URI = get_env_var('NAVER_REDIRECT_URI')

# 공통 함수: 사용자 정보 저장
def save_user_info(email, name, profile_url, provider):
    if not email:
        raise RuntimeError(f"{provider}에서 이메일을 가져올 수 없습니다.")
    save_user(email, name, profile_url, provider)

# 공통 함수: 사용자 정보 요청
def fetch_user_info(token_url, token_data, user_info_url, headers=None):
    token_response = requests.post(token_url, data=token_data)
    token_response.raise_for_status()
    access_token = token_response.json().get('access_token')

    user_info_response = requests.get(user_info_url, headers={**(headers or {}), 'Authorization': f'Bearer {access_token}'})
    user_info_response.raise_for_status()
    return user_info_response.json()

# 라우트 정의
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/google')
def login_google():
    google_auth_url = (
        'https://accounts.google.com/o/oauth2/v2/auth?'
        f'client_id={GOOGLE_CLIENT_ID}&'
        f'redirect_uri={GOOGLE_REDIRECT_URI}&'
        'response_type=code&'
        'scope=email'
    )
    return redirect(google_auth_url)

@app.route('/login/google/callback')
def google_callback():
    code = request.args.get('code')
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    user_info = fetch_user_info(
        token_url='https://oauth2.googleapis.com/token',
        token_data=token_data,
        user_info_url='https://www.googleapis.com/oauth2/v2/userinfo'
    )
    save_user_info(user_info.get('email'), user_info.get('name'), user_info.get('picture'), "Google")
    return f"Google 로그인 성공: {user_info.get('email')}"

@app.route('/login/github')
def login_github():
    github_auth_url = (
        'https://github.com/login/oauth/authorize?'
        f'client_id={GITHUB_CLIENT_ID}&'
        f'redirect_uri={GITHUB_REDIRECT_URI}&'
        'scope=user:email'
    )
    return redirect(github_auth_url)

@app.route('/login/github/callback')
def github_callback():
    code = request.args.get('code')
    token_data = {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': GITHUB_REDIRECT_URI
    }
    user_info = fetch_user_info(
        token_url='https://github.com/login/oauth/access_token',
        token_data=token_data,
        user_info_url='https://api.github.com/user',
        headers={'Accept': 'application/json'}
    )
    save_user_info(user_info.get('email'), user_info.get('name'), user_info.get('avatar_url'), "GitHub")
    return f"GitHub 로그인 성공: {user_info.get('email')}"

@app.route('/login/kakao')
def login_kakao():
    kakao_auth_url = (
        'https://kauth.kakao.com/oauth/authorize?'
        f'client_id={KAKAO_CLIENT_ID}&'
        f'redirect_uri={KAKAO_REDIRECT_URI}&'
        'response_type=code'
    )
    return redirect(kakao_auth_url)

@app.route('/login/kakao/callback')
def kakao_callback():
    code = request.args.get('code')
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_CLIENT_ID,
        'redirect_uri': KAKAO_REDIRECT_URI,
        'code': code
    }
    user_info = fetch_user_info(
        token_url='https://kauth.kakao.com/oauth/token',
        token_data=token_data,
        user_info_url='https://kapi.kakao.com/v2/user/me'
    )
    kakao_account = user_info.get('kakao_account', {})
    save_user_info(
        email=kakao_account.get('email'),
        name=user_info.get('properties', {}).get('nickname'),
        profile_url=user_info.get('properties', {}).get('profile_image'),
        provider="Kakao"
    )
    return f'Kakao 로그인 성공: {kakao_account.get("email")}'

@app.route('/login/naver')
def login_naver():
    state = 'RANDOM_STATE_STRING'
    naver_auth_url = (
        'https://nid.naver.com/oauth2.0/authorize?'
        f'response_type=code&'
        f'client_id={NAVER_CLIENT_ID}&'
        f'redirect_uri={NAVER_REDIRECT_URI}&'
        f'state={state}'
    )
    return redirect(naver_auth_url)

@app.route('/login/naver/callback')
def naver_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': NAVER_CLIENT_ID,
        'client_secret': NAVER_CLIENT_SECRET,
        'code': code,
        'state': state
    }
    user_info = fetch_user_info(
        token_url='https://nid.naver.com/oauth2.0/token',
        token_data=token_data,
        user_info_url='https://openapi.naver.com/v1/nid/me'
    )
    response = user_info.get('response', {})
    save_user_info(
        email=response.get('email'),
        name=response.get('name'),
        profile_url=response.get('profile_image'),
        provider="Naver"
    )
    return f'Naver 로그인 성공: {response.get("email")}'

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true')
