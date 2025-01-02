# ./frontend/app/routes.py

import os
import openai
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

bp = Blueprint('main', __name__)

@bp.route('/logout')
def logout():
    # 로그아웃 처리 후 메인 페이지로 리다이렉트 (예: index 페이지가 있다면 'main.index'로 대체)
    from flask_login import logout_user
    logout_user()
    return "로그아웃 완료"  # 또는 redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@bp.route('/generate-question', methods=['GET', 'POST'])
@login_required
def generate_question():
    """
    OpenAI API를 통해 질문을 생성하는 예시 라우트
    """
    openai.api_key = os.getenv('OPENAI_API_KEY', 'YOUR_DEFAULT_API_KEY')
    generated_question = None

    if request.method == 'POST':
        user_input = request.form.get('tech_stack', 'Cloud')
        prompt_text = f"다음 기술 스택 {user_input}에 대한 면접 질문을 생성해 주세요."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_text,
            max_tokens=80,
            temperature=0.7,
        )
        generated_question = response.choices[0].text.strip()

    return render_template('dashboard/generate_question.html', question=generated_question)
