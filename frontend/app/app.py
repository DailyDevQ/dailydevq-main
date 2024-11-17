# ./frontend/app/app.py

from flask import Flask, render_template, redirect, request, url_for
import os
from dotenv import load_dotenv
import requests
from backend.functions.user_service import save_user

# .env 파일 로드
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 환경 변수에서 클라이언트 ID와 시크릿 키 가져오기
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
KAKAO_CLIENT_ID = os.getenv('KAKAO_CLIENT_ID')
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')

# 환경 변수에서 리디렉션 URI 가져오기
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')
GITHUB_REDIRECT_URI = os.getenv('GITHUB_REDIRECT_URI')
KAKAO_REDIRECT_URI = os.getenv('KAKAO_REDIRECT_URI')
NAVER_REDIRECT_URI = os.getenv('NAVER_REDIRECT_URI')


# 구글 API 로그인 라우트
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
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')
    user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    user_info_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
    user_info = user_info_response.json()
    email = user_info.get('email')
    # 사용자 데이터 저장
    save_user(email, user_info.get('name'), user_info.get('picture'), "Google")
    return f"Google 로그인 성공: {email}"

# 깃허브 API 로그인 라우트
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
    token_url = 'https://github.com/login/oauth/access_token'
    token_data = {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': GITHUB_REDIRECT_URI
    }
    token_headers = {'Accept': 'application/json'}
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    user_info_url = 'https://api.github.com/user'
    user_info_response = requests.get(user_info_url, headers={'Authorization': f'token {access_token}'})
    user_info = user_info_response.json()
    email = user_info.get('email')

    if email is None:
        # 이메일이 공개되지 않은 경우 추가 요청
        emails_url = 'https://api.github.com/user/emails'
        emails_response = requests.get(emails_url, headers={'Authorization': f'token {access_token}'})
        emails = emails_response.json()
        for e in emails:
            if e.get('primary') and e.get('verified'):
                email = e.get('email')
                break

    # 사용자 데이터 저장
    save_user(email, user_info.get('name'), user_info.get('avatar_url'), "GitHub")
    return f"GitHub 로그인 성공: {email}"

# 카카오 API 로그인 라우트
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
    token_url = 'https://kauth.kakao.com/oauth/token'
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_CLIENT_ID,
        'redirect_uri': KAKAO_REDIRECT_URI,
        'code': code
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    user_info_url = 'https://kapi.kakao.com/v2/user/me'
    user_info_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
    user_info = user_info_response.json()

    email = user_info.get('kakao_account', {}).get('email')
    name = user_info.get('properties', {}).get('nickname')
    profile_url = user_info.get('properties', {}).get('profile_image')

    # 사용자 정보 저장
    save_user(email, name, profile_url, "Kakao")
    return f'Kakao 로그인 성공: {email}'


# 네이버 API 로그인 라우트
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
    token_url = 'https://nid.naver.com/oauth2.0/token'
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': NAVER_CLIENT_ID,
        'client_secret': NAVER_CLIENT_SECRET,
        'code': code,
        'state': state
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    user_info_url = 'https://openapi.naver.com/v1/nid/me'
    user_info_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
    user_info = user_info_response.json()

    email = user_info.get('response', {}).get('email')
    name = user_info.get('response', {}).get('name')
    profile_url = user_info.get('response', {}).get('profile_image')

    # 사용자 정보 저장
    save_user(email, name, profile_url, "Naver")
    return f'Naver 로그인 성공: {email}'


if __name__ == '__main__':
    app.run(debug=True)
