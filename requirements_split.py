# requirements_split.py

import os

# 기본 패키지 (Flask 관련 핵심 패키지)
base_packages = """Flask==3.1.0
blinker==1.9.0
click==8.1.7
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==3.0.2
Werkzeug==3.1.3
python-dotenv==1.0.1
typing_extensions==4.12.2
requests==2.32.3
"""

# 개발용 패키지 (코드 포맷팅, 린팅 도구)
development_packages = """black==24.10.0
flake8==7.1.1
mccabe==0.7.0
mypy-extensions==1.0.0
packaging==24.2
pathspec==0.12.1
platformdirs==4.3.6
pycodestyle==2.12.1
pyflakes==3.2.0
"""

# 테스트용 패키지
testing_packages = """pytest==8.3.3
exceptiongroup==1.2.2
iniconfig==2.0.0
pluggy==1.5.0
tomli==2.1.0
"""

# requirements 디렉토리 생성
os.makedirs('requirements', exist_ok=True)

# 각 파일 생성 및 내용 작성
with open('requirements/base.txt', 'w') as f:
    f.write(base_packages)

with open('requirements/dev.txt', 'w') as f:
    f.write("-r base.txt\n")  # base.txt 의존성 포함
    f.write(development_packages)

with open('requirements/test.txt', 'w') as f:
    f.write("-r base.txt\n")  # base.txt 의존성 포함
    f.write(testing_packages)

# 프로덕션용 requirements.txt 업데이트
with open('requirements.txt', 'w') as f:
    f.write("-r requirements/base.txt\n")
