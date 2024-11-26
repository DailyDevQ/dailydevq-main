# ./frontend/app/app.py

from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user  # 수정됨
from dotenv import load_dotenv
import os
import requests
from backend.functions.user_service import save_user, get_user_from_db  # 수정됨
from frontend.app.routes import bp as main_bp


# .env 파일 로드
load_dotenv()

# Flask 앱 초기화
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

# LoginManager 초기화
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_google'  # 수정됨: 보호된 페이지 접근 시 리다이렉트 경로 설정

# 사용자 클래스 정의
class User(UserMixin):  # 수정됨: Flask-Login 사용자 모델 정의
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

# 사용자 로드 함수
@login_manager.user_loader  # 수정됨: Flask-Login 사용자 로드 함수
def load_user(user_id):
    """
    사용자 ID를 기반으로 DynamoDB에서 사용자 정보를 로드합니다.
    """
    user_data = get_user_from_db(user_id)  # DynamoDB에서 사용자 정보 검색
    if user_data:
        return User(user_data['id'], user_data['name'], user_data['email'])
    return None

# Blueprint 등록
app.register_blueprint(main_bp, url_prefix='/')  # 수정됨: 'main' Blueprint 등록

# 환경 변수 가져오기 함수
def get_env_var(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"환경 변수 {name}이(가) 설정되지 않았습니다.")
    return value

# DynamoDB 사용자 검색 함수
def get_user_from_db(user_id):  # 수정됨: DynamoDB에서 사용자 정보를 가져오는 함수 추가
    import boto3
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')  # DynamoDB 테이블 이름
    try:
        response = table.get_item(Key={'id': user_id})
        return response.get('Item')
    except Exception as e:
        print(f"DynamoDB 오류: {e}")
        return None

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
def save_user_info(email, name, profile_url, provider):  # 수정됨: 중복 확인 및 로그인 추가
    if not email:
        raise RuntimeError(f"{provider}에서 이메일을 가져올 수 없습니다.")

    # DynamoDB에서 사용자 중복 확인
    existing_user = get_user_from_db(email)
    if not existing_user:
        save_user(email, name, profile_url, provider)

    # 사용자 객체 생성 및 세션 로그인
    user = User(id=email, name=name, email=email)
    login_user(user)

# 공통 함수: 사용자 정보 요청
def fetch_user_info(token_url, token_data, user_info_url, headers=None):
    try:
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        access_token = token_response.json().get('access_token')

        user_info_response = requests.get(
            user_info_url,
            headers={**(headers or {}), 'Authorization': f'Bearer {access_token}'}
        )
        user_info_response.raise_for_status()
        return user_info_response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"OAuth 인증 중 오류가 발생했습니다: {e}")

# 라우트 정의
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required  # 수정됨: 로그인 보호 적용
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Google 로그인 API
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
    if not code:
        return "Google 인증 실패: 인증 코드를 찾을 수 없습니다.", 400

    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    try:
        user_info = fetch_user_info(
            token_url='https://oauth2.googleapis.com/token',
            token_data=token_data,
            user_info_url='https://www.googleapis.com/oauth2/v2/userinfo'
        )
    except RuntimeError as e:
        return str(e), 500

    email = user_info.get('email')
    if not email:
        return "Google 인증 실패: 이메일 정보가 없습니다.", 400

    save_user_info(email, user_info.get('name'), user_info.get('picture'), "Google")
    return redirect(url_for('main.dashboard'))

# GitHub 로그인 API
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

    try:
        user_info = fetch_user_info(
            token_url='https://github.com/login/oauth/access_token',
            token_data=token_data,
            user_info_url='https://api.github.com/user',
            headers={'Accept': 'application/json'}
        )
    except RuntimeError as e:
        return str(e), 500

    email = user_info.get('email')
    if not email:
        return "GitHub 인증 실패: 이메일 정보가 없습니다.", 400

    save_user_info(email, user_info.get('name'), user_info.get('avatar_url'), "GitHub")
    return redirect(url_for('main.dashboard'))

# Kakao 로그인 API
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

    try:
        user_info = fetch_user_info(
            token_url='https://kauth.kakao.com/oauth/token',
            token_data=token_data,
            user_info_url='https://kapi.kakao.com/v2/user/me'
        )
    except RuntimeError as e:
        return str(e), 500

    kakao_account = user_info.get('kakao_account', {})
    email = kakao_account.get('email')
    if not email:
        return "Kakao 인증 실패: 이메일 정보가 없습니다.", 400

    save_user_info(
        email=email,
        name=user_info.get('properties', {}).get('nickname'),
        profile_url=user_info.get('properties', {}).get('profile_image'),
        provider="Kakao"
    )
    return redirect(url_for('main.dashboard'))

# Naver 로그인 API
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

    try:
        user_info = fetch_user_info(
            token_url='https://nid.naver.com/oauth2.0/token',
            token_data=token_data,
            user_info_url='https://openapi.naver.com/v1/nid/me'
        )
    except RuntimeError as e:
        return str(e), 500

    response = user_info.get('response', {})
    email = response.get('email')
    if not email:
        return "Naver 인증 실패: 이메일 정보가 없습니다.", 400

    save_user_info(
        email=email,
        name=response.get('name'),
        profile_url=response.get('profile_image'),
        provider="Naver"
    )
    return redirect(url_for('main.dashboard'))

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true')
