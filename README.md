# DailyDevQ-Main-Repo

DailyDevQ는 개발자를 위한 AI 기반의 기술 면접 질문 및 학습 관리 플랫폼입니다. AWS 서버리스 아키텍처와 다양한 소셜 로그인 기능을 활용하여 사용자 친화적이고 효율적인 학습 환경을 제공합니다.

---

## 주요 기능

- **소셜 로그인**: Google, GitHub, Kakao, Naver를 통한 간편한 로그인 지원
- **DynamoDB 데이터 저장**: 사용자 정보를 안전하게 관리
- **AI 기반 면접 질문 제공**: OpenAI API를 활용하여 맞춤형 면접 질문 생성
- **E-mail 구독 서비스**: AWS SES를 통한 일일 면접 질문 이메일 발송
- **학습 진행 상황 관리**: Flask 기반 대시보드로 학습 데이터를 시각화

---

## 기술 스택

### 프론트엔드
- **Flask**: 웹 프레임워크
- **Jinja2**: 템플릿 엔진
- **Bootstrap 5**: UI 구성

### 백엔드
- **Python**: 3.10+
- **AWS DynamoDB**: NoSQL 데이터베이스
- **AWS Lambda**: 서버리스 컴퓨팅
- **OpenAI API**: GPT-3.5 Turbo
- **AWS SES**: 이메일 서비스

### 인프라
- **AWS**: EC2, S3, IAM, VPC
- **Terraform**: 인프라 코드 관리
- **GitHub Actions**: CI/CD 파이프라인 구축

---

## 설치 및 실행

### 1. 클론 및 가상환경 설정

```bash
git clone https://github.com/DailyDevQ/dailydevq-main.git
cd dailydevq-main

# 가상환경 생성 및 활성화
python -m venv dailydevq-venv
source dailydevq-venv/bin/activate  # Windows는 dailydevq-venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 아래 내용을 추가합니다

```dotenv
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
KAKAO_CLIENT_ID=your_kakao_client_id
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
```

### 4. 애플리케이션 실행

```bash
flask run
```


## 디렉토리 구조 (지속적인 업데이트 예정.)

```plaintext
dailydevq-main/
├── frontend/
│   ├── app/
│   │   ├── static/
│   │   │   ├── css/            # CSS 파일
│   │   │   │   └── style.css
│   │   │   └── js/             # JavaScript 파일
│   │   ├── templates/
│   │   │   ├── auth/           # 인증 관련 HTML 템플릿
│   │   │   │   └── dashboard/
│   │   │   ├── 404.html        # 404 에러 페이지
│   │   │   ├── 500.html        # 500 에러 페이지
│   │   │   ├── base.html       # 공통 레이아웃 템플릿
│   │   │   └── index.html      # 메인 페이지
│   │   ├── __init__.py         # 패키지 초기화 파일
│   │   ├── app.py              # Flask 애플리케이션 진입점
│   │   └── routes.py           # 라우트 관리
├── backend/
│   ├── functions/
│   │   ├── email_sender/       # 이메일 발송 관련 코드
│   │   ├── handler.py          # Lambda 핸들러
│   │   └── user_service.py     # 사용자 정보 관리 함수
├── infrastructure/
│   ├── dynamodb.tf             # DynamoDB 설정
│   ├── outputs.tf              # Terraform 출력
│   ├── providers.tf            # AWS 프로바이더 설정
│   ├── terraform.tfvars        # Terraform 변수 값 (Git에 업로드 금지) 따로 생성 후 사용.
│   └── variables.tf            # Terraform 변수 정의
├── requirements/
│   ├── base.txt                # 기본 패키지 목록
│   ├── dev.txt                 # 개발용 패키지
│   └── test.txt                # 테스트용 패키지
├── requirements_split.py       # requirements 파일 생성 스크립트
├── .gitignore                  # Git에서 제외할 파일 목록
├── LICENSE                     # 라이선스 파일
├── MAIN-LOGO.jpg               # DailyDevQ 샘플 로고 이미지
├── README.md                   # 프로젝트 설명 파일
└── .env                        # 환경 변수 파일 (Git에 업로드 금지) 따로 생성 후 사용.
```

---

### 주요 업데이트 내용
1. **`auth/` 디렉토리**:
   - 인증 관련 HTML 파일은 `/templates/auth/` 디렉토리에 저장.
   - 세부 인증 페이지(예: 대시보드 등)는 `/templates/auth/dashboard/`에서 관리.

2. **에러 페이지 추가**:
   - `404.html` (Not Found) 및 `500.html` (Internal Server Error) 페이지 추가.

3. **정적 파일 디렉토리 구조화**:
   - `static/` 디렉토리 아래 `css/`와 `js/`로 파일을 구분하여 관리.

4. **Terraform 디렉토리 명확화**:
   - `.terraform/` 디렉토리로 Terraform 자동 생성 파일 구분.
   - 주요 설정 파일은 상위 디렉토리에 위치.

---
> **Note**: 이 디렉토리 구조는 현재 개발 진행 중인 상태를 반영하고 있습니다. 프로젝트가 진행됨에 따라 디렉토리와 파일이 추가될 수 있습니다.
---

### 주요 파일 설명

#### `requirements_split.py`
`requirements_split.py`는 Python 프로젝트의 의존성을 관리하기 위한 스크립트입니다. 이 코드를 실행하면 `requirements` 디렉토리에 의존성을 목적별로 나눠 관리하는 파일들을 생성합니다.

##### 주요 기능:
- **의존성 파일 자동 생성**: `base.txt`, `dev.txt`, `test.txt` 생성
- **중복 관리 방지**: `base.txt`를 다른 의존성 파일에서 재사용
- **명확한 의존성 구분**: 개발, 테스트, 배포 목적에 맞는 패키지 분리

##### 코드 예시:
```python
# ./requirements_split.py

import os

# 기본 패키지 목록
base_packages = """Flask==3.1.0
requests==2.32.3
python-dotenv==1.0.1
"""

# 개발용 패키지 목록
development_packages = """black==24.10.0
flake8==7.1.1
"""

# 테스트용 패키지 목록
testing_packages = """pytest==8.3.3
coverage==7.3.1
"""

# requirements 디렉토리 생성
os.makedirs('requirements', exist_ok=True)

# 각 목적별 파일 생성
with open('requirements/base.txt', 'w') as f:
    f.write(base_packages)

with open('requirements/dev.txt', 'w') as f:
    f.write("-r base.txt\n")  # 기본 패키지 포함
    f.write(development_packages)

with open('requirements/test.txt', 'w') as f:
    f.write("-r base.txt\n")  # 기본 패키지 포함
    f.write(testing_packages)

print("requirements 디렉토리와 관련 파일이 생성되었습니다.")
```

#### 사용 방법
1. 해당 파일을 프로젝트 루트 디렉토리에 위치시킵니다.
2. 아래 명령어를 실행합니다:
   ```bash
   python requirements_split.py
   ```
3. `requirements/` 디렉토리에 생성된 파일을 확인합니다:
   - `base.txt`: 기본 패키지
   - `dev.txt`: 개발용 패키지
   - `test.txt`: 테스트용 패키지

이 스크립트는 의존성 관리를 간소화하고, 코드 충돌을 방지하는 데 도움을 줍니다.

---

## 기여 방법

1. 이 저장소를 포크합니다.
2. 기능 추가나 버그 수정을 위한 브랜치를 생성합니다.
3. 코드를 커밋하고 `git push`합니다.
4. Pull Request를 생성하여 변경 사항을 요청합니다.

---

## 라이선스

이 프로젝트는 **Apache License 2.0** 하에 배포됩니다. 자세한 내용은 [LICENSE](./LICENSE)를 참조하세요.

---

## 문의

- **이메일**: dailydevq@gmail.com
- **GitHub**: [DailyDevQ](https://github.com/DailyDevQ)
