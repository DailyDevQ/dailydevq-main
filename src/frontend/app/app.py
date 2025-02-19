# ./frontend/app/app.py

# =========================================================================================
# Imports and Setup (임포트와 기본 설정)
#  - 필요한 라이브러리와 모듈을 불러오고, 플라스크와 관련된 환경을 초기화하는 코드 섹션입니다.
#  - Import necessary libraries and modules, initialize Flask and environment variables.
# =========================================================================================

from flask import Flask, render_template, redirect, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    current_user,
)
from dotenv import load_dotenv
import os
import requests

# 프로젝트 내부에서 만든 DynamoDB 관련 함수 임포트
# Import custom functions for interacting with DynamoDB
from backend.functions.user_service import save_user, get_user_from_db

# Flask 애플리케이션의 Blueprint 임포트
# Import the main Blueprint containing application routes
from frontend.app.routes import bp as main_bp

# .env 파일 로드
# Load environment variables from the .env file
load_dotenv()

# =========================================================================================
# Flask Application Initialization (플라스크 애플리케이션 초기화)
#  - Flask 인스턴스를 생성하고, 세션 암호화와 쿠키 설정을 구성합니다.
#  - Create the Flask app instance, configure session encryption and cookies.
# =========================================================================================

app = Flask(__name__)

# 세션 관리를 위한 비밀키 설정
# Set a secret key for secure session management
app.secret_key = os.getenv("SECRET_KEY")

# 세션 쿠키 설정 (HTTPS 환경에서 SESSION_COOKIE_SECURE=True 권장)
# Configure session cookies (SESSION_COOKIE_SECURE=True is recommended for HTTPS)
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# =========================================================================================
# Flask-Login Configuration (Flask-Login 설정)
#  - 사용자의 인증 상태를 관리하고, 로그인 관련 기능을 지원합니다.
#  - Manage user authentication status and provide login features.
# =========================================================================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = (
    None  # 기본 로그인 뷰 사용 안 함 / Disable the default login view
)


# Flask-Login용 사용자 모델 정의
# Define a user model class for Flask-Login
class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email


# 로그인된 사용자 로드 함수
# This function loads a user from the database using email as an identifier
@login_manager.user_loader
def load_user(email):
    user_data = get_user_from_db(email)
    if user_data:
        return User(
            id=user_data["email"], name=user_data.get("name"), email=user_data["email"]
        )
    return None


# Blueprint 등록
# Register the main Blueprint with the Flask app
app.register_blueprint(main_bp, url_prefix="/")

# =========================================================================================
# Environment Variable Utility (환경 변수 유틸리티 함수)
#  - 주어진 이름의 환경 변수를 가져오고, 설정되지 않았다면 예외를 발생시킵니다.
#  - Retrieve an environment variable; raise an error if it's not set.
# =========================================================================================


def get_env_var(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"환경 변수 {name}이(가) 설정되지 않았습니다.")
    return value


# =========================================================================================
# DynamoDB: User Retrieval (DynamoDB에서 사용자 검색)
#  - 이메일을 이용해 DynamoDB 테이블에서 사용자를 조회하는 로직을 담고 있습니다.
#  - Use email as a key to retrieve user data from the 'Users' table in DynamoDB.
# =========================================================================================


"""def get_user_from_db(email):
    import boto3

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Users")  # 실제 DynamoDB 테이블 이름과 일치해야 합니다.
    try:
        # 이메일을 기준으로 테이블에서 스캔
        # Scan the table for the item with the matching email
        response = table.scan(
            FilterExpression="email = :email",
            ExpressionAttributeValues={":email": email},
        )
        items = response.get("Items")
        if items:
            return items[0]  # 첫 번째 매칭된 결과 반환 / Return the first matched item
        return None
    except Exception as e:
        print(f"DynamoDB 오류: {e}")
        return None
"""

# =========================================================================================
# OAuth Client Settings (OAuth 클라이언트 설정)
#  - 구글, 깃허브, 카카오, 네이버 등 OAuth 인증에 필요한 클라이언트 ID, 시크릿, 리다이렉트 URI를 가져옵니다.
#  - Retrieve OAuth settings from environment variables for Google, GitHub, Kakao, and Naver.
# =========================================================================================

GOOGLE_CLIENT_ID = get_env_var("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = get_env_var("GOOGLE_CLIENT_SECRET")
GITHUB_CLIENT_ID = get_env_var("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = get_env_var("GITHUB_CLIENT_SECRET")
KAKAO_CLIENT_ID = get_env_var("KAKAO_CLIENT_ID")
NAVER_CLIENT_ID = get_env_var("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = get_env_var("NAVER_CLIENT_SECRET")

GOOGLE_REDIRECT_URI = get_env_var("GOOGLE_REDIRECT_URI")
GITHUB_REDIRECT_URI = get_env_var("GITHUB_REDIRECT_URI")
KAKAO_REDIRECT_URI = get_env_var("KAKAO_REDIRECT_URI")
NAVER_REDIRECT_URI = get_env_var("NAVER_REDIRECT_URI")

# =========================================================================================
# User Information Handling (사용자 정보 처리)
#  - OAuth 인증 과정에서 받은 사용자 정보를 데이터베이스에 저장하고 세션에 로그인하는 로직을 포함합니다.
#  - Store the user info retrieved from the OAuth flow to the database and log them in.
# =========================================================================================


def save_user_info(email, name, profile_url, provider):
    """
    사용자가 DB에 존재하지 않으면 저장하고, Flask-Login을 통해 로그인 처리합니다.
    If the user does not exist in the DB, save it, then log in with Flask-Login.
    """
    if not email:
        raise RuntimeError(f"{provider}에서 이메일을 가져올 수 없습니다.")

    existing_user = get_user_from_db(email)
    if not existing_user:
        save_user(email, name, profile_url, provider)

    user = User(id=email, name=name, email=email)
    login_user(user)


def fetch_user_info(token_url, token_data, user_info_url, headers=None):
    """
    토큰을 발급받고(access token), 해당 토큰으로 사용자 정보를 조회하는 공통 함수입니다.
    1) token_url로 액세스 토큰 요청
    2) user_info_url로 사용자 정보 요청
    Common function that obtains an access token and then fetches user info.
    1) Request an access token from token_url
    2) Use the token to request user info from user_info_url
    """
    try:
        # 액세스 토큰 요청 / Obtain access token
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        access_token = token_response.json().get("access_token")

        # 사용자 정보 요청 / Request user info
        user_info_response = requests.get(
            user_info_url,
            headers={**(headers or {}), "Authorization": f"Bearer {access_token}"},
        )
        user_info_response.raise_for_status()
        return user_info_response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"OAuth 인증 중 오류가 발생했습니다: {e}")


# =========================================================================================
# Routes (라우트)
#  - Flask 애플리케이션에서 처리할 URL 경로와 함수를 정의합니다.
#  - Define the URL endpoints and their corresponding functions.
# =========================================================================================


# 메인 페이지: 로그인 화면을 렌더링
# Main page: renders the login template
@app.route("/")
def index():
    return render_template("login.html")


# 대시보드: 로그인된 사용자만 접근 가능
# Dashboard: accessible only for logged-in users
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


# =========================================================================================
# Google OAuth Flow
# =========================================================================================


@app.route("/login/google")
def login_google():
    """
    구글 인증 페이지로 리다이렉트합니다.
    Redirect user to Google's OAuth consent screen.
    """
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        "response_type=code&"
        "scope=email"
    )
    return redirect(google_auth_url)


@app.route("/login/google/callback")
def google_callback():
    """
    구글 OAuth 콜백 처리:
    1) 액세스 토큰 발급
    2) 사용자 정보 불러오기
    3) 사용자 정보 저장 및 로그인
    Handle Google's OAuth callback:
    1) Get an access token
    2) Fetch user info
    3) Save user info and log in
    """
    code = request.args.get("code")
    if not code:
        return "Google 인증 실패: 인증 코드를 찾을 수 없습니다.", 400

    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        user_info = fetch_user_info(
            token_url="https://oauth2.googleapis.com/token",
            token_data=token_data,
            user_info_url="https://www.googleapis.com/oauth2/v2/userinfo",
        )
    except RuntimeError as e:
        return str(e), 500

    email = user_info.get("email")
    if not email:
        return "Google 인증 실패: 이메일 정보가 없습니다.", 400

    save_user_info(email, user_info.get("name"), user_info.get("picture"), "Google")
    return redirect(url_for("main.dashboard"))


# =========================================================================================
# GitHub OAuth Flow
# =========================================================================================


@app.route("/login/github")
def login_github():
    """
    깃허브 인증 페이지로 리다이렉트합니다.
    Redirect user to GitHub's OAuth consent screen.
    """
    from urllib.parse import urlencode

    query_params = urlencode(
        {
            "client_id": GITHUB_CLIENT_ID,
            "redirect_uri": GITHUB_REDIRECT_URI,
            "scope": "user:email",
        }
    )
    github_auth_url = f"https://github.com/login/oauth/authorize?{query_params}"
    return redirect(github_auth_url)


@app.route("/login/github/callback")
def github_callback():
    """
    깃허브 OAuth 콜백 처리:
    1) 액세스 토큰 발급
    2) 사용자 정보 불러오기
    3) 사용자 정보 저장 및 로그인
    Handle GitHub's OAuth callback:
    1) Get an access token
    2) Fetch user info
    3) Save user info and log in
    """
    code = request.args.get("code")
    if not code:
        return "GitHub 인증 실패: code가 없습니다.", 400

    # 액세스 토큰 요청 / Request an access token
    token_url = "https://github.com/login/oauth/access_token"
    token_data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GITHUB_REDIRECT_URI,
    }
    token_headers = {"Accept": "application/json"}

    try:
        token_response = requests.post(
            token_url, data=token_data, headers=token_headers
        )
        token_response.raise_for_status()
        token_json = token_response.json()
    except requests.RequestException as e:
        return f"GitHub 인증 실패: {e}", 500

    access_token = token_json.get("access_token")
    if not access_token:
        return f"GitHub 인증 실패: {token_json}", 500

    # 깃허브 사용자 정보 요청 / Retrieve GitHub user information
    user_info_url = "https://api.github.com/user"
    try:
        user_info_response = requests.get(
            user_info_url, headers={"Authorization": f"token {access_token}"}
        )
        user_info_response.raise_for_status()
        user_info = user_info_response.json()
    except requests.RequestException as e:
        return f"GitHub 사용자 정보 요청 실패: {e}", 500

    # 이메일 가져오기 / Fetch email
    email = user_info.get("email")
    if not email:
        emails_url = "https://api.github.com/user/emails"
        try:
            emails_response = requests.get(
                emails_url, headers={"Authorization": f"token {access_token}"}
            )
            emails_response.raise_for_status()
            emails = emails_response.json()
            for e in emails:
                if e.get("primary") and e.get("verified"):
                    email = e.get("email")
                    break
        except requests.RequestException as e:
            return f"GitHub 이메일 요청 실패: {e}", 500

    if not email:
        return "GitHub 인증 실패: 이메일을 가져올 수 없습니다.", 400

    # 사용자 정보 저장 / Save user info
    try:
        save_user_info(
            email=email,
            name=user_info.get("name", "Unknown"),
            profile_url=user_info.get("avatar_url", ""),
            provider="GitHub",
        )
    except Exception as e:
        return f"GitHub 인증 실패: 사용자 정보 저장 중 오류 발생. 상세: {e}", 500

    # 사용자 객체 생성 및 로그인 / Create user object and log in
    user = User(id=email, name=user_info.get("name", "Unknown"), email=email)
    login_user(user)

    return redirect(url_for("main.dashboard"))


# =========================================================================================
# Kakao OAuth Flow
# =========================================================================================


@app.route("/login/kakao")
def login_kakao():
    """
    카카오 인증 페이지로 리다이렉트합니다.
    Redirect user to Kakao's OAuth consent screen.
    """
    kakao_auth_url = (
        "https://kauth.kakao.com/oauth/authorize?"
        f"client_id={KAKAO_CLIENT_ID}&"
        f"redirect_uri={KAKAO_REDIRECT_URI}&"
        "response_type=code"
    )
    return redirect(kakao_auth_url)


@app.route("/login/kakao/callback")
def kakao_callback():
    """
    카카오 OAuth 콜백 처리:
    1) 액세스 토큰 발급
    2) 사용자 정보 불러오기
    3) 사용자 정보 저장 및 로그인
    Handle Kakao's OAuth callback:
    1) Get an access token
    2) Fetch user info
    3) Save user info and log in
    """
    code = request.args.get("code")
    token_data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
    }

    try:
        user_info = fetch_user_info(
            token_url="https://kauth.kakao.com/oauth/token",
            token_data=token_data,
            user_info_url="https://kapi.kakao.com/v2/user/me",
        )
    except RuntimeError as e:
        return str(e), 500

    kakao_account = user_info.get("kakao_account", {})
    email = kakao_account.get("email")
    if not email:
        return "Kakao 인증 실패: 이메일 정보가 없습니다.", 400

    save_user_info(
        email=email,
        name=user_info.get("properties", {}).get("nickname"),
        profile_url=user_info.get("properties", {}).get("profile_image"),
        provider="Kakao",
    )

    user = User(
        id=email, name=user_info.get("properties", {}).get("nickname"), email=email
    )
    login_user(user)

    return redirect(url_for("main.dashboard"))


# =========================================================================================
# Naver OAuth Flow
# =========================================================================================


@app.route("/login/naver")
def login_naver():
    """
    네이버 인증 페이지로 리다이렉트합니다. (CSRF 방지를 위해 state 사용)
    Redirect user to Naver's OAuth consent screen using a random state for CSRF protection.
    """
    state = "RANDOM_STATE_STRING"
    naver_auth_url = (
        "https://nid.naver.com/oauth2.0/authorize?"
        f"response_type=code&"
        f"client_id={NAVER_CLIENT_ID}&"
        f"redirect_uri={NAVER_REDIRECT_URI}&"
        f"state={state}"
    )
    return redirect(naver_auth_url)


@app.route("/login/naver/callback")
def naver_callback():
    """
    네이버 OAuth 콜백 처리:
    1) 액세스 토큰 발급
    2) 사용자 정보 불러오기
    3) 사용자 정보 저장 및 로그인
    Handle Naver's OAuth callback:
    1) Get an access token
    2) Fetch user info
    3) Save user info and log in
    """
    code = request.args.get("code")
    state = request.args.get("state")
    token_data = {
        "grant_type": "authorization_code",
        "client_id": NAVER_CLIENT_ID,
        "client_secret": NAVER_CLIENT_SECRET,
        "code": code,
        "state": state,
    }

    try:
        user_info = fetch_user_info(
            token_url="https://nid.naver.com/oauth2.0/token",
            token_data=token_data,
            user_info_url="https://openapi.naver.com/v1/nid/me",
        )
    except RuntimeError as e:
        return str(e), 500

    response = user_info.get("response", {})
    email = response.get("email")
    if not email:
        return "Naver 인증 실패: 이메일 정보가 없습니다.", 400

    save_user_info(
        email=email,
        name=response.get("name"),
        profile_url=response.get("profile_image"),
        provider="Naver",
    )

    return redirect(url_for("main.dashboard"))


# =========================================================================================
# Main Application Execution (메인 애플리케이션 실행)
# =========================================================================================

if __name__ == "__main__":
    # URL 매핑 구조를 출력 (디버깅용)
    # Print the URL map (for debugging)
    print(app.url_map)

    # FLASK_DEBUG 환경 변수를 확인하여 디버그 모드 설정
    # Set debug mode based on FLASK_DEBUG environment variable
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
