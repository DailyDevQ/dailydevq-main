# frontend/app/app.py

from flask import Flask, render_template, redirect, request, session, url_for
import requests

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'

# Google OAuth 설정
GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'
GOOGLE_CLIENT_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'
GOOGLE_REDIRECT_URI = 'http://localhost:5000/login/google/callback'

# Kakao OAuth 설정
KAKAO_CLIENT_ID = 'YOUR_KAKAO_CLIENT_ID'
KAKAO_REDIRECT_URI = 'http://localhost:5000/login/kakao/callback'

# Naver OAuth 설정
NAVER_CLIENT_ID = 'YOUR_NAVER_CLIENT_ID'
NAVER_CLIENT_SECRET = 'YOUR_NAVER_CLIENT_SECRET'
NAVER_REDIRECT_URI = 'http://localhost:5000/login/naver/callback'

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
    return f'Google 로그인 성공: {email}'

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
    return f'Kakao 로그인 성공: {email}'

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
    return f'Naver 로그인 성공: {email}'

if __name__ == '__main__':
    app.run(debug=True)
