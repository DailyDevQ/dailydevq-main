# **DailyDevQ-Main-Repo**

[![EN](https://img.shields.io/badge/lang-en-blue.svg)](/README/README-en.md) 
[![KR](https://img.shields.io/badge/lang-kr-red.svg)](/README.md)

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Terraform](https://img.shields.io/badge/IaC-Terraform-623CE4.svg?logo=terraform)
![AWS](https://img.shields.io/badge/Cloud-AWS-FF9900.svg?logo=amazon-aws)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF.svg?logo=github-actions)
![OpenAI](https://img.shields.io/badge/AI-OpenAI-412991.svg?logo=openai)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
<!-- ![Build Status](https://github.com/DailyDevQ/dailydevq-main/actions/workflows/main.yml/badge.svg) -->

DailyDevQ is an AI-powered technical interview question and learning management platform designed for developers. By leveraging an AWS serverless architecture and diverse social login options, it provides a user-friendly and efficient learning environment.

---

## **Key Features**

- **Social Login**: Easy login via Google, GitHub, Kakao, and Naver.
- **Secure Data Storage**: Manage user data securely with AWS DynamoDB.
- **AI-Powered Interview Questions**: Generate personalized interview questions using the OpenAI API.
- **Email Subscription Service**: Send daily interview questions through AWS SES.
- **Learning Progress Management**: Track and visualize progress with a Flask-based dashboard.

---

## **Technology Stack**

### **Frontend**
- **Flask**: Web framework
- **Jinja2**: Template engine
- **Bootstrap 5**: UI design

### **Backend**
- **Python**: 3.10+
- **AWS DynamoDB**: NoSQL database
- **AWS Lambda**: Serverless computing
- **OpenAI API**: GPT-3.5 Turbo
- **AWS SES**: Email service

### **Infrastructure**
- **AWS**: EC2, S3, IAM, VPC
- **Terraform**: Infrastructure as Code (IaC)
- **GitHub Actions**: CI/CD pipeline

---

## **Installation and Setup**

### **1. Clone the Repository and Set Up Virtual Environment**

```bash
git clone https://github.com/DailyDevQ/dailydevq-main.git
cd dailydevq-main

# Create and activate a virtual environment
python -m venv dailydevq-venv
source dailydevq-venv/bin/activate  # On Windows: dailydevq-venv\Scripts\activate
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Configure Environment Variables**
Create a `.env` file in the root directory of the project and add the following:

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

### **4. Run the Application**

```bash
flask run
```

---

## **Directory Structure** *(Subject to updates as the project evolves)*

```plaintext
dailydevq-main/
├── frontend/
│   ├── app/
│   │   ├── static/
│   │   │   ├── css/            # CSS files
│   │   │   │   └── style.css
│   │   │   └── js/             # JavaScript files
│   │   ├── templates/
│   │   │   ├── auth/           # Authentication-related templates
│   │   │   │   └── dashboard/
│   │   │   ├── 404.html        # 404 Error page
│   │   │   ├── 500.html        # 500 Error page
│   │   │   ├── base.html       # Base layout template
│   │   │   └── index.html      # Main page
│   │   ├── __init__.py         # Package initializer
│   │   ├── app.py              # Flask application entry point
│   │   └── routes.py           # Route management
├── backend/
│   ├── functions/
│   │   ├── email_sender/       # Email dispatch logic
│   │   ├── handler.py          # Lambda handler
│   │   └── user_service.py     # User management functions
├── infrastructure/
│   ├── dynamodb.tf             # DynamoDB configuration
│   ├── outputs.tf              # Terraform outputs
│   ├── providers.tf            # AWS provider configuration
│   ├── terraform.tfvars        # Terraform variable values (excluded from Git)
│   └── variables.tf            # Terraform variable definitions
├── requirements/
│   ├── base.txt                # Base dependencies
│   ├── dev.txt                 # Development dependencies
│   └── test.txt                # Testing dependencies
├── requirements_split.py       # Script for managing requirements files
├── .gitignore                  # Git ignore rules
├── LICENSE                     # License file
├── MAIN-LOGO.jpg               # Sample logo image for DailyDevQ
├── README.md                   # Project description
└── .env                        # Environment variable file (excluded from Git)
```

---

### **Recent Updates**

1. **`auth/` Directory**:
   - Templates related to authentication are organized under `/templates/auth/`.
   - Subpages such as dashboards are placed in `/templates/auth/dashboard/`.

2. **Error Pages Added**:
   - `404.html` (Not Found) and `500.html` (Internal Server Error) are included for improved user experience.

3. **Static File Organization**:
   - CSS and JavaScript files are organized under `/static/css/` and `/static/js/`.

4. **Terraform Clarifications**:
   - Generated Terraform files are separated in `.terraform/`.
   - Main configuration files remain in the root directory.

---

### **Key File Highlight: `requirements_split.py`**
This script simplifies dependency management by splitting them into `base.txt`, `dev.txt`, and `test.txt`.

#### **How It Works**
1. Creates the required dependency files in the `requirements/` directory.
2. Ensures dependencies are grouped for specific purposes (e.g., testing, development).
3. Helps prevent version conflicts by reusing `base.txt`.

#### **Usage**
Run the following command to generate the files:
```bash
python requirements_split.py
```

---

## **Contributing**

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch to your fork.
4. Open a Pull Request to this repository.

---

## **License**

This project is distributed under the **Apache License 2.0**. See [LICENSE](./LICENSE) for details.

---

## **Contact**

- **Email**: dailydevq@gmail.com
- **GitHub**: [DailyDevQ](https://github.com/DailyDevQ)