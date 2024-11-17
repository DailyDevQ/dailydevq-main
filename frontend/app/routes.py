# frontend/app/routes.py

from flask import Blueprint, render_template

# 메인 블루프린트 생성
main = Blueprint('main', __name__)

# 메인 페이지 라우트
@main.route('/')
def index():
    return render_template('index.html')

# About 페이지 라우트
@main.route('/about')
def about():
    return render_template('about.html')